
import random
import re
import copy
##### REGEX DEFS ######
basic_action_regex = re.compile("^\+(.) (.*)$")

#######################

################### CLASSES #########################
class Game:
    def __init__(self, my_players, my_shop):
        self.players = my_players
        
        self.num_players = len(self.players)
        self.trash = []
        self.active_player = self.players[0]
        self.active_player_number = 0
        self.shop = my_shop
        self.game_over = False
        self.empty_piles_needed = 4

    def play_card(self, card):
        self.active_player.my_deck.hand.remove(card)
        self.active_player.my_deck.in_play.append(card)
        if card.is_attack:
            self.process_card_actions(card.actions, None)
            self.process_attack(card.additional_action)
        else:
            self.process_card_actions(card.actions, card.additional_action)

    def buy_card(self, card):
        for_sale = self.shop.supply
        if for_sale[card.name][1] != 0:
            for_sale[card.name][1] -= 1
            if for_sale[card.name][1] == 0:
                self.shop.empty_piles += 1
        if card.name == 'province':
            if for_sale['province'][1] == 0:
                self.game_over = True
    
    def trash_card(self, card):
        self.active_player.my_deck.hand.remove(card)
        self.trash += [card]

    def gain_to_hand(self, card):
        self.active_player.my_deck.hand += [card]


    def process_card_actions(self, actions, additional_action):
        for x in actions:
            actual_action = basic_action_regex.match(x)
            amount = int(actual_action.group(1))
            act_type = actual_action.group(2)
            if act_type == 'Card' or act_type == 'Cards':
                self.active_player.my_deck.draw(amount)
            elif act_type == 'Buy' or act_type == 'Buys':
                self.active_player.buys += amount
            elif act_type == 'Action' or act_type == 'Actions':
                self.active_player.actions += amount
            elif act_type == 'Coin' or act_type == 'Coins':
                self.active_player.coins += amount
        if additional_action != None:
            additional_action(self)

    def process_reaction(self, react_fn):
        return react_fn(self)
        #reactions return True if they negate the attack completely

    def process_attack(self, attack_fn):
        for x in self.players:
            reactions = x.my_deck.get_reactions_in_hand()
            blocked = False
            if reactions != None:
                for y in reactions:
                    if self.process_reaction(y.reaction):
                        blocked = True
            if not blocked:
                attack_fn(self, x)
    
    def next_turn(self):
        self.active_player.cleanup()
        if(self.empty_piles_needed <= self.shop.empty_piles):
            self.game_over = True
        if self.game_over == True:
            return True
        else:
            self.active_player_number = (self.active_player_number + 1) % self.num_players
            self.active_player = self.players[self.active_player_number]
            return False
    



class Shop:
    def __init__(self, my_reset_fn):
        self.reset_fn = my_reset_fn
        self.supply = self.reset_fn()
        self.empty_piles = 0

    def get_cards_under_amount(self, amount):
        cards_under_amount = []
        for x in self.supply:
            if self.supply[x][1] > 0:
                if self.supply[x][0].cost <= amount:
                    cards_under_amount += [self.supply[x][0]]
        return cards_under_amount
    
    def reset_shop(self):
        self.reset_fn()


class Card:
    def __init__(self, my_base_actions, my_cost, my_pts, my_worth, my_additional_action, _is_attack, _is_reaction, my_reaction, my_name):
        self.actions = my_base_actions
        self.cost = my_cost
        self.pts = my_pts
        self.worth = my_worth
        self.additional_action = my_additional_action
        self.is_attack = _is_attack
        self.is_reaction = _is_reaction
        self.reaction = my_reaction
        self.name = my_name

class Player:
    def __init__(self, starting_deck, my_name, my_ai):
        self.my_deck = copy.deepcopy(starting_deck)
        self.name = my_name
        self.actions = 1
        self.buys = 1
        self.coins = 0
        self.game = None
        self.ai = my_ai

    def count_points(self):
        total_points = 0
        all_cards = self.my_deck.hand + self.my_deck.discard_pile + self.my_deck.draw_pile
        for x in all_cards:
            total_points += x.pts
        return total_points
    
    def join_game(self, game_to_join):
        self.game = game_to_join

    def play_actions(self, action_cards):
        if self.actions > 0 and action_cards != None:
            action_to_play = self.ai.action_fn(self.my_deck, action_cards)
            if action_to_play.name != 'error': 
                self.game.play_card(action_to_play)
                self.actions -= 1
                self.play_actions(action_cards.remove(action_to_play))
    
    def buy_cards(self):
        self.coins += self.my_deck.calc_hand_value()
        if self.buys > 0:
            card_to_buy = self.ai.buy_fn(self.game.shop, self.my_deck, self.coins)
            if card_to_buy.name != 'error':
                self.game.buy_card(card_to_buy)
                self.coins -= card_to_buy.cost
                self.buys -= 1
                self.my_deck.discard_pile += [card_to_buy]
                self.buy_cards()

    def choose_card_to_discard(self):
        self.my_deck.discard(self.ai.discard_fn(self.my_deck))
        
    def cleanup(self):
        self.my_deck.cleanup_deck_actions()
        self.actions = 1
        self.buys = 1
        self.coins = 0

class Deck:
    def __init__(self, my_cards):
        self.cards = my_cards
        self.draw_pile = self.cards
        self.discard_pile = []
        self.hand = []
        self.in_play = []

    def shuffle(self):
        random.shuffle(self.discard_pile)
        self.draw_pile = self.draw_pile + self.discard_pile
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
            if self.draw_pile == []:
                print('tried to draw from empty deck')
                
            else:
                self.hand += [self.draw_pile.pop()]
            
    def discard(self, card):
        self.hand.remove(card)
        self.discard_pile += [card]

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
                my_hand_actions += [x]
        return my_hand_actions

    def get_reactions_in_hand(self):
        my_hand_reactions = []
        for x in self.hand:
            if x.is_reaction:
                my_hand_reactions += [x]
        return my_hand_reactions

    def get_all_card_names(self):
        card_names = []
        for x in self.hand + self.draw_pile + self.discard_pile:
            card_names += [x.name]
        return card_names






####### GAME CARDS (& thier additonal actions) ###########
class ImaginaryCard(Card):
    def __init__(self):
        super().__init__(None, 0, 0, 0, None, False, False, None, 'error')

class Copper(Card):
    def __init__(self):
        super().__init__(None, 0, 0, 1, None, False, False, None, 'copper')

class Silver(Card):
    def __init__(self):
        super().__init__(None, 3, 0, 2, None, False, False, None, 'silver')

class Gold(Card):
    def __init__(self):
        super().__init__(None, 6, 0, 3, None, False, False, None, 'gold')

class Curse(Card):
    def __init__(self):
        super().__init__(None, 0, -1, 0, None, False, False, None, 'curse')

class Estate(Card):
    def __init__(self):
        super().__init__(None, 2, 1, 0, None, False, False, None, 'estate')

class Duchy(Card):
    def __init__(self):
        super().__init__(None, 5, 3, 0, None, False, False, None, 'duchy')

class Province(Card):
    def __init__(self):
        super().__init__(None, 8, 6, 0, None, False, False, None, 'province')

def cellar_action(my_game):
    cur_player = my_game.active_player
    cards_to_discard = []
    targ_card = my_game.active_player.ai.discard_option_fn(cur_player.my_deck)
    while targ_card.name != 'error':
        cards_to_discard += [targ_card]
        cur_player.my_deck.discard(targ_card)
        targ_card = my_game.active_player.ai.discard_option_fn(cur_player.my_deck)
    cur_player.my_deck.draw(len(cards_to_discard))

class Cellar(Card):
    def __init__(self):
        super().__init__(['+1 Action'], 2, 0, 0, cellar_action, False, False, None, 'cellar')

class Market(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+1 Action', '+1 Buy', '+1 Coin'], 5, 0, 0, None, False, False, None, 'market')

def merchant_action(my_game):
    cur_player = my_game.active_player
    if Silver in cur_player.my_deck.hand:
        my_game.process_card_actions(['+1 Coin'], None)

class Merchant(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+1 Action'], 3, 0, 0, merchant_action, False, False, None, 'merchant')

def militia_action(my_game, target_player):
    while len(target_player.my_deck.hand) > 3:
        target_player.choose_card_to_discard()

class Militia(Card):
    def __init__(self):
        super().__init__(['+2 Coins'], 4, 0, 0, militia_action, True, False, None, 'militia')

def mine_action(my_game):
    card_to_trash = my_game.active_player.ai.trash_for_treasure_fn(my_game.shop, my_game.active_player.my_deck, my_game.active_player.coins)
    
    if card_to_trash.name != 'error':
        my_game.trash_card(card_to_trash)
        card_to_gain = my_game.active_player.ai.gain_fn(my_game.shop, my_game.active_player.my_deck, card_to_trash.cost + 3)
        my_game.gain_to_hand(card_to_gain)

class Mine(Card):
    def __init__(self):
        super().__init__([], 5, 0, 0, mine_action, False, False, None, 'mine')

def moat_reaction(my_game):
    return True

class Moat(Card):
    def __init__(self):
        super().__init__(['+2 Cards'], 2, 0, 0, None, False, True, moat_reaction, 'moat')
        
def remodel_action(my_game):
    card_to_trash = my_game.active_player.ai.trash_fn(my_game.shop, my_game.active_player.my_deck, my_game.active_player.coins)
    my_game.trash_card(card_to_trash)
    card_to_gain =  my_game.active_player.ai.gain_fn(my_game.shop, my_game.active_player.my_deck, card_to_trash.cost + 2)
    my_game.gain_to_hand(card_to_gain)

class Remodel(Card):
    def __init__(self):
        super().__init__([], 4, 0, 0, remodel_action, False, False, None, 'remodel')

class Smithy(Card):
    def __init__(self):
        super().__init__(['+3 Cards'], 4, 0, 0, None, False, False, None, 'smithy')

class Village(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+2 Actions'], 3, 0, 0 , None, False, False, None, 'village')

def workshop_action(my_game):
    card_to_gain =  my_game.active_player.ai.gain_fn(my_game.shop, my_game.active_player.my_deck, 4)
    my_game.gain_to_hand(card_to_gain)

class Workshop(Card):
    def __init__(self):
        super().__init__([], 3, 0, 0, workshop_action, False, False, None, 'workshop')
#####################################################
