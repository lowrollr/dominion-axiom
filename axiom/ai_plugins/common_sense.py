import random as random

from ai_plugins.dominion_ai import AI
from ai_plugins.randomania import Randomania
from game import *

#makes plays that make sense
#wont buy curses/copper
#will play actions
#will discard victory point cards
#will sequence actions to allow for action-chaining
#always spends money efficiently
def cs_action(_deck, _action_cards):
    if _action_cards == []:
        return ImaginaryCard()
    #try to sequence actions efficiently
    for x in _action_cards:
        #card gives additional actions?
        for y in x.actions:
            act_type = card_action_regex(y)
            if act_type == 'Action' or act_type == 'Actions':
                return x

    lowest_value = 999999
    lowest_value_card = ImaginaryCard()
    for x in _action_cards:
        if x.cost < lowest_value:
            lowest_value = x.cost
            lowest_value_card = x
    return lowest_value_card
     
def cs_discard(_deck):
    #going to try to stay simple here so we'll be discarding the card with the
    #lowest value (lowest buy price in this case) if no vp cards are in hand
    #this isn't always optimal but this is just another baseline bot
    lowest_value = 999999
    lowest_value_card = ImaginaryCard()
    for x in _deck.hand:
        #check for vp cards
        if x.pts:
            return x
        #find low value card
        elif x.cost < lowest_value:
            lowest_value = x.cost
            lowest_value_card = x

    return lowest_value_card

def cs_discard_option(_deck):
    lowest_value = 999999
    lowest_value_card = ImaginaryCard()
    for x in _deck.hand:
        #check for vp cards
        if x.pts:
            return x
    return lowest_value_card

#buy the highest-costed available card
def cs_buy(_shop, _deck, _coins):
    highest_value = 0
    highest_value_card = ImaginaryCard()
    cards_available = _shop.get_cards_under_amount(_coins)
    for x in cards_available:
        if x.cost > highest_value:
            highest_value = x.cost
            highest_value_card = x
    return highest_value_card


# def cs_trash(_self, _deck, _coins):

# def cs_trash_for_treasure(_shop, _deck, _coins):

def cs_trash_option(_shop, _deck, _coins):
    for x in _deck.hand:
        if x == Curse() or x == Copper() or x == Estate():
            return x
    return ImaginaryCard()

def cs_gain(_shop, _deck, _limit):
    highest_value = 0
    highest_value_card = ImaginaryCard()
    cards_available = _shop.get_cards_under_amount(_limit)
    for x in cards_available:
        if x.cost > highest_value:
            highest_value = x.cost
            highest_value_card = x
    return highest_value_card

def cs_put_on_top(_deck, _player):
    #played all actions for turn
    if _player.actions == 0:
        highest_value = 0
        highest_value_card = ImaginaryCard()
        for x in _deck.hand:
            if x.cost > highest_value:
                highest_value = x.cost
                highest_value_card = x
        return highest_value_card
    else:
        not_actions = []
        for x in _deck.hand:
            if x.actions == [] and x.additional_action == None:
                not_actions += [x]
        if not_actions == []:
            return random.choice(_deck.hand)
        return random.choice(not_actions)

#True is draw, False is discard
def cs_draw_or_discard(_card, _player):
    if _card.actions != [] or _card.additional_action != None or _card.attack_fn != None:
        if _player.actions > 0:
            return True
    if _card.pts:
        return False
    if _card.worth > 1:
        return True
    return False

Common_Sense = AI(cs_action, cs_discard, cs_discard_option, cs_buy, \
     Randomania.trash_fn, Randomania.trash_for_treasure_fn, cs_gain, cs_put_on_top, cs_trash_option, cs_draw_or_discard)