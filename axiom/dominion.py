import random
import re
import copy

from game import Card, Deck, Player, Shop, Game
from ai_plugins.randomania import Randomania
from ai_plugins.miser import Miser
from shop_presets import *
from deck_presets import *




def start_game(num_players):
    game_players = []
    for x in range(num_players):
        game_players += [Player(default_deck(), 'player' + str(x), Randomania)]
    game_shop = Shop(default_shop)
    my_game = Game(game_players, game_shop)
    return my_game



##########
scores_decks = []
for i in range(1000):
    
    game = start_game(4)


    for x in game.players:
        
        x.join_game(game)
        random.shuffle(x.my_deck.draw_pile)
        x.my_deck.draw(5)
    while not game.game_over:
        game.active_player.play_actions(game.active_player.my_deck.get_actions_in_hand())
        game.active_player.buy_cards()
        game.next_turn()
    for x in game.players:
        print(x.count_points())
        scores_decks += [[x.count_points(), x.my_deck.get_all_card_names()]]
    
    print(i)

scores_decks = sorted(scores_decks)
for x in range(1, 11):
    print(str(scores_decks[-x]))

