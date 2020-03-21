# dominion-axiom
### What the heck is this?
dominion-axiom is a platform for users to implement and test their own AI to play the popular tabletop deck-building game Dominion. If you are unfamiliar with Dominion, a brief discussion of the game and its rules is on Wikipedia: https://en.wikipedia.org/wiki/Dominion_(card_game)

### core-features of dominion-axiom include 
  * the ability to simulate a limitless amount of games and gain access to meaninful statistics
  * baseline AI schemes to compare your algorithms to
  * a complete game-engine with numerous cards implemented to test with
  * customizable game presets
  
  
## User Guide

### Getting Started
This tool requires that the user have Python3 installed on thier machine.

In order to run your first analysis of Dominion games, clone this repo, then input the following command into your command line of choice (within the dominion-axiom directory):
```
python3 axiom <# of players> <player1 AI type> <player2 AI type> ... <playerN AI type> <# of games to play> <starting deck preset> <shop preset> 
```
For example, using the default deck and shop presets, simulating 10000 games with 4 players using the miser, common_sense, miser, and common_sense ai schemes, would look like this:
```
python3 axiom 4 miser common_sense miser common_sense 1000 default default
```
The output of the analysis will be printed to the console, and should look something like this:
```
......../dominion-axiom$ python3 axiom 4 miser common_sense miser common_sense 1000 default default
# of players: 4
simulating 1000 games
using deck preset: default
using shop preset: default
simulated 50 games so far...
simulated 100 games so far...
simulated 150 games so far...
simulated 200 games so far...
simulated 250 games so far...
simulated 300 games so far...
simulated 350 games so far...
simulated 400 games so far...
simulated 450 games so far...
simulated 500 games so far...
simulated 550 games so far...
simulated 600 games so far...
simulated 650 games so far...
simulated 700 games so far...
simulated 750 games so far...
simulated 800 games so far...
simulated 850 games so far...
simulated 900 games so far...
simulated 950 games so far...
common_sense average score = 30.6695
miser average score = 29.073
```
Your exact average scores should of course be slightly different.

### Using Custom Deck/Shop Presets
Within the axiom directory, there exist directories named `deck_presets` and `shop_presets`. Within these directories are `.deck` and `.shop` files respectively. Axiom supports the ability for users to use their own preset files during simulation. 

#### Creating a .deck File
A deck preset defines which cards exist in each player's deck when the game begins. In order to create a custom deck preset, create a file named `<whatever you want to name it>.deck` within the `axiom/deck_presets` directory and open it with your text-editor of choice.

The contents of these files are extremely straightforward. For example, the default file included, `default.deck` is simply written as:
```
7 copper
3 estate
```
This .deck file represents a starting deck with 7 'copper' cards and 3 'estate' cards. The general format for each line in a .deck file must be `<card amount> <card name>`. It's that easy!

#### Creating a .shop File
Similarly, creating a shop preset file is also pretty straightforward. A shop preset defines which cards are available in the game's shop (some call this the supply), as well as the amount of each cards available.

The default file included, `default.shop`, looks like this:

```
60 copper
40 silver
30 gold
30 curse
12 estate
12 duchy
12 province
10 cellar
10 market
10 merchant
10 militia
10 mine
10 moat
10 remodel
10 smithy
10 village
10 workshop
```
This file stipulates that the shop will have 60 'copper' cards available for sale, 40 'silver' cards, 30 'gold' cards, etc. The general format for each line must be `<card amount> <card name>`.

#### Using your custom preset file
Use command line arguments to utilize your custom preset file in simulation. For example, if you created `top_secret.deck` and `extra_fun.shop`, running the simulation with the following command would utilize those files:
```
python3 axiom 4 miser common_sense miser common_sense 1000 top_secret extra_fun
```
(also see the command line examples in the 'Getting Started' section)
