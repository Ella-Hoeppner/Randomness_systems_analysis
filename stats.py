"""
Defines functions for analyzing the statistics of randomness systems.
"""

from math import log

def get_stats(source, steps, trials):
  """
  Computes the entropy and variance of the randomness system over a given number of steps, averaged over a certain number of trials.
  Args:
    source: A randomness system that defines sample(), entropy(), and a values variable (int).
    steps (int): The number of steps over which the analysis should be done.
    trials (int): The number of trials to average the statistics over. A higher number will take longer, but the results will be closer to the true average
  Return:
    tuple: Contains two lists of integers with length equal to the steps input, describing the average entropy and variance (respectively) of the system over the tested steps
  """
  entropies=[0 for i in range(steps)]
  variances=[0 for i in range(steps)]
  for i in range(trials):
    # For each trial, keep track of the current number of times each value has been chosen, so that variance can be calculated
    output_counts=[0 for i in range(source.values)]

    # Reset the randomness source, so that it behaves like a new one
    source.reset()
    for i2 in range(steps):
      # Add the current entropy in the proper location in the array
      entropies[i2]+=source.entropy()

      # Take a sample, and log the chosen value
      output_counts[source.sample()]+=1
      
      # Add the current variance in the proper location in the array
      variances[i2]+=variance(output_counts)
  
  # Divide the cumulative entropies and variances by the number of trials to get the average
  entropies=[e/(trials*log(source.values)) for e in entropies]
  variances=[v/trials for v in variances]

  return (entropies, variances)

def get_lowest_variance_source(sources, min_entropy, steps, trials):
  """
  Finds the randomness source in a given list that has the lowest variance.
  Args:
    sources (list): Contains the sources that this function will test, and select the best from
    min_entropy (float): The function will ignore any sources that have entropy under this value
    steps (int): The number of steps over which to calculate entropy and variance
    trials (int): The number of trials to use when calculating entropy and variance. A higher value will make the function take longer, but will be more likely to give the correct result
  Returns
    tuple: contains two elements: the selected randomness source, and the variance of that source. If no randomness source passes the entropy threshold, the first tuple will just be (None, 0)
  """

  best_source=None
  lowest_variance=0

  for source in sources:
    source_entropy=0
    source_variance=0

    for i in range(trials):
      # Reset the source before each trial
      source.reset()
      output_counts=[0 for i in range(source.values)]
      for i2 in range(steps):
        # For each step, keep track of the chosen value and the current entropy
        source_entropy+=source.entropy()
        output_counts[source.sample()]+=1
      source_variance+=variance(output_counts)
    
    #Find the average entropy, expressed as a fraction of the highest possible entropy that a system with the this number of values could have
    source_entropy/=trials*steps*log(source.values)

    if source_entropy>=min_entropy:
      source_variance/=trials
      if best_source==None or source_variance<=lowest_variance:
        best_source=source
        lowest_variance=source_variance
  return (best_source, lowest_variance)


def variance(values):
  """
  Returns the variance of a set of variables
  """
  average=sum(values)/len(values)
  def square(x):
    return x*x
  return sum([square(x-average) for x in values])/len(values)