
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

    def process_attack(self, attack_fn): #process applying a card's attack to the attacker's opponets
        #apply the attack to each player who isn't the active player
        for x in self.players:
            if x != self.active_player:
                # get any reactions that the given player might have
                reactions = x.my_deck.get_reactions_in_hand()
                blocked = False
                #check if any of the reactions block the attack (not all reactions will block)
                for y in reactions:
                    if self.process_reaction(y.reaction):
                        blocked = True
                #if it isn't blocked, call the attack function targeting the given player
                if not blocked:
                    attack_fn(self, x)
    
    def next_turn(self): #manage changing the game state to reflect a turn transition
        #clean up any player related objects
        self.active_player.cleanup()
        #check if the empty_piles game-ending condition has been met
        if(self.empty_piles_needed <= self.shop.empty_piles):
            self.game_over = True
        #if the game is over, end the game and call the update function to process cards with a dynamic point total
        if self.game_over == True:
            for x in self.players:
                for y in x.my_deck.get_all_cards():
                    y.update(x)
            return True
        #if the game is not over, change the active player to be the next player
        else:
            self.active_player_number = (self.active_player_number + 1) % self.num_players
            self.active_player = self.players[self.active_player_number]
            return False
    



class Shop: #manages everything related exclusively to the game's shop
    def __init__(self, supply_dict): #pass in a dict containing the shop's starting configuration
        self.def_supply = supply_dict
        #copy the starting configuration into the shop's supply dict (we don't want to change the configuration itself)
        self.supply = copy.deepcopy(self.def_supply)
        #there are no empty piles when the game begins
        self.empty_piles = 0

    def get_cards_under_amount(self, amount): #get all cards less than or equal to a given amount of coins
        cards_under_amount = []
        for x in self.supply:
            #check if the card is still available
            if self.supply[x][1] > 0:
                #check if the card's cost is less than or equals to the given amount of coins
                if self.supply[x][0].cost <= amount:
                    cards_under_amount += [self.supply[x][0]]
        return cards_under_amount
    
    def reset_shop(self): #reset the shop to its starting configuration
        self.supply = copy.deepcopy(self.def_supply)


class Card: #superclass for a card, holds all the card's data
    def __init__(self, my_base_actions, my_cost, my_pts, my_worth, my_additional_action, _is_attack, my_attack_fn, _is_reaction, my_reaction, my_name):
        #elementary actions that don't need special processing
        self.actions = my_base_actions
        #cost to buy from the shop, in coins
        self.cost = my_cost
        #how many victory points the card is worth
        self.pts = my_pts
        #how many coins the card is worth (this will only be non-zero for treasure cards)
        self.worth = my_worth
        #a function defining the card's non basic actions
        self.additional_action = my_additional_action
        #if the card is an attack or not
        self.is_attack = _is_attack
        #a function defining the card's attack action
        self.attack_fn = my_attack_fn
        #if the card is a reaction or not
        self.is_reaction = _is_reaction
        #a function defining the card's triggered reaction
        self.reaction = my_reaction
        #a string holding the name of the card
        self.name = my_name
    
    def update(self, my_player): #some cards change as the game progresses, this function might be defined by a Card subclass if that is needed
        pass

class Player: #manages everything related exclusively to a specific player
    def __init__(self, starting_deck, my_name, my_ai):
        #a Deck object which will be initialized to be a copy of the game's defined deck preset
        self.my_deck = copy.deepcopy(starting_deck)
        #a string holding the player's name
        self.name = my_name
        #the amount of actions the player currently has for the turn
        self.actions = 1
        #the amount of buys the player has available for the turn
        self.buys = 1
        #the coins a player currently has available to buy things with
        self.coins = 0
        #the Game object that the player belongs to
        self.game = None
        #the ai scheme that the player will utilize
        self.ai = my_ai

    def count_points(self): #count and return the victory points in the player's deck
        total_points = 0
        #get all cards that the player currently has in their possession 
        all_cards = self.my_deck.hand + self.my_deck.discard_pile + self.my_deck.draw_pile
        #count the victory points of each card
        for x in all_cards:
            total_points += x.pts
        #return the total
        return total_points
    
    def join_game(self, game_to_join): #set the Game that the player belongs to
        self.game = game_to_join

    def play_actions(self, action_cards): #recursively process the player's action phase
        #check if the player is able to play an aciton
        if self.actions > 0 and action_cards != None:
            #pass control to the player's AI action decision function to determine which action to play
            action_to_play = self.ai.action_fn(self.game, self, None, True)
            #if the AI scheme has returned a valid card to pay
            if action_to_play.name != 'error': 
                #game processes playing the card
                self.game.play_card(action_to_play)
                #the player now has one less action to play this turn
                self.actions -= 1
                #play additoinal actions (if possible)
                self.play_actions(action_cards.remove(action_to_play))
    
    def buy_cards(self): #recursively process the player's buy phase
        #calculated the value of the player's hand (sum of all treasures' worth)
        self.coins += self.my_deck.calc_hand_value()
        #move the treasures to in_play so they aren't counted again
        self.move_treasures()
        #check if the player has buys remaining
        if self.buys > 0:
            #get the card that the AI scheme buy decision function determines should be bought
            card_to_buy = self.ai.buy_fn(self.game, self, None, True)
            #check if the card is valid
            if card_to_buy.name != 'error':
                #game processes buying the card
                self.game.buy_card(card_to_buy)
                #remove the coins that were spent
                self.coins -= card_to_buy.cost
                #decrease the amount of buys available this turn
                self.buys -= 1
                #place the bought card in the discard pile
                self.my_deck.discard_pile += [card_to_buy]
                #continue to buy cards (if possible)
                self.buy_cards()

    def move_treasures(self): #move treasures from the player's hand to the in_play zone
        my_treasures = []
        #get all treasures in the player's hand
        for x in self.my_deck.hand:
            if x.worth:
                my_treasures += [x]
        #move them to in_play
        for x in my_treasures:
            self.my_deck.hand.remove(x)
            self.my_deck.in_play.append(x)

    def choose_card_to_discard(self): #choose a card in hand to dicard (with help from the player's AI scheme) and discard it 
        self.my_deck.discard(self.ai.discard_fn(self.game, self, None, False))
        
    def cleanup(self): #process end of turn
        #call deck cleanup function
        self.my_deck.cleanup_deck_actions()
        #reset action, buy, and coin amounts
        self.actions = 1
        self.buys = 1
        self.coins = 0

class Deck: #manages everything related exclusively to a specific Deck
            #a deck defines all cards a player owns and each of the zones they exist within
    def __init__(self, my_cards): #pass a set of cards to initialize the deck with
        self.cards = my_cards
        #place all cards in the draw pile
        self.draw_pile = self.cards
        #initialize hand, dicard pile, and in_play zones to be empty
        self.discard_pile = []
        self.hand = []
        self.in_play = []

    def get_all_cards(self): #returna list containing all cards in all zones
        return self.draw_pile + self.discard_pile + self.hand + self.in_play

    def shuffle(self): #shuffle the discard pile into the draw pile, below the cards already in the draw pile
        #randomize the discard pile
        random.shuffle(self.discard_pile)
        #place the shuffled discard pile below the existing draw pile
        self.draw_pile = self.draw_pile + self.discard_pile
        #the discard pile should now be empty
        self.discard_pile = []

    def cleanup_deck_actions(self): #process cleanup actions related to the deck
        #move all cards in the player's hand and the in_play zone into the discard pile
        self.discard_pile = self.discard_pile + self.hand + self.in_play
        #the hand and in_play zone is now empty
        self.hand = []
        self.in_play = []
        #draw a new hand of 5 cards
        self.draw(5)

    def draw(self, amnt): #draw an amount of cards
        #process each draw
        for i in range(amnt):
            #if the draw pile is empty, shuffle the discard pile into the draw pile
            if self.draw_pile == []:
                self.shuffle()
            #if the draw pile is still empty a card can't be drawn!
            if self.draw_pile != []:
                #put the top card of the draw pile into the hand
                self.hand += [self.draw_pile.pop()]
            
    def discard(self, card): #discard a card
        #remove the card from the hand
        self.hand.remove(card)
        #place it in the discard pile
        self.discard_pile += [card]

    def place(self, card, offset): #place a card in a specific part of the deck (offset from top)
        self.draw_pile.insert(offset, card)

    def calc_hand_value(self): #calculate the value/worth of the hand
        total_value = 0
        #total the worth of each card
        for x in self.hand:
            total_value += x.worth
        return total_value
    
    def get_actions_in_hand(self): #get all action cards in a player's hand
        my_hand_actions = []
        for x in self.hand:
            if x.actions != None:
                my_hand_actions += [x]
        return my_hand_actions

    def get_reactions_in_hand(self): #get all reaction cards in a player's hand
        my_hand_reactions = []
        for x in self.hand:
            if x.is_reaction:
                my_hand_reactions += [x]
        return my_hand_reactions

    def get_all_card_names(self): #get the names of all cards in a player's deck
        card_names = []
        for x in self.hand + self.draw_pile + self.discard_pile:
            card_names += [x.name]
        return card_names


# -/




# Game Cards & their corresponding actions
# (implementations of specific Dominion cards)

class ImaginaryCard(Card): #this will be used to simulate choosing not to play a Card, returning this === choosing not to play a card
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

def cellar_action(my_game): #additional action text: "Discard any number of cards, then draw that many."
    #get the current/active player
    cur_player = my_game.active_player
    cards_to_discard = []
    #get the card that the player chooses to discard
    targ_card = my_game.active_player.ai.discard_fn(my_game, my_game.active_player, None, True)
    #keep discarding cards as long as the player keeps choosing to discard
    while targ_card.name != 'error':
        cards_to_discard += [targ_card]
        #discard the given card
        cur_player.my_deck.discard(targ_card)
        #get an additional card to discard
        targ_card = my_game.active_player.ai.discard_fn(my_game, my_game.active_player, None, True)
    #draw however many cards the player discarded
    cur_player.my_deck.draw(len(cards_to_discard))

class Cellar(Card):
    def __init__(self):
        super().__init__(['+1 Action'], 2, 0, 0, cellar_action, False, None, False, None, 'cellar')

class Market(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+1 Action', '+1 Buy', '+1 Coin'], 5, 0, 0, None, False, None, False, None, 'market')

def merchant_action(my_game): #additional action text: "The first time you play a Silver this turn, +1 Coin."
    #get the current/active player
    cur_player = my_game.active_player
    #if there is a Silver card in tthe player's hand, increase the players coins by 1
    if Silver in cur_player.my_deck.hand:
        my_game.process_card_actions(['+1 Coin'], None)

class Merchant(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+1 Action'], 3, 0, 0, merchant_action, False, None, False, None, 'merchant')

def militia_attack(my_game, target_player): #attack text: "Each other player discards down to 3 cards in his hand"
    #the targeted player chooses cards to discard until they have 3 cards in hand
    while len(target_player.my_deck.hand) > 3:
        target_player.choose_card_to_discard()

class Militia(Card):
    def __init__(self):
        super().__init__(['+2 Coins'], 4, 0, 0, None, True, militia_attack, False, None, 'militia')

def mine_stip(cards): #stipulation = card trashed must be a treasure
    filtered = []
    #get all treasures in the given list of carrds
    for x in cards:
        if x.worth:
            filtered += [x]
    return filtered

def mine_action(my_game): #additional action text: "Trash a Treasure card from your hand. Gain a Treasure card costing up to 3 more; put it into your hand."
    #get a valid card (treasure) to trash
    card_to_trash = my_game.active_player.ai.trash_fn(my_game, my_game.active_player, mine_stip, False)
    #check if the player chooses a card to trash
    if card_to_trash.name != 'error':
        #trash the card
        my_game.trash_card(card_to_trash)
        #gain a valid card (treasure) 
        card_to_gain = my_game.active_player.ai.gain_fn(my_game, my_game.active_player, mine_stip, False)
        #put the gained card into the player's hand
        my_game.gain_to_hand(card_to_gain)

class Mine(Card):
    def __init__(self):
        super().__init__([], 5, 0, 0, mine_action, False, None, False, None, 'mine')

def moat_reaction(my_game): #returns True to signal to the Game that the attack has been negated
    return True

class Moat(Card):
    def __init__(self):
        super().__init__(['+2 Cards'], 2, 0, 0, None, False, None, True, moat_reaction, 'moat')

def remodel_action(my_game): #additional action text: "Trash a card from your hand. Gain a card costing up to 2 more than the trashed card."
    #the player chooses a card to trash from their hand
    card_to_trash = my_game.active_player.ai.trash_fn(my_game, my_game.active_player, None, False)
    #trash the given card
    my_game.trash_card(card_to_trash)

    def remodel_stip(cards): #stipulation = cards under cost of card_to_trash + 2
        filtered = []
        #get all cards that fulfill the stipulation
        for x in cards:
            if x.cost <= card_to_trash.cost + 2:
                filtered += [x]
        return filtered
    #player chooses a card to gain out of the cards that fulfill the stipulation
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

def workshop_action(my_game): #additional action text: "Gain a card costing up to 4."
    def workshop_stip(cards): #get all cards that cost 4 or less
        filtered = []
        for x in cards:
            if x.cost <= 4:
                filtered += [x]
        return filtered
    #player chooses a card to gain that costs less than 4
    card_to_gain =  my_game.active_player.ai.gain_fn(my_game, my_game.active_player, workshop_stip, False)
    my_game.gain(card_to_gain)

class Workshop(Card):
    def __init__(self):
        super().__init__([], 3, 0, 0, workshop_action, False, None, False, None, 'workshop')

def artisan_action(my_game): #additional action text: "Gain a card to your hand costing up to 5. Put a card from your hand onto your deck."
    def artisan_stip(cards): #get all cards that cost 5 or less
        filtered = []
        for x in cards:
            if x.cost <= 5:
                filtered += [x]
        return filtered
    #player chooses a card to gain that costs 5 or less
    card_to_gain =  my_game.active_player.ai.gain_fn(my_game, my_game.active_player, artisan_stip, False)
    my_game.gain_to_hand(card_to_gain)
    #player chooses a card from their hand to put on top of their deck
    my_game.active_player.my_deck.place(my_game.active_player.ai.put_on_top_fn(my_game, my_game.active_player, None, False))

class Artisan(Card):
    def __init__(self):
        super().__init__([], 6, 0, 0, artisan_action, False, None, False, None, 'artisan')

def bandit_action(my_game): #additional action text: "Gain a Gold."
    my_game.gain(Gold())

def bandit_attack(my_game, target_player): #attack text: "Each other player reveals the top 2 cards of their deck, trashes a revealed treasure other than Copper, and discards the rest."
    #reveal 2 cards
    for x in range(2):
        #if there is a card on top to reveal
        if target_player.my_deck.draw_pile != []:
            #take the card off the top of the deck
            targ_card = target_player.my_deck.draw_pile.pop()
            #trash the card if it has worth (is a treasure) but is not a Copper
            if targ_card.worth and type(targ_card) != type(Copper()):
                #put the card in the trash pile
                my_game.trash += [targ_card]
            else:
                #if it doesn't fulfill the condition, instead put the card in the player's discard pile
                target_player.my_deck.discard_pile += [targ_card]

class Bandit(Card):
    def __init__(self):
        super().__init__([], 5, 0, 0, bandit_action, True, bandit_attack, False, None, 'bandit')

def bureaucrat_action(my_game): #additional action text: "Gain a Silver onto your deck."
    #put a silver card on top of the active player's deck
    my_game.active_player.my_deck.draw_pile.insert(0, Silver())

def bureacrat_attack(my_game, target_player): #attack text: "Each other player reveals a Victory card from their hand and puts it onto their deck (or reveals a hand with no Victory cards)."
    #check player's hand for cards worth points
    for x in target_player.my_deck.hand:
        #TODO: might want to make this an ai scheme action
        #if a card worth points is found, remove it from their hand, put it on top of the deck, and break out of the loop
        if x.pts:
            target_player.my_deck.hand.remove(x)
            target_player.my_deck.draw_pile.insert(0, x)
            break

class Bureaucrat(Card):
    def __init__(self):
        super().__init__([], 4, 0, 0, bureaucrat_action, True, bureacrat_attack, False, None, 'bureaucrat')

def chapel_action(my_game): #additional action text: "Trash up to 4 cards from your hand."
    #allow trashes to happen up to 4 times
    for x in len(4):
        #player optionally trashes a card
        card_to_trash = my_game.active_player.ai.trash_fn(my_game, my_game.active_player, None, True)
        my_game.trash_card(card_to_trash)

class Chapel(Card):
    def __init__(self):
        super().__init__([], 2, 0, 0, chapel_action, False, None, False, None, 'chapel')

def council_room_action(my_game): #additional action text: "Each other player draws a card"
    for x in my_game.players:
        #if the target player is not the active player, that player draws a card
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
    #card text: "Worth 1 Victory Point per 10 cards you have (rounded down)."
    def update(self, my_player): #update the points this card is worth in accordance to its text
        amnt = len(my_player.my_deck.get_all_cards())
        self.pts = math.floor(float(amnt)/10)

class Laboratory(Card):
    def __init__(self):
        super().__init__(['+2 Cards', '+1 Action'], 5, 0, 0, None, False, None, False, None, 'laboratory')

# -/
