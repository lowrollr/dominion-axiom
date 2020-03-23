import random as random
import sys

from game import *

#Read the User Guide for more information about AI schemes!!!
class AI: #AI subclasses will inherit functions from 

    def __init__(self, _name):
        self.name = _name

    def process_decision_params(self, _stip, _optional): #preprocessing used 
        stip =  _stip
        #if there is no stipulation, return a function that just returns the list of cards passed to it
        if not _stip:
            stip = lambda x: x
        optional_card = []
        #when choosing between cards, optional_card can be appended to the list of cards to choose from, 
        #which will automatically handle dealing with op
        if _optional:
            optional_card = [ImaginaryCard()]
        return stip, optional_card

    def action_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        #get action cards to choose from
        choose_from = stip(_player.my_deck.get_actions_in_hand()) + optional_card
        #pick a random one to play
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()
        
    def discard_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        #get cards in hand to choose from
        choose_from = stip(_player.my_deck.hand) + optional_card
        #if there is at least one card available to pick, pick a random card from those available
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()
        
    def buy_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        #get valid cards in shop that the player is able to buy
        cards_available = _game.shop.get_cards_under_amount(_player.coins)
        choose_from = stip(cards_available) + optional_card
        #choose a random card from the valid one in the shop
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()

    def trash_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        #get a valid card from the player's hand
        choose_from = stip(_player.my_deck.hand) + optional_card
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()

    def gain_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        #get all cards in the shop, the stipulation will provide the limit if there is one
        cards_available = _game.shop.get_cards_under_amount(999999999)
        #get all valid cards to gain
        choose_from = stip(cards_available) + optional_card
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()
    
    def put_on_top_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        #get a valid card from the player's hand
        choose_from = stip(_player.my_deck.hand) + optional_card
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()
