import random
import re

##### REGEX DEFS ######
basic_action_regex = re.compile("^\+(.) (.*)$")

#######################

class Game:
    def __init__(self, my_players):
        self.players = my_players
        for x in self.players:
            x.join_game(self)
        self.num_players = len(self.players)
        self.trash = []
        self.active_player = self.players[0]
        self.active_player_number = 0

    def play_card(self, card):
        self.active_player.deck.hand.remove(card)
        self.active_player.deck.in_play.append(card)
        if card.is_attack:
            self.process_card_actions(card.actions, None)
            self.process_attack(card.additional_action)
        else:
            self.process_card_actions(card.actions, card.additional_action)

    def buy_card(self, card):

    def process_card_actions(self, actions, additional_action):
        
    def process_attack(self, attack_fn):
        for x in self.players:
            reactions = x.deck.get_reactions_in_hand()
            blocked = False
            if reactions != None:
                for y in reactions:
                    
            if not blocked:
                attack_fn(self, x)
    
    def next_turn(self)
        self.active_player.cleanup()
        self.active_player_number = (self.active_player_number + 1) % self.num_players
        self.active_player = self.players[self.active_player_number]


class Shop:
    def __init__(self, my_supply_dict):
        self.supply = my_supply_dict

class Card:
    def __init__(self, my_base_actions, my_cost, my_pts, my_worth, my_additional_action, _is_attack, _is_reaction, my_reaction):
        self.actions = my_actions
        self.cost = my_cost
        self.pts = my_pts
        self.worth = my_worth
        self.additional_action = my_additional_action
        self.is_attack = _is_attack
        self.is_reaction = _is_reaction
        self.reaction = my_reaction

class Player:
    def __init__(self, starting_deck, my_name, decision_dict):
        self.my_deck = starting_deck
        self.name = my_name
        self.actions = 1
        self.buys = 1
        self.action_alg = action_choice_alg
        self.buy_alg = buy_choice_alg
        self.game = None
        self.decisions = decision_dict

    def join_game(self, game_to_join):
        self.game = game_to_join

    def play_actions(self, action_cards):
        if self.actions > 0:
            action_to_play = self.action_alg(action_cards)
            self.game.play_card(action_to_play)
            self.actions -= 1
            self.play_actions(action_cards - action_to_play)
    
    def buy_cards(self):

        
    def cleanup(self):
        self.my_deck.cleanup_deck_actions()
        self.actions = 1
        self.buys = 1

class Deck:
    def __init__(self, my_cards):
        self.cards = my_cards
        self.draw_pile = []
        self.discard_pile = []
        self.hand = []
        self.in_play = []

    def shuffle(self):
        self.draw_pile = self.draw_pile + random.shuffle(self.discard_pile)
        self.discard_pile = []

    def cleanup_deck_actions(self):
        self.discard_pile = self.discard_pile + self.hand + self.in_play
        self.hand = []
        self.in_play = []
        self.draw(5)

    def draw(self, amnt):
        if len(self.draw_pile) < 5:
            self.shuffle()
        for i in range(amnt):
            self.hand += self.draw_pile.pop()

    def discard(self, cards):
        for x in cards:
            self.hand.remove(x)
            self.discard_pile.append(x)

    def place(self, card, offset):
        self.draw_pile.insert(card, offset)

    def calc_hand_value(self):
        total_value = 0
        for x in self.hand:
            total_value += x.worth
        return total_value
    
    def get_actions_in_hand(self):
        my_hand_actions = []
        for x in self.hand:
            if x.actions != None:
                my_hand_actions += x
        return my_hand_actions

    def get_reactions_in_hand(self):
        my_hand_reactions = []
        for x in self.hand:
            if x._is_reaction:
                my_hand_reactions += x
        return my_hand_reactions

####### GAME CARDS (& thier additonal actions) ###########
copper = Card(None, 0, 0, 1, None, False, False, None)
silver = Card(None, 3, 0, 2, None, False, False, None)
gold = Card(None, 6, 0, 3, None, False, False, None)
curse = Card(None, 0, -1, 0, None, False, False, None)
estate = Card(None, 2, 1, 0, None, False, False, None)
duchy = Card(None, 5, 3, 0, None, False, False, None)
province = Card(None, 8, 6, 0, None, False, False, None)

def cellar_action(my_game):
    cur_player = my_game.active_player
    for x in cards_to_discard:
        cur_player.discard(x)
    cur_player.draw(len(cards_to_discard))

cellar = Card(['+1 Action'], 2, 0, 0, cellar_action, False, False, None)
market = Card(['+1 Card', '+1 Action', '+1 Buy', '+1 Coin'], 5, 0, 0, None, False, False, None)

def merchant_action(my_game):
    cur_player = my_game.active_player
    if silver in cur_player.hand:
        my_game.process_card_actions('+1 Coin', None)

merchant = Card(['+1 Card', '+1 Action'], 3, 0, 0, merchant_action, False, False, None)

def militia_action(my_game, target_player):
    if target_player.hand

#####################################################


def play_random_action(my_actions):
    return random.choice(my_actions, 1)

def start_game(num_players):