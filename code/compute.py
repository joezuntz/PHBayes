#import numpy, the main python pckage for numerical work.  Rename it for clarity.
import numpy as np

#import the python module for monte-carlo markov chains and other Bayesian things
import pymc

#Load in the data.  For now just use some mock data
#For each star we will have several data elements:
#   for each transit that *anyone* detects
#      a mass m
#      the number of people who found it
#      the number of people who did not find it

# The parameters of our model:
# The probability of a person missing a transit of mass m (false negative rate)
### The probability of a person seeing a transit of mass m when none exists (false positive rate) = 0 for now
# The probability of a star having n transits, for n=0,..
# Let's go up to 10 here.
# The probability that the transits are of masses {m_i}, given that there are n of them

maximum_transits = 10

#Some thoughts on this bit.
#It might be easier to reparameterize this as
#p_0 = P(0 or more planets) = 1
#p_1 = P(1 or more planets | 0 or more planets)
#p_2 = P(2 or more planets | 1 or more planets)
#p_3 = P(3 or more planets | 2 or more planets)
#as this way all the parameters are just numbers from 0 to 1
#for now we can put our prior on these numbers as uniform in 0..1
#If you find it upsetting that we are using probabilities of probabilites then you can just
#imagine that we are using probabilities of fractions, instead of probabilities of probabilities
#(although in fact the latter is perfectly okay).  I will reflect that common discomfort in the
#variable names.

#So we are saying that if we were told that 15% of stars in the Kepler sample had at least 3 transits
#and were asked to guess how many had at least 4 transits, then we would say that we thought it was equally 
#likely to be anything between 0% and 15%.


#We will call that list of parameters:
fraction_atleast = []

#All stars have at least zero transits :-)
fraction_atleast.append(1)

#So let's loop up to the maximum number of transits adding a parameter with a uniform prior for each one.
#In PyMC you create variables by specifying your prior - it forces you to be a good bayesian.
for i in xrange(maximum_transits):
	name = 'prob_at_least_%d_transits_given_at_least_%d' % (i+1,i)
	p_i = pymc.Uniform(name,0.0,1.0)
	fraction_atleast.append(p_i)


#We have said that we have now reached the maximum number of transits, so the next number is zero
#i.e. we are asserting that if a planet has at least 10 planets then it definitely 
#does not have 11 or more.  It might seem a bit silly to put this here, but it will be useful later.
fraction_atleast.append(0)

#So how do we compute the probability of having n planets, given these numbers?
#Well, it's the probability p of having at least n planets, and not at least n+1
# p = p_0 * p_1 * p_2 * ... p_n * (1-p_{n+1})
# so we can use that probability when the time comes.
#I wonder if we can just generate these parameters programatically?
#Yes!  PyMC rocks!  We are creating what it calls "deterministic" variables here - ones that depend 
#only on their parent parameters.  We just create them by doing the simple maths.

fraction_exactly = []
for i in xrange(maximum_transits+1):
	p = fraction_atleast[0]  #This is identically one.
	for j in xrange(i-1):
		p = p * fraction_atleast[j]
	p = p * (1-fraction_atleast[i+1])
	p.__name__ = "fraction_exactly_%d_transits" % i
	p.trace = True  #This says that we do want to record the values of this parameter.
	fraction_exactly.append(p)
	
#We have decided that the maximum number of transits is maximum_transits, so the probability of having 11
#or indeed any more is zero.
fraction_exactly.append(0)

#Hopefully planetary people will actually have better priors on these things.


#Okay, now the mass bit.
#Our new parameters are a bunch of numbers that represents the probability that, given a star with n transits, 
#those transits have mass m1,m2,m3,m4.  So how the hell am I going to do this?  Maybe it is trivial?
#It probably isn't a very good assumption, but we can claim that all the planets are drawn from the same
#distribution separately (i.e. we assume that the masses of planets in a system are independent).
#So in fact we just have one parameter per mass bin, which is the fraction of transits with that mass.

#These things have to add up to 1 too, just like with the number counts, so we probably want to do something 
#similar and use a cumlulative mass profile (i.e. we want N(mass>M) as a function of M).
#This won't be like the number counts in that we cannot use the same cumulative hierarchy thing as before.
#We probably need to define some mass bins first.

#Okay, so now it's detectabilities/user response function.  We are modelling this in the same mass bins as
#we model the masses in, I think.
