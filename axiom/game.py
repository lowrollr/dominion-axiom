
import random
import re
import copy
import math



# Regex Definitions:

basic_action_regex = re.compile("^\+(.) (.*)$")

# -/


# Helper Functions:

def card_action_regex(action): #process basic card action text
        actual_action = basic_action_regex.match(action)
        amount = int(actual_action.group(1))
        act_type = actual_action.group(2)
        #ex: "+2 Cards" -> 2, 'Cards'
        return (act_type, amount)

def card_in_list(card, list_of_cards): #is a card in a given list of cards
    for x in list_of_cards:
        #its necessary to compare types because we are comparing class instances
        if type(x) is type(card):
            return True
    return False

# -/

# Game Classes:

class Game: #manages everything relating to the game itself, contains instances of all other classes 
    def __init__(self, my_players, my_shop): #pass in a list of initialized players and an initialized shop
        self.players = my_players
        self.num_players = len(self.players)
        #trash pile starts empty
        self.trash = []
        #first player in list gets to go first
        self.active_player = self.players[0]
        self.active_player_number = 0
        self.shop = my_shop
        #flag that is updated to True when a game-ending condition occurs
        self.game_over = False
        #How many empty piles are needed in the shop to end the game
        self.empty_piles_needed = 3

    def play_card(self, card): #manages changing the game state to reflect a player playing a card
        #remove the card from the players hand and put it in play
        self.active_player.my_deck.hand.remove(card)
        self.active_player.my_deck.in_play.append(card)
        #if the card is an attack card, we need to process it's attack function
        if card.is_attack:
            self.process_card_actions(card.actions, card.additional_action)
            self.process_attack(card.attack_fn)
        else:
            #process the card's action text
            self.process_card_actions(card.actions, card.additional_action)

    def buy_card(self, card): #manage changing the game state to reflect a player buying a card
        #get the cards currently in the shops supply 
        for_sale = self.shop.supply
        #if the card is available (if it is passed to this function it should ALWAYS be), subtract 1 from its quantity
        if for_sale[card.name][1]:
            for_sale[card.name][1] -= 1
            #if there are no more cards of that type available after subtracting 1 from its quantity,
            #increse the empty piles counter by 1
            if not for_sale[card.name][1]:
                self.shop.empty_piles += 1
        #province is a special case, since as soon as provinces are depleted the game ends
        if card.name == 'province':
            if not for_sale['province'][1]:
                #set the game_over flag to reflect that a game-ending condition has been met
                self.game_over = True
    
    def trash_card(self, card): #manage changing the game state to reflect a player trashing a card
        #remove the given card from the active player's hand and put it in the trash pile
        self.active_player.my_deck.hand.remove(card)
        self.trash += [card]

    def gain_to_hand(self, card): #manage changing the game state to reflect a player gaining a card to their hand
        self.active_player.my_deck.hand += [card]

    def gain(self, card): #manage changing the game state to reflect a player gaining a card to their dicard pile
        self.active_player.my_deck.discard_pile += [card]

    def process_card_actions(self, actions, additional_action): #process card text -> execute corresponding game actions
        # look at each basic action within a card's text 
        for x in actions:
            #for basic actions, process the card text using regex
            action_processed = card_action_regex(x)
            action_text = action_processed[0]
            action_amnt = action_processed[1]
            #match the card text with a basic game action
            if action_text == 'Card' or action_text == 'Cards':
                self.active_player.my_deck.draw(action_amnt)
            elif action_text == 'Buy' or action_text == 'Buys':
                self.active_player.buys += action_amnt
            elif action_text == 'Action' or action_text == 'Actions':
                self.active_player.actions += action_amnt
            elif action_text == 'Coin' or action_text == 'Coins':
                self.active_player.coins += action_amnt
        #if there is an additional action function for this card, call it
        if additional_action != None:
            additional_action(self)

    def process_reaction(self, react_fn):
        return react_fn(self)
        #reactions return True if they negate the attack completely

    def process_attack(self, attack_fn):
        for x in self.players:
            if x != self.active_player:
                reactions = x.my_deck.get_reactions_in_hand()
                blocked = False
                
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
            for x in self.players:
                for y in x.my_deck.get_all_cards():
                    y.update(x)
            return True
        else:
            self.active_player_number = (self.active_player_number + 1) % self.num_players
            self.active_player = self.players[self.active_player_number]
            return False
    



class Shop:
    def __init__(self, supply_dict):
        self.def_supply = supply_dict
        self.supply = copy.deepcopy(self.def_supply)
        self.empty_piles = 0

    def get_cards_under_amount(self, amount):
        cards_under_amount = []
        for x in self.supply:
            if self.supply[x][1] > 0:
                if self.supply[x][0].cost <= amount:
                    cards_under_amount += [self.supply[x][0]]
        return cards_under_amount
    
    def reset_shop(self):
        self.supply = copy.deepcopy(self.def_supply)


class Card:
    def __init__(self, my_base_actions, my_cost, my_pts, my_worth, my_additional_action, _is_attack, my_attack_fn, _is_reaction, my_reaction, my_name):
        self.actions = my_base_actions
        self.cost = my_cost
        self.pts = my_pts
        self.worth = my_worth
        self.additional_action = my_additional_action
        self.is_attack = _is_attack
        self.attack_fn = my_attack_fn
        self.is_reaction = _is_reaction
        self.reaction = my_reaction
        self.name = my_name
    
    def update(self, my_player):
        pass

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
            action_to_play = self.ai.action_fn(self.game, self, None, True)
            if action_to_play.name != 'error': 
                self.game.play_card(action_to_play)
                self.actions -= 1
                self.play_actions(action_cards.remove(action_to_play))
    
    def buy_cards(self):
        self.coins += self.my_deck.calc_hand_value()
        if self.buys > 0:
            card_to_buy = self.ai.buy_fn(self.game, self, None, True)
            if card_to_buy.name != 'error':
                self.game.buy_card(card_to_buy)
                self.coins -= card_to_buy.cost
                self.buys -= 1
                self.my_deck.discard_pile += [card_to_buy]
                self.buy_cards()

    def choose_card_to_discard(self):
        self.my_deck.discard(self.ai.discard_fn(self.game, self, None, False))
        
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

    def get_all_cards(self):
        return self.draw_pile + self.discard_pile + self.hand + self.in_play

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
        for i in range(amnt):
            if self.draw_pile == []:
                self.shuffle()
            else:
                self.hand += [self.draw_pile.pop()]
            
    def discard(self, card):
        self.hand.remove(card)
        self.discard_pile += [card]

    def place(self, card, offset):
        self.draw_pile.insert(offset, card)

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


# -/




# Game Cards & their corresponding actions

class ImaginaryCard(Card):
    def __init__(self):
        super().__init__(None, 0, 0, 0, None, False, None, False, None, 'error')

class Copper(Card):
    def __init__(self):
        super().__init__(None, 0, 0, 1, None, False, None, False, None, 'copper')

class Silver(Card):
    def __init__(self):
        super().__init__(None, 3, 0, 2, None, False, None, False, None, 'silver')

class Gold(Card):
    def __init__(self):
        super().__init__(None, 6, 0, 3, None, False, None, False, None, 'gold')

class Curse(Card):
    def __init__(self):
        super().__init__(None, 0, -1, 0, None, False, None, False, None, 'curse')

class Estate(Card):
    def __init__(self):
        super().__init__(None, 2, 1, 0, None, False, None, False, None, 'estate')

class Duchy(Card):
    def __init__(self):
        super().__init__(None, 5, 3, 0, None, False, None, False, None, 'duchy')

class Province(Card):
    def __init__(self):
        super().__init__(None, 8, 6, 0, None, False, None, False, None, 'province')

def cellar_action(my_game):
    cur_player = my_game.active_player
    cards_to_discard = []
    targ_card = my_game.active_player.ai.discard_fn(my_game, my_game.active_player, None, True)
    while targ_card.name != 'error':
        cards_to_discard += [targ_card]
        cur_player.my_deck.discard(targ_card)
        targ_card = my_game.active_player.ai.discard_fn(my_game, my_game.active_player, None, True)
    cur_player.my_deck.draw(len(cards_to_discard))

class Cellar(Card):
    def __init__(self):
        super().__init__(['+1 Action'], 2, 0, 0, cellar_action, False, None, False, None, 'cellar')

class Market(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+1 Action', '+1 Buy', '+1 Coin'], 5, 0, 0, None, False, None, False, None, 'market')

def merchant_action(my_game):
    cur_player = my_game.active_player
    if Silver in cur_player.my_deck.hand:
        my_game.process_card_actions(['+1 Coin'], None)

class Merchant(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+1 Action'], 3, 0, 0, merchant_action, False, None, False, None, 'merchant')

def militia_attack(my_game, target_player):
    while len(target_player.my_deck.hand) > 3:
        target_player.choose_card_to_discard()

class Militia(Card):
    def __init__(self):
        super().__init__(['+2 Coins'], 4, 0, 0, None, True, militia_attack, False, None, 'militia')

def mine_stip(cards):
    filtered = []
    for x in cards:
        if x.worth:
            filtered += [x]
    return filtered

def mine_action(my_game):
    card_to_trash = my_game.active_player.ai.trash_fn(my_game, my_game.active_player, mine_stip, False)
    
    if card_to_trash.name != 'error':
        my_game.trash_card(card_to_trash)
        card_to_gain = my_game.active_player.ai.gain_fn(my_game, my_game.active_player, mine_stip, False)
        my_game.gain_to_hand(card_to_gain)

class Mine(Card):
    def __init__(self):
        super().__init__([], 5, 0, 0, mine_action, False, None, False, None, 'mine')

def moat_reaction(my_game):
    return True

class Moat(Card):
    def __init__(self):
        super().__init__(['+2 Cards'], 2, 0, 0, None, False, None, True, moat_reaction, 'moat')



def remodel_action(my_game):
    card_to_trash = my_game.active_player.ai.trash_fn(my_game, my_game.active_player, None, False)
    my_game.trash_card(card_to_trash)
    def remodel_stip(cards):
        filtered = []
        for x in cards:
            if x.cost <= card_to_trash.cost + 2:
                filtered += [x]
        return filtered
    card_to_gain =  my_game.active_player.ai.gain_fn(my_game, my_game.active_player, remodel_stip, False)
    my_game.gain(card_to_gain)

class Remodel(Card):
    def __init__(self):
        super().__init__([], 4, 0, 0, remodel_action, False, None, False, None, 'remodel')

class Smithy(Card):
    def __init__(self):
        super().__init__(['+3 Cards'], 4, 0, 0, None, False, None, False, None, 'smithy')

class Village(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+2 Actions'], 3, 0, 0 , None, False, None, False, None, 'village')

def workshop_action(my_game):
    def workshop_stip(cards):
        filtered = []
        for x in cards:
            if x.cost <= 4:
                filtered += [x]
        return filtered
    card_to_gain =  my_game.active_player.ai.gain_fn(my_game, my_game.active_player, workshop_stip, False)
    my_game.gain(card_to_gain)

class Workshop(Card):
    def __init__(self):
        super().__init__([], 3, 0, 0, workshop_action, False, None, False, None, 'workshop')

def artisan_action(my_game):
    def artisan_stip(cards):
        filtered = []
        for x in cards:
            if x.cost <= 5:
                filtered += [x]
        return filtered
    card_to_gain =  my_game.active_player.ai.gain_fn(my_game, my_game.active_player, artisan_stip, False)
    my_game.gain_to_hand(card_to_gain)
    my_game.active_player.my_deck.place(my_game.active_player.ai.put_on_top_fn(my_game, my_game.active_player, None, False))

class Artisan(Card):
    def __init__(self):
        super().__init__([], 6, 0, 0, artisan_action, False, None, False, None, 'artisan')

def bandit_action(my_game):
    my_game.gain(Gold())

def bandit_attack(my_game, target_player):
    for x in range(2):
        if target_player.my_deck.draw_pile != []:
            targ_card = target_player.my_deck.draw_pile.pop()
            if targ_card.worth:
                my_game.trash += [targ_card]
            else:
                target_player.my_deck.discard_pile += [targ_card]

class Bandit(Card):
    def __init__(self):
        super().__init__([], 5, 0, 0, bandit_action, True, bandit_attack, False, None, 'bandit')

def bureaucrat_action(my_game):
    my_game.active_player.my_deck.draw_pile.insert(0, Silver())

def bureacrat_attack(my_game, target_player):
    for x in target_player.my_deck.hand:
        #might want to make this an ai scheme action
        if x.pts:
            target_player.my_deck.hand.remove(x)
            target_player.my_deck.draw_pile.insert(0, x)
            break

class Bureaucrat(Card):
    def __init__(self):
        super().__init__([], 4, 0, 0, bureaucrat_action, True, bureacrat_attack, False, None, 'bureaucrat')

def chapel_action(my_game):
    for x in len(4):
        card_to_trash = my_game.active_player.ai.trash_fn(my_game, my_game.active_player, None, True)
        my_game.trash_card(card_to_trash)

class Chapel(Card):
    def __init__(self):
        super().__init__([], 2, 0, 0, chapel_action, False, None, False, None, 'chapel')

def council_room_action(my_game):
    for x in my_game.players:
        if x != my_game.active_player:
            x.my_deck.draw(1)

class Council_Room(Card):
    def __init__(self):
        super().__init__(['+4 Cards', '+1 Buy'], 5, 0, 0, council_room_action, False, None, False, None, 'council-room')

class Festival(Card):
    def __init__(self):
        super().__init__(['+2 Actions', '+1 Buy', '+2 Coins'], 5, 0, 0, None, False, None, False, None, 'festival')

class Gardens(Card):
    def __init__(self):
        super().__init__([], 4, -1, 0, None, False, None, False, None, 'gardens')

    def update(self, my_player):
        amnt = len(my_player.my_deck.get_all_cards())
        self.pts = math.floor(float(amnt)/10)

class Laboratory(Card):
    def __init__(self):
        super().__init__(['+2 Cards', '+1 Action'], 5, 0, 0, None, False, None, False, None, 'laboratory')

# -/
