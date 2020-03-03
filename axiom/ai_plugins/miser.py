
import random as random
import sys

from ai_plugins.dominion_ai import AI
from game import *
#note: this ai scheme will stop working as of now if the default 7 supply cards (i.e. copper, silver, gold, province, duchy, estate, curse) are used
#miser: never plays or buys actions. Just buys provinces, gold, and silver, in the most efficient way possible.



class Miser(AI):
    #Try to dicard things that aren't treasures first, and then discard treasures in order of lowest value
    def discard_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = super().process_decision_params(_stip, _optional)
        for x in stip(_player.my_deck.hand):
            if not x.worth:
                return x
        #hand is literally all treasures
        if _optional:
            return ImaginaryCard()
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
        cards_available = _game.shop.get_cards_under_amount(_player.coins)
        stip_cards = stip([Province(), Gold(), Silver()])
        list_of_cards = []
        for x in stip_cards:
            for y in cards_available:
                if type(x) is type(y):
                    list_of_cards += [x]

        if card_in_list(Province(), list_of_cards):
            return Province()
        elif card_in_list(Gold(), list_of_cards):
            return Gold()
        elif card_in_list(Silver(), list_of_cards):
            return Silver()
        else:
            if _optional:
                return ImaginaryCard()
            else:
                return random.choice(cards_available)
