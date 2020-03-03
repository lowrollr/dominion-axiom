import random as random
import sys

from game import *

class AI:
    # def __init__(self, my_action_fn, my_discard_fn, my_discard_option_fn, my_buy_fn, my_trash_fn, my_trash_for_treasure_fn, my_gain_fn, my_put_on_top_fn, my_trash_option_fn, my_draw_or_discard_fn):
    #     self.action_fn = my_action_fn
    #     self.discard_fn = my_discard_fn
    #     self.discard_option_fn = my_discard_option_fn
    #     self.buy_fn = my_buy_fn
    #     self.trash_fn = my_trash_fn
    #     self.trash_for_treasure_fn = my_trash_for_treasure_fn
    #     self.gain_fn = my_gain_fn
    #     self.put_on_top_fn = my_put_on_top_fn
    #     self.trash_option_fn = my_trash_option_fn
    #     self.draw_or_discard_fn = my_draw_or_discard_fn

    def __init__(self, _name):
        self.name = _name

    def process_decision_params(self, _stip, _optional):
        stip =  _stip
        if not _stip:
            stip = lambda x: x
        optional_card = []
        if _optional:
            optional_card = [ImaginaryCard()]
        return stip, optional_card

    def action_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        choose_from = stip(_player.my_deck.get_actions_in_hand()) + optional_card
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()
        
    def discard_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        choose_from = stip(_player.my_deck.hand) + optional_card
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()
        
    def buy_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        cards_available = _game.shop.get_cards_under_amount(_player.coins)
        choose_from = stip(cards_available) + optional_card
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()

    def trash_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        choose_from = stip(_player.my_deck.hand) + optional_card
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()

    def gain_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        cards_available = _game.shop.get_cards_under_amount(sys.maxsize)
        choose_from = stip(cards_available) + optional_card
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()
    
    def put_on_top_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        choose_from = stip(_player.my_deck.hand) + optional_card
        if choose_from:
            return random.choice(choose_from)
        else:
            return ImaginaryCard()

    def draw_or_discard_from_deck_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = self.process_decision_params(_stip, _optional)
        top_card = _player.my_deck.draw_pile.pop()
        if stip([top_card]):
            if not _optional:
                if random.randint(0, 1):
                    return top_card
                else:
                    _player.my_deck.discard_pile += [top_card]
                    return ImaginaryCard()
            else:
                rand_num = random.randint(0, 2)
                if rand_num == 0:
                    return top_card
                elif rand_num == 1:
                    _player.my_deck.discard_pile += [top_card]
                    return ImaginaryCard()
                else:
                    _player.my_deck.place(top_card, 0) 
                    return ImaginaryCard()
        else:
            #keep it on top, doesn't meet the stipulation
            _player.my_deck.place(top_card, 0) 
            return ImaginaryCard()