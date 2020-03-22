import sys
from dominion import simulate_games

if __name__ == '__main__':
    #check args to make sure they are correct
    if len(sys.argv) == 1:
        print("invalid number of args, please try again")
    else:
        #player types should make sense given the number of players
        num_players = int(sys.argv[1])
        print('# of players: ' + str(num_players))
        if len(sys.argv) != 5 + num_players:
            print("invalid number of args, please try again")
        else:
            player_types = []
            for x in range(num_players):
                player_types += [sys.argv[x+2]]
            num_games = int(sys.argv[2 + num_players])
            print("simulating " + str(num_games) + " games")
            deck_preset = sys.argv[3 + num_players]
            print("using deck preset: " + deck_preset)
            shop_preset = sys.argv[4 + num_players]
            print("using shop preset: " + shop_preset)
            #start the simulation
            simulate_games(num_players, player_types, num_games, deck_preset, shop_preset)