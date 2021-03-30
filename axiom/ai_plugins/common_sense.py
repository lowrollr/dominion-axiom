import random as random
import sys

from ai_plugins.dominion_ai import AI
from game import *

#The general theory behind this AI scheme is just to eliminate stupid plays. 
#It is mostly ensures that certain plays AREN'T made rather than ensuring certain plays ARE made
#In general, Common_Sense will:
#not buy Curses and Copper
#always play available actions
#sequence actions to allow for action-chaining
#discard victory point cards
#always spends coins/execute gains efficiently (maximize value)
class Common_Sense(AI):
    def action_fn(self, _game, _player, _stip, _optional): #always play actions if able, always chain actions if able
        stip, optional_card = super().process_decision_params(_stip, _optional)
        #get action cards that can be played in the player's hand
        available_actions = stip(_player.my_deck.get_actions_in_hand())
        #if there are no available actions to play
        if not available_actions:
            return ImaginaryCard()
        #try to sequence actions efficiently
        for x in available_actions:
            #card gives additional actions?
            for y in x.actions:
                act_type = card_action_regex(y)
                if act_type == 'Action' or act_type == 'Actions':
                    return x
        #if actions cannot be chained, play the action with the highest shop value
        highest_value = -1
        highest_value_card = ImaginaryCard()
        for x in available_actions:
            if x.cost > highest_value:
                highest_value = x.cost
                highest_value_card = x
        return highest_value_card

    def discard_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = super().process_decision_params(_stip, _optional)
        #if a victory point card found that isn't an action or a treasure, discard that
        #if not, discard the card with the lowest value
        lowest_value = sys.maxsize
        lowest_value_card = ImaginaryCard()
        #get cards that can be discarded from the player's hand
        available_cards = stip(_player.my_deck.hand)
        for x in available_cards:
            #check for vp cards that aren't also actions or treasrues
            if x.pts and not x.worth and not x.actions and not x.additional_action:
                return x
            #find low value card
            elif x.cost < lowest_value:
                lowest_value = x.cost
                lowest_value_card = x
        #if it's not optional to discard, return the lowest valued card
        if not _optional:
            return lowest_value_card
        #if it is optional, don't discard anything
        else:
            return ImaginaryCard()
    
    def buy_fn(self, _game, _player, _stip, _optional):
        #buy the highest-costed available card
        stip, optional_card = super().process_decision_params(_stip, _optional)
        highest_value = 0
        highest_value_card = ImaginaryCard()
        #get available cards from the shop
        available_cards = stip(_game.shop.get_cards_under_amount(_player.coins))
        #find the card with the highest value that the player can afford
        for x in available_cards:
            if x.cost > highest_value:
                highest_value = x.cost
                highest_value_card = x
        #return that card
        return highest_value_card

    def gain_fn(self, _game, _player, _stip, _optional):
        #gain the highest-costed available card (this works the same as buy)
        stip, optional_card = super().process_decision_params(_stip, _optional)
        highest_value = -1
        highest_value_card = ImaginaryCard()
        available_cards = stip(_game.shop.get_cards_under_amount(sys.maxsize))
        for x in available_cards:
            if x.cost > highest_value:
                highest_value = x.cost
                highest_value_card = x
        return highest_value_card
        
    def put_on_top_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = super().process_decision_params(_stip, _optional)
        #get cards in hand that the player can put on top
        available_cards = stip(_player.my_deck.hand)
        
        #if the player is out of actions for the turn, put the highest valued action in hand on top
        if not _player.actions: 
            #find the highest valued action card in the player's hand
            highest_value = -1
            highest_value_card = ImaginaryCard()
            for x in available_cards:
                if x.cost > highest_value and (x.actions or x.additional_action or x.attack_fn):
                    highest_value = x.cost
                    highest_value_card = x
            if highest_value != -1:
                return highest_value_card
            #if there are no actions, put the highest valued card on top
            highest_value = -1
            highest_value_card = ImaginaryCard()
            for x in available_cards:
                if x.cost > highest_value:
                    highest_value = x.cost
                    highest_value_card = x
            #put that card on top
            return highest_value_card
        #if the player is not out of actions, just put the highest valued non-action card on top
        else:
            #determine which cards are not actions
            not_actions = []
            for x in available_cards:
                if not x.actions and not x.additional_action and not x.attack_fn:
                    not_actions.append(x)
            if _optional:
                return ImaginaryCard()  
            else:
                #if there are not any non-actions, put a random card on top
                if not not_actions:
                    return(random.choice(available_cards))
                #if there are, randomly select one of those to put on top
                return(random.choice(not_actions))
    
