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
# The probability of a person seeing a transit of mass m when none exists (false positive rate)
# The probability of a star having n transits, for n=0,..
# The probability that the transits are of masses {m_i}, given that there are n of them.

#
