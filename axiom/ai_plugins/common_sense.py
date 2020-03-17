import random as random
import sys

from ai_plugins.dominion_ai import AI
from game import *


#makes plays that make sense
#wont buy curses/copper
#will play actions
#will discard victory point cards
#will sequence actions to allow for action-chaining
#always spends money efficiently
class Common_Sense(AI):

    def action_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = super().process_decision_params(_stip, _optional)
        available_actions = stip(_player.my_deck.get_actions_in_hand())
        if not available_actions:
            return ImaginaryCard()
        #try to sequence actions efficiently
        for x in available_actions:
            #card gives additional actions?
            for y in x.actions:
                act_type = card_action_regex(y)
                if act_type == 'Action' or act_type == 'Actions':
                    return x

        lowest_value = sys.maxsize
        lowest_value_card = ImaginaryCard()
        for x in available_actions:
            if x.cost < lowest_value:
                lowest_value = x.cost
                lowest_value_card = x
        return lowest_value_card

    def discard_fn(self, _game, _player, _stip, _optional):
        #going to try to stay simple here so we'll be discarding the card with the
        #lowest value (lowest buy price in this case) if no vp cards are in hand
        #this isn't always optimal but this is just another baseline bot
        stip, optional_card = super().process_decision_params(_stip, _optional)
        lowest_value = sys.maxsize
        lowest_value_card = ImaginaryCard()
        available_cards = stip(_player.my_deck.hand)
        for x in available_cards:
            #check for vp cards
            if x.pts:
                return x
            #find low value card
            elif x.cost < lowest_value:
                lowest_value = x.cost
                lowest_value_card = x
        if not _optional:
            return lowest_value_card
        else:
            return ImaginaryCard()
    
    def buy_fn(self, _game, _player, _stip, _optional):
        #buy the highest-costed available card
        stip, optional_card = super().process_decision_params(_stip, _optional)
        highest_value = 0
        highest_value_card = ImaginaryCard()
        available_cards = stip(_game.shop.get_cards_under_amount(_player.coins))
        for x in available_cards:
            if x.cost > highest_value:
                highest_value = x.cost
                highest_value_card = x
        return highest_value_card

    def gain_fn(self, _game, _player, _stip, _optional):
        #buy the highest-costed available card
        stip, optional_card = super().process_decision_params(_stip, _optional)
        highest_value = 0
        highest_value_card = ImaginaryCard()
        available_cards = stip(_game.shop.get_cards_under_amount(sys.maxsize))
        for x in available_cards:
            if x.cost > highest_value:
                highest_value = x.cost
                highest_value_card = x
        return highest_value_card
        
    def put_on_top_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = super().process_decision_params(_stip, _optional)
        available_cards = stip(_player.my_deck.hand)
        if not _player.actions: #played all actions for turn
            highest_value = 0
            highest_value_card = ImaginaryCard()
            for x in available_cards:
                if x.cost > highest_value:
                    highest_value = x.cost
                    highest_value_card = x
            return highest_value_card
        else:
            not_actions = []
            for x in available_cards:
                if not x.actions and not x.additional_action and not x.attack_fn:
                    not_actions += [x]
            if _optional:
                return ImaginaryCard()  
            else:
                if not not_actions:
                    return(random.choice(available_cards))
                return(random.choice(not_actions))
    
    # #Returns the card if it is drawn, otherwise places it in discard or draw pile accordingly
    # def draw_or_discard_from_deck_fn(self, _game, _player, _stip, _optional):
    #     stip, optional_card = super().process_decision_params(_stip, _optional)
    #     top_card = _player.my_deck.draw_pile.pop()
    #     if stip([top_card]):
    #         if top_card.actions or top_card.additional_action or top_card.attack_fn:
    #             if _player.actions:
    #                 return top_card
    #             else:
    #                 if _optional:
    #                     _player.my_deck.place(top_card, 0)
    #                     return ImaginaryCard()
    #                 else:
    #                     _player.my_deck.discard += [top_card]
    #                     return ImaginaryCard()
    #         elif top_card.pts:
    #             _player.my_deck.discard_pile += [top_card]
    #             return ImaginaryCard()
    #         elif top_card.worth >= 1:
    #             return top_card
    #         else:
    #             _player.my_deck.discard_pile += [top_card]
    #             return ImaginaryCard()
    #     else:
    #         #keep it on top, doesn't meet the stipulation
    #         _player.my_deck.place(top_card, 0)
    #         return ImaginaryCard()

