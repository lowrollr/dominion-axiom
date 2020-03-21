# dominion-axiom
### What the heck is this?
dominion-axiom is a platform for users to implement and test their own AI to play the popular tabletop deck-building game Dominion.
### core-features of dominion-axiom include 
  * the ability to simulate a limitless amount of games and gain access to meaninful statistics
  * baseline AI schemes to compare your algorithms to
  * a complete game-engine with numerous cards implemented to test with
  * customizable game presets
  
  
## User Guide

### Getting Started
This tool requires that the user have Python3 installed on thier machine.

In order to run your first analysis of Dominion games, clone this repo, then input the following command into your command line of choice (within the dominion-axiom directory):
'''
python3 axiom <# of players> <player1 AI type> <player2 AI type> ... <playerN AI type> <# of games to play> <starting deck preset> <shop preset>
'''
For example, using the default deck and shop presets, simulating 10000 games with 4 players using the miser, common_sense, miser, and common_sense ai schemes, would look like this:
'''
python3 axiom 4 miser common_sense miser common_sense 1000 default default
'''
The output of the analysis will be printed to the console

