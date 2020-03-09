import sys
from dominion import simulate_games

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("invalid number of args, please try again")
    else:
        num_players = int(sys.argv[1])
        if len(sys.argv) != 3 + num_players:
            print("invalid number of args, please try again")
        else:
            player_types = []
            for x in range(num_players):
                player_types += [sys.argv[x+2]]
            num_games = int(sys.argv[2 + num_players])
            print("simulating " + str(num_games) + " games")
            simulate_games(num_players, player_types, num_games)