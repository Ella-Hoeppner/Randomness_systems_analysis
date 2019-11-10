"""
Runs tests, defined the constants at the top of the code, that finds the best parameters for a generalied deck and dynamic dice according to the constraints that the constants define. It then measures the entropy and variance of the systems defined by the discovered parameters over some number of samples, and outputs the results to a csv file.
"""

import randomness_systems as rs
import stats
import write_results

# The number of possible values that each randomness system should return
VALUES=6

# The number of step to use when calculating variance and entropy
STEPS=25

# The number of trials to use when averaging variance and entropy. A higher number will be more likely to give accurate results, but will take longer
TRIALS=10000

# MAX_SIZE_FACTOR and MAX_REFILL_CONSTANT are the maximum size factor and refill constant to consider when searching for the best generalized deck. The higher these numbers are, the longer the algorithm will take (specifically, the algorithm will search a number of generalized decks equal to the product of these two constants.)
MAX_SIZE_FACTOR=10
MAX_REFILL_CONSTANT=10

# DECREASE_FACTOR_DIVISIONS defines the number of values for decrease factor that will be used when searching for the best dynamic dice. The decrease factors used will be evenly distributed between 0 and 1. The higher this number is, the longer the algorithm will take.
DECREASE_FACTOR_DIVISIONS=100

# The minimum entropy to accept for a randomness system. Systems that have less than this entropy will be ignored. This must be a value between 0 and 1, because it is expressed as a fraction of the maximum possible entropy that a system with the given number of values could have
MIN_ENTROPY=0.9

# Find all combinations of size factor and refill constant, and define corresponding generalized decks
g_decks=[]
for i in range(1,MAX_SIZE_FACTOR+1):
  for i2 in range(1,MAX_REFILL_CONSTANT+1):
    g_decks.append(rs.GeneralizedDeck(VALUES,i,i2))

# Find the best generalized deck out of all those defined above.
best_g_deck, g_deck_variance=stats.get_lowest_variance_source(g_decks,MIN_ENTROPY,STEPS,TRIALS)

# Define all dynamic dice to test, sampling evenly between 0 and 1
d_dice=[]
for i in range(DECREASE_FACTOR_DIVISIONS):
  d_dice.append(rs.DynamicDice(VALUES,(i+0.5)/DECREASE_FACTOR_DIVISIONS))

# Find the best dynamic dest out of all those defined above
best_d_dice, d_dice_variance=stats.get_lowest_variance_source(d_dice,MIN_ENTROPY,STEPS,TRIALS)

if best_g_deck==None or best_d_dice==None:
  # If no generalizde deck or dynamic die were found, then it must have been the case that none within the tested parameters were above the minimum entropy threshold. In that case, print a message describing the failure
  if best_g_deck==None:
    print("No generalized deck above the entropy threshold was found in the range of specified parameters. Aborting.")
  if best_d_dice==None:
    print("No dynamic dice above the entropy threshold was found in the range of specified parameters. Aborting.")
else:
  # If a generalized deck and dynamic die were found, print a message describing them
  print(f"The best generalized deck parameters found were {best_g_deck.size_factor} for the size factor and {best_g_deck.refill_constant} for the refill constant. The resulting variance was {g_deck_variance}.")
  print(f"The best dynamic dice parameter found was {best_d_dice.decrease_factor} for the decrease factor. The resulting variance was {d_dice_variance}.")

  # Compute the relevant statistics of the best generalized deck and dynamic dice, as well as the statistics of a basic deck and basic dice system for comparison.
  deck_results=stats.get_stats(rs.Deck(VALUES), STEPS, TRIALS)
  dice_results=stats.get_stats(rs.Dice(VALUES), STEPS, TRIALS)
  g_deck_results=stats.get_stats(best_g_deck, STEPS, TRIALS)
  d_dice_results=stats.get_stats(best_d_dice, STEPS, TRIALS)

  # Write the results to a csv file so that they can be analyzed
  write_results.write_results("out.csv",deck_results+dice_results+g_deck_results+d_dice_results, ["Deck entropy", "Deck variance", "Dice entropy", "Dice variance", "Generalized Deck entropy", "Generalizde Deck variance", "Dynamic Dice entropy", "Dynamic Dice variance"])

  print("The results have been saved to out.csv")