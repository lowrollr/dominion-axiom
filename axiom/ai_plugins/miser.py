
import random as random
import sys

from ai_plugins.dominion_ai import AI
from game import *

#this AI scheme never plays or buys actions. Just buys provinces, gold, and silver, in the most efficient way possible.

class Miser(AI):
    #Try to dicard things that aren't treasures first, and then discard treasures in order of lowest value
    def discard_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = super().process_decision_params(_stip, _optional)
        for x in stip(_player.my_deck.hand):
            #discard the first card found that isn't worth coins
            if not x.worth:
                return x
        #if the hand is literally all treasures...
        #if it's optional to discard, don't dicard anything
        if _optional:
            return ImaginaryCard()
        #if it's not optional, find the card with the lowest value and discard that one
        else:
            lowest_value = sys.maxsize
            lowest_card = _player.my_deck.hand[0]
            for x in _player.my_deck.hand:
                if x.worth < lowest_value:
                    lowest_value = x.worth
                    lowest_card = x
            return lowest_card

    #miser_trash will just work the exact same as discard so we'll just pass miser_discard
    def buy_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = super().process_decision_params(_stip, _optional)
        #get the cards the player can afford
        cards_available = _game.shop.get_cards_under_amount(_player.coins)
        #the cards the player is interested in buying are only Silver, Gold, and Provinces
        stip_cards = stip([Province(), Gold(), Silver()])
        list_of_cards = []
        #see if the cards_available contain Silver, Gold, or Province
        for x in stip_cards:
            for y in cards_available:
                if type(x) is type(y):
                    list_of_cards.append(x)
        #if a Province is available, buy a Province, if not buy a Gold, if not buy a Silver
        if card_in_list(Province(), list_of_cards):
            return Province()
        elif card_in_list(Gold(), list_of_cards):
            return Gold()
        elif card_in_list(Silver(), list_of_cards):
            return Silver()
        else:
            #if Silver, Gold, and Provinces are not available
            #if it's optional don't buy anything
            if _optional:
                return ImaginaryCard()
            #if it's not optional just buy a random card
            else:
                return random.choice(cards_available)
