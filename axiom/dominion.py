import random
import re
import copy
import importlib
import inspect
import csv

from game import *
from ai_plugins.dominion_ai import AI

#keeps track of ai_types being used during simulation
ai_types = set()

def import_AI(ai_name): #import an AI scheme defined by the user at runtime
    try:
        #use importlib to load the module with the given name
        module = importlib.import_module('ai_plugins.{0}'.format(ai_name))
        for x in dir(module):
            #get the AI subclass inside of the given file
            obj = getattr(module, x)
            #check if it's a subclass of AI
            if inspect.isclass(obj) and issubclass(obj, AI) and obj is not AI:
                return obj
            #or if it's the AI class itself
            elif ai_name == 'dominion_ai' and inspect.isclass(obj):
                return obj

    except ImportError: #this will be thrown if the name the user specifies does not correspond to an ai_plugin
        print('ERROR: failed to import AI module "' + ai_name + '". Make sure "'+ ai_name + '.py" is present in the "ai_plugins" directory and has no syntax errors')
        exit()

def import_deck(deck_name): #load a deck preset specified by the user at runtime
    try:
        #attempt to open the file specified
        deck_file = open('./axiom/deck_presets/' + deck_name + '.deck', 'r')
    except FileNotFoundError: #this is thrown if the file specified does not exist
        print('ERROR: failed to find deck file: ' + deck_name + '.deck')
        exit()
    starting_cards = []
    #parse the .deck file and construct a list of cards
    for elem in deck_file:
        elem_split = elem.split(' ')
        card_amnt = elem_split[0]
        card_name = elem_split[1].rstrip()
        card = eval(card_name.title() + '()')
        for x in range(0, int(card_amnt)):
            starting_cards.append(card)
    deck_file.close()
    #return a Deck object containing the cards specified in the deck preset file
    return Deck(starting_cards)
    

def import_shop(shop_name): #load a shop preset specified by the 
    try:
        #attempt to open the file specified
        shop_file = open('./axiom/shop_presets/' + shop_name + '.shop', 'r')
    except: #this is thrown if the file specified does not exist
        print('ERROR: failed to find shop file: ' + shop_name + '.shop')
        exit()
    #init shop_contents dictionary
    shop_contents = {}
    #parse file to load shop items into dictionary
    for elem in shop_file:
        elem_split = elem.split(' ')
        card_amnt = elem_split[0]
        card_name = elem_split[1].rstrip()
        shop_contents[card_name] = [eval(card_name.title() + '()'), int(card_amnt)]
    shop_file.close()
    #return shop_contents dictionary to be passed to Shop init fn
    return shop_contents

def start_game(num_players, player_types, deck_preset, shop_preset): #start a single game of Dominion
    global ai_types
    game_players = []
    #initialize each game Player
    for x in range(num_players):
        #import the AI scheme for a given player
        ai_type = import_AI(player_types[x])
        if ai_type:
            #initialize Player with default starting deck, and imported AI scheme
            game_players.append(Player(copy.deepcopy(import_deck(deck_preset)), 'player' + str(x), ai_type(str(ai_type).split('.')[1])))    
            #add the AI scheme the Player is using to the ai_types set      
            ai_types.add(str(ai_type).split('.')[1])
    #initialize game Shop and import the shop preset used for this simulation
    game_shop = Shop(import_shop(shop_preset))
    #initialize a Game object with the players and shop that we just initialized
    my_game = Game(game_players, game_shop)
    return my_game

def simulate_games(num_players, player_types, num_games, deck_preset, shop_preset): #simulate a given number of games with a set of Player AI schemes and deck/shop presets
    #this will store decks for each AI scheme and corresponding scores
    ai_scores = []
    for i in range(num_games):
        #give console update every 50 games because large numbers of games simulated can take a while. This occurs every half second on my machine but YMMV
        if i%50 == 0 and i != 0:
            print('simulated ' + str(i) + ' games so far...')
        #start the game
        game = start_game(num_players, player_types, deck_preset, shop_preset)
        #if this is the first game, initialize the ai_scores list to keep track of scores/decks
        if not i:
            global ai_types
            for x in ai_types:
                ai_scores.append([x, []])
        #have each player in the game join and draw their starting hand after their deck is shuffled
        for x in game.players:
            x.join_game(game)
            random.shuffle(x.my_deck.draw_pile)
            x.my_deck.draw(5)
        #as long a game-ending condition has not been reached, keep having players take turns
        while not game.game_over:
            #action phase
            game.active_player.play_actions(game.active_player.my_deck.get_actions_in_hand())
            #buy phase
            game.active_player.buy_cards()
            #cleanup phase
            game.next_turn()
        #record Player's scores and decks
        for x in ai_scores:
            for y in game.players:
                if y.ai.name == x[0]:
                    x[1].append([y.count_points(), y.my_deck.get_all_card_names()])

    #sort the score/deck pairs for each AI scheme by highest score
    for x in ai_scores:
        x = [x[0], x[1].sort()]

    #sum up total scores for each AI scheme and report the average
    ai_sums = []
    for x in ai_scores:
        ai_sums.append(0)
        for y in range(len(x[1])):
            ai_sums[-1] += x[1][y][0]
        print(str(x[0] + " average score = " + str(ai_sums[-1]/len(x[1]))))
