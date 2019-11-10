"""
Defines four sytems for producing random numbers. Each system is implemented as a class. The initializer of each function takes a number of arguments, and the initializers for some of the classes take more arguments. Each class stores a variable "values", which is an that describes the number of possible values that the system can output. Additionally, each class defines the following functions:
-reset(), which resets the system so that it acts as if it was newly intialized
-sample(), which returns a value, expressed as an integer between 0 (inclusive) and the "values" variable (exclusive)
-entropy(), which returns the entropy of the probability distribution that defines the next sample
"""

from random import random
from math import log

class Dice:
  """
  A basic dice system. Each sample is chosen from a uniform distribution. Since all samples are chosen from the same distribution, this class is stateless, and the entropy() function will always return the same value.
  """
  def __init__(self, values):
    self.values=values
  def reset(self):
    pass
  def sample(self):
    return int(random()*self.values)
  def entropy(self):
    return log(self.values)

class Deck:
  """
  A basic deck system. The class keeps track of a "deck" of values, which at first contains one element for each possible value the system can return. When a smaple is chosen, a random element is chosen from the deck and returned. Once an element is chosen, it is removed from the deck, and the deck resets once all elements have been removed.
  """
  def __init__(self, values):
    self.values=values
    self.deck=[]
    self.__refill()
  def reset(self):
    self.deck=[]
    self.__refill()
  def sample(self):
    index=int(random()*len(self.deck))
    value=self.deck[index]
    del self.deck[index]
    if len(self.deck)==0:
      self.__refill()
    return value
  def entropy(self):
    return log(len(self.deck))
  def __refill(self):
    self.deck=list(range(self.values))

class GeneralizedDeck:
  """
  A generalized deck system. There are two parameters that define this system: the size factor and refill constant, each of which are integers that must be greater than 0. The deck starts with a number of copies equal to the size factor for each value it can return. When the number of elements left in the deck is less than the refill constant, a number of copies equal to the size factor of each value will be added to the deck.
  """
  def __init__(self, values, size_factor, refill_constant):
    self.values=values
    self.size_factor=size_factor
    self.refill_constant=refill_constant
    self.deck=[]
    self.__refill()
  def reset(self):
    self.deck=[]
    self.__refill()
  def sample(self):
    index=int(random()*len(self.deck))
    value=self.deck[index]
    del self.deck[index]
    if len(self.deck)<self.refill_constant:
      self.__refill()
    return value
  def entropy(self):
    # Count the number of occurrences of each value in the deck.
    occurrences=[0 for i in range(self.values)]
    for value in self.deck:
      occurrences[value]+=1
    
    # Use the number of occurrences of each value to find the probabilities, and compute the entropy from the probability distribution.
    e=0
    for o in occurrences:
      if o>0:
        p=o/len(self.deck)
        e-=p*log(p)
    return e
  def __refill(self):
    self.deck+=list(range(self.values))*self.size_factor

class DynamicDice:
  """
  A dynamic dice system. There is one parameter that defines this system: the decrease factor, which is a float that must be above 0 and less than or equal to 1. Each value that the system can return has a corresponding probability, and when a value is chosen it's probability is multiplied by the decrease factor, and then all probabilities are multiplied by a factor such that all probabilities will still sum to 1.
  """
  def __init__(self, values, decrease_factor):
    self.values=values
    self.decrease_factor=decrease_factor
    self.probabilities=[1/values for i in range(values)]
  def reset(self):
    self.probabilities=[1/self.values for i in range(self.values)]
  def sample(self):
    # Choose a value using the probability distribution
    choice=random()
    chosen_value=-1
    for i in range(self.values):
      choice-=self.probabilities[i]
      if choice<=0:
        chosen_value=i
        break
    
    # Decrease the chosen probability according to decrease_factor
    self.probabilities[chosen_value]*=self.decrease_factor

    # Find the sum of all probabilities, and then divide each probability by this sum. This will cause all probabilities to sum 1.
    probability_sum=sum(self.probabilities)
    self.probabilities=[p/probability_sum for p in self.probabilities]
    return chosen_value
  def entropy(self):
    e=0
    for p in self.probabilities:
      e-=p*log(p)
    return e