import random
import re
import copy
import importlib
import inspect
import csv

from game import *
from ai_plugins.dominion_ai import AI

ai_types = set()

def import_AI(ai_name):
    try:
        module = importlib.import_module('ai_plugins.{0}'.format(ai_name))
        for x in dir(module):
            obj = getattr(module, x)
            if inspect.isclass(obj) and issubclass(obj, AI) and obj is not AI:
                return obj
            elif ai_name == 'dominion_ai' and inspect.isclass(obj):
                return obj
                
    except ImportError:
        print('ERROR: failed to import AI module "' + ai_name + '". Make sure "'+ ai_name + '.py" is present in the "ai_plugins" directory and has no syntax errors')
        exit()

def import_deck(deck_name):
    try:
        deck_file = open('./axiom/deck_presets/' + deck_name + '.deck', 'r')
    except FileNotFoundError:
        print('ERROR: failed to find deck file: ' + deck_name + '.deck')
        exit()
    starting_cards = []
    for elem in deck_file:
        elem_split = elem.split(' ')
        card_amnt = elem_split[0]
        card_name = elem_split[1].rstrip()
        card = eval(card_name.title() + '()')
        for x in range(0, int(card_amnt)):
            starting_cards += [card]
    deck_file.close()
    return Deck(starting_cards)
    

def import_shop(shop_name):
    try:
        shop_file = open('./axiom/shop_presets/' + shop_name + '.shop', 'r')
    except:
        print('ERROR: failed to find shop file: ' + shop_name + '.shop')
        exit()
    shop_contents = {}
    for elem in shop_file:
        elem_split = elem.split(' ')
        card_amnt = elem_split[0]
        card_name = elem_split[1].rstrip()
        shop_contents[card_name] = [eval(card_name.title() + '()'), int(card_amnt)]
    shop_file.close()
    return shop_contents

def start_game(num_players, player_types, deck_preset, shop_preset):
    global ai_types
    game_players = []
    for x in range(num_players):
        ai_type = import_AI(player_types[x])
        if ai_type:
            game_players += [Player(copy.deepcopy(import_deck(deck_preset)), 'player' + str(x), ai_type(str(ai_type).split('.')[1]))]          
            ai_types.add(str(ai_type).split('.')[1])
    game_shop = Shop(import_shop(shop_preset))
    my_game = Game(game_players, game_shop)
    return my_game

def simulate_games(num_players, player_types, num_games, deck_preset, shop_preset):
    ai_scores = []
    for i in range(num_games):
        if i%50 == 0 and i != 0:
            print('simulated ' + str(i) + ' games so far...')

        game = start_game(num_players, player_types, deck_preset, shop_preset)
        if not i:
            global ai_types
            for x in ai_types:
                ai_scores += [[x, []]]
        for x in game.players:
            x.join_game(game)
            random.shuffle(x.my_deck.draw_pile)
            x.my_deck.draw(5)
        while not game.game_over:
            game.active_player.play_actions(game.active_player.my_deck.get_actions_in_hand())
            game.active_player.buy_cards()
            game.next_turn()

        for x in ai_scores:
            for y in game.players:
                if y.ai.name == x[0]:
                    x[1] += [[y.count_points(), y.my_deck.get_all_card_names()]]
        # for x in game.players:
        #     if x.ai.name == 'miser':
        #         miser_decks += [[x.count_points(), x.my_deck.get_all_card_names()]]
        #     elif x.ai.name == 'common-sense':
        #         common_sense_decks += [[x.count_points(), x.my_deck.get_all_card_names()]]
        #     elif x.ai.name == 'dominion_ai':
        #         randomania_decks += [[x.count_points(), x.my_deck.get_all_card_names()]]
        
    for x in ai_scores:
        x = [x[0], x[1].sort()]

    ai_sums = []
    for x in ai_scores:
        ai_sums += [0]
        for y in range(len(x[1])):
            ai_sums[-1] += x[1][y][0]
        print(str(x[0] + " average score = " + str(ai_sums[-1]/len(x[1]))))

    
            
    # miser_sum = 0
    # common_sense_sum = 0
    # randomania_sum = 0
    # for x in range(len(randomania_decks)):
    #     randomania_sum += randomania_decks[x][0]

    # for x in range(len(common_sense_decks)):
    #     common_sense_sum += common_sense_decks[x][0]

    # for x in range(len(miser_decks)):
    #     miser_sum += miser_decks[x][0]

    # if len(miser_decks) != 0:
    #     print('Miser Avg. Score = ' + str(miser_sum/len(miser_decks)))
    # if len(common_sense_decks) != 0:
    #     print('Common_Sense Avg. Score = ' + str(common_sense_sum/len(common_sense_decks)))
    # if len(randomania_decks) != 0:
    #     print('Randomania Avg. Score = ' + str(randomania_sum/len(randomania_decks)))