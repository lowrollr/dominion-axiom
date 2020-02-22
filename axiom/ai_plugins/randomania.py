
import random as random

from ai_plugins.dominion_ai import AI
from cards import *
from game import *

#randomania: always choose a decision randomly given all possible decisions -- this one is very very bad
def randomania_action(_deck, _actions):
    return random.choice(_actions + [ImaginaryCard()])

def randomania_discard(_deck):
    return random.choice(_deck.hand)

def randomania_discard_option(_deck):
    return random.choice(_deck.hand + [ImaginaryCard()])

def randomania_buy(_shop, _deck, _coins):
    cards_available = _shop.get_cards_under_amount(_coins)
    return random.choice(cards_available + [ImaginaryCard()])

def randomania_trash(_self, _deck, _coins):
    return random.choice(_deck.hand)

def randomania_trash_for_treasure(_shop, _deck, _coins):
    treasures = []
    for x in _deck.hand:
        if x.worth > 0:
            treasures += [x]
    treasures += [ImaginaryCard()]
    treasure_to_trash = random.choice(treasures)
    return treasure_to_trash
    
def randomania_gain(_shop, _deck, _limit):
    cards_available = _shop.get_cards_under_amount(_limit)
    return random.choice(cards_available)

Randomania = AI(randomania_action, randomania_discard, randomania_discard_option, randomania_buy, \
    randomania_trash, randomania_trash_for_treasure, randomania_gain)