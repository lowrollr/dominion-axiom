# dominion-axiom
### What the heck is this?
dominion-axiom is a platform for users to implement and test their own AI to play the popular tabletop deck-building game Dominion. If you are unfamiliar with Dominion, a brief discussion of the game and its rules is on Wikipedia: https://en.wikipedia.org/wiki/Dominion_(card_game).

### core-features of dominion-axiom include 
  * the ability to simulate a limitless amount of games and gain access to meaninful statistics
  * baseline AI schemes to compare your algorithms to
  * a complete game-engine with numerous cards implemented to test with
  * customizable game presets
  
  
## User Guide

### Getting Started
This tool requires that the user have Python3 installed on their machine. This guide also assumes that the reader has played Dominion before and is familiar with the rules.

In order to run your first analysis of Dominion games, clone this repo, then input the following command into your command line of choice (within the dominion-axiom directory):
```
python3 axiom <# of players> <player1 AI type> <player2 AI type> ... <playerN AI type> <# of games to play> <starting deck preset> <shop preset> 
```
For example, using the default deck and shop presets, simulating 1000 games with 4 players using the miser, common_sense, miser, and common_sense ai schemes, would look like this:
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


### AI Schemes
The 'meat' of this platform is of course the ability to develop AI to play Dominion. In the context of this simulator, 'AI' is a collection of functions that broadly define all the decisions a player could make during the course of the game. I oftentimes refer to the collection of these functions as 'AI schemes'. Each AI scheme is defined within its own python file within the `axiom/ai_plugins` directory, and is a subclass of the superclass `AI` defined in `dominion_ai.py`. The `AI` superclass defines every decision point function (and works as an AI scheme on its own), so deprecated AI schemes will still work even if a new decision function is added later on. However, the functions defined in the `AI` superclass simply make all decisions randomly, so the resulting scores when using this scheme are very, very, very bad.

#### Getting Started Writing Your Own AI Scheme
I have included a script in the root directory called `new_ai.py` that will generate a skeleton with all the necessary functions you'll need to develop. In order to get started, run the command `python3 new_ai.py <your_ai_name>`. This will create a file within the `axiom/ai_plugins` directory called <your_ai_name>.py with everything you'll need to get started.

#### AI Scheme Decision Function Design
All decisions within Dominion boil down to choosing between different Cards. AI schemes decisions broadly define each of the different decisions within Dominion. At first one might think that there are a lot but there are only 6! (This could (and probably will) change as more cards are implemented within this platform).

To make development easier, AI scheme decision functions are universally defined with the same arguments. 

The universal format of these functions is as follows:
```python
def example_AI_fn(self, _game, _player, _stip, _optional):
```

`_game`: This is a Game object, which contains all the information concerning the Game, Players, Shop, etc. This is a large collection of information you can selectively pull from to inform your decisions.

`_player`: This is a Player object corresponding to the player who must make the given decision. Some cards in Dominion prompt actions for players other than the 'active player' (player who's turn it is currently), so it is necessary to pass this as an argument for that reason.

`_stip`: This is a stipulation (rule that must be followed when performing the decision) defined as a function. This function will always take a list of Card objects as an argument, and return a new list of Card objects. The returned list of Cards represents the Cards that are 'valid' for the given stipulation. To reiterate, a stipulation defines rules that MUST be followed. If there is no stipulation, this function will by default be defined as a function that simply returns the list that is given, so no cards are eliminated as options. This might be the most confusing concept of AI schemes, so here is an example:

A card might require that a player trash a Card with cost < 5. This is where the stipulation function comes in. In this case, the stipulation would be passed a set of cards (the player's hand) and return all the cards in that player's hand with cost < 5.

`_optional`: Always a boolean. This will be True if the decision is optional, and False if the decision is not optional. For example, if a Card action stated that a Player "may draw a card", then `_optional` would be True. If the card stated that a Player "draws a card", `_optional` would be False.

Because all Dominion decisions are choices between different cards, each decision function returns a Card object. This Card corresponds to the card that the player chooses for the given decision. If for some reason the Player does not choose a Card (if they are unable to or allowed to choose not to), a Card object subclass called ImaginaryCard is returned (see the miser example below). This is a signal to the game engine that no card was chosen.

There are currently 6 different functions that broadly define actions players can take in Dominion:

##### action_fn
This defines the player's choice to play an action from their hand during the Action phase. 
The actions in the player's hand must be passed to the stipulation function, which will return the actions that the player is able to play.
This function will return a Card object corresponding to the card that the player will choose to play.

##### discard_fn
This defines the player's choice to discard a card from their hand.
The cards in the player's hand must be passed to the stipulation function, which will return the cards that the player is able to discard.
This function will return a Card object corresponding to the card that the player will choose to discard.

##### buy_fn
This defines the player choosing a card to buy from the game's shop during the Buy phase.
This will involve choosing from the cards available in the shop that the player is able to afford with the coins in their hand.
The cards available in the shop must be passed to the stipulation function, which will return the cards that the player is able to purchase.
This function will return a Card object corresponding to the card that the player will purchase from the shop.

##### trash_fn
This defines the player choosing a card from their hand to put in the trash pile.
The cards in the player's hand must be passed to the stipulation function, which will return the cards that the player is able to put in the trash pile.
This function will return a Card object corresponding to the card that the player will choose to put in the trash pile.

##### gain_fn
This defines the player choosing a card to gain from the game's shop.
The cards available in the shop must be passed to the stipulatioon function, which will return the cards that the player is able to gain.
This function will return a Card object corresponding to the card that the player will gain from the shop.

##### put_on_top_fn
This defines the player choosing a card from their hand to put on top of their draw pile.
The cards in the player's hand must be passed to the stipulation function, which will return the cards that the players is able to put on top of their draw pile from their hand.
This function will return a Card object corresponding to the card that the player will put on top of their draw pile.

It is important to note that these functions don't actually perform any of the game mechanics that might be made after making one of these decisions, that is handled by the game engine!

##### Preprocessing
It is likely that you'll want to do some sort of preprocessing on the `_stip` and `_optional` arguments. For example, when the game engine passes control to a decision function and doesn't have any further stipulations, the agrument passed will be 'None'. You could of  course handle this case in each function, but it is oftentimes more efficient to abstract this handling to a different function. In the `AI` superclass, stipulations passed in as None are converted to functions that simply return the passed in argument during preprocessing. This superclass function is available for your use, or you can define your own!

The preprocessing function format:
```python
def process_decision_params(self, _stip, _optional):
   return new_stip, new_optional
```

##### Examples
This all might sound a little confusing, but maybe if I give an example it will be clearer!

The following is a function within the `miser` AI scheme, which is included as part of this platform:
``` python
def buy_fn(self, _game, _player, _stip, _optional):
        stip, optional_card = super().process_decision_params(_stip, _optional)
        cards_available = _game.shop.get_cards_under_amount(_player.coins)
        stip_cards = stip([Province(), Gold(), Silver()])
        list_of_cards = []
        for x in stip_cards:
            for y in cards_available:
                if type(x) is type(y):
                    list_of_cards += [x]

        if card_in_list(Province(), list_of_cards):
            return Province()
        elif card_in_list(Gold(), list_of_cards):
            return Gold()
        elif card_in_list(Silver(), list_of_cards):
            return Silver()
        else:
            if _optional:
                return ImaginaryCard()
            else:
                return random.choice(cards_available)
 ```
Let's walk through this line-by-line:
```python
stip, optional_card = super().process_decision_params(_stip, _optional)
```
First, we use the superclass preprocessing function to do necessary preprocessing on the stipulation and optional card arguments.
```python
cards_available = _game.shop.get_cards_under_amount(_player.coins)
```
Then, we define `cards_available` as a list of all the cards available in the shop that the player can afford with the coins they currently have (This is something you should always do in buy_fn).
```python
stip_cards = stip([Province(), Gold(), Silver()])
```
This particular AI scheme by definition is only interested in having a deck full of Silver, Gold, and Province cards, so those are the only cards we are interested in buying. This means that we want to apply our stipulation function to only these cards, since we aren't buying any others (If your algorithm considers all cards available in the shop, just apply the stipulation function to the list of cards available)
```python
list_of_cards = []
for x in stip_cards:
    for y in cards_available:
        if type(x) is type(y):
            list_of_cards += [x]
```
This simply defines list_of_cards as the list of cards that we are interested in buying, essentially the intersection of stip_cards and cards_available.
```python
if card_in_list(Province(), list_of_cards):
    return Province()
elif card_in_list(Gold(), list_of_cards):
    return Gold()
elif card_in_list(Silver(), list_of_cards):
    return Silver()
```
This algorithm prioritizes buying Provnices, then Gold, and finally Silver. The card_in_list is a helper function we obtain from `game.py` that returns whether or not a card is included in a list of cards (this is not as simple as `<card> in list` because we are comparing class instances, similarly to the for loop above). If the card we desire is available, we return an instance of it.
```python
else:
    if _optional:
        return ImaginaryCard()
    else:
        return random.choice(cards_available)
```
Finally, we handle the case where we can't buy any of the cards we desire. If buying a card is optional, we return an instance of an ImaginaryCard, which signals to the game engine that we are choosing to do nothing. However, if the game stipulates that we must purchase a card, we return a random choice out of the cards available.

For many, many more examples of how to write decision functions for this platform, please consult the 3 AI schemes currently included (dominion_ai (superclass), common_sense, and miser). 


