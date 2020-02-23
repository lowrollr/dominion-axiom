
import random as random

from ai_plugins.dominion_ai import AI
from game import *
from ai_plugins.randomania import Randomania
#note: this ai scheme will stop working as of now if the default 7 supply cards (i.e. copper, silver, gold, province, duchy, estate, curse) are used
#miser: never plays or buys actions. Just buys provinces, gold, and silver, in the most efficient way possible.

#Try to dicard things that aren't treasures first, and then discard treasures in order of lowest value
def miser_discard(_deck):
    for x in _deck.hand:
        if not x.worth:
            return x
    #hand is literally all treasures
    lowest_value = 9999999
    lowest_card = _deck.hand[0]
    for x in _deck.hand:
        if x.worth < lowest_value:
            lowest_value = x.worth
            lowest_card = x
    return lowest_card


#miser_trash will just work the exact same as discard so we'll just pass miser_discard
def miser_buy(_shop, _deck, _coins):
    if _coins >= 8:
        return Province()
    elif _coins >= 6:
        return Gold()
    elif _coins >= 3:
        return Silver()
    else:
        return ImaginaryCard()


#other types of decisions aren't really import for this scheme at this time
Miser = AI(Randomania.action_fn, miser_discard, Randomania.discard_option_fn, miser_buy, \
    Randomania.trash_fn, Randomania.trash_for_treasure_fn, Randomania.gain_fn)