from game import Card, Game



####### GAME CARDS (& thier additonal actions) ###########
class ImaginaryCard(Card):
    def __init__(self):
        super().__init__(None, 0, 0, 0, None, False, False, None, 'error')

class Copper(Card):
    def __init__(self):
        super().__init__(None, 0, 0, 1, None, False, False, None, 'copper')

class Silver(Card):
    def __init__(self):
        super().__init__(None, 3, 0, 2, None, False, False, None, 'silver')

class Gold(Card):
    def __init__(self):
        super().__init__(None, 6, 0, 3, None, False, False, None, 'gold')

class Curse(Card):
    def __init__(self):
        super().__init__(None, 0, -1, 0, None, False, False, None, 'curse')

class Estate(Card):
    def __init__(self):
        super().__init__(None, 2, 1, 0, None, False, False, None, 'estate')

class Duchy(Card):
    def __init__(self):
        super().__init__(None, 5, 3, 0, None, False, False, None, 'duchy')

class Province(Card):
    def __init__(self):
        super().__init__(None, 8, 6, 0, None, False, False, None, 'province')

def cellar_action(my_game):
    cur_player = my_game.active_player
    cards_to_discard = []
    targ_card = my_game.active_player.ai.discard_option_fn(cur_player.my_deck)
    while targ_card.name != 'error':
        cards_to_discard += [targ_card]
        cur_player.my_deck.discard(targ_card)
        targ_card = my_game.active_player.ai.discard_option_fn(cur_player.my_deck)
    cur_player.my_deck.draw(len(cards_to_discard))

class Cellar(Card):
    def __init__(self):
        super().__init__(['+1 Action'], 2, 0, 0, cellar_action, False, False, None, 'cellar')

class Market(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+1 Action', '+1 Buy', '+1 Coin'], 5, 0, 0, None, False, False, None, 'market')

def merchant_action(my_game):
    cur_player = my_game.active_player
    if Silver in cur_player.my_deck.hand:
        my_game.process_card_actions(['+1 Coin'], None)

class Merchant(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+1 Action'], 3, 0, 0, merchant_action, False, False, None, 'merchant')

def militia_action(my_game, target_player):
    while len(target_player.my_deck.hand) > 3:
        target_player.choose_card_to_discard()

class Militia(Card):
    def __init__(self):
        super().__init__(['+2 Coins'], 4, 0, 0, militia_action, True, False, None, 'militia')

def mine_action(my_game):
    card_to_trash = my_game.active_player.ai.trash_for_treasure_fn(my_game.shop, my_game.active_player.my_deck, my_game.active_player.coins)
    
    if card_to_trash.name != 'error':
        my_game.trash_card(card_to_trash)
        card_to_gain = my_game.active_player.ai.gain_fn(my_game.shop, my_game.active_player.my_deck, card_to_trash.cost + 3)
        my_game.gain_to_hand(card_to_gain)

class Mine(Card):
    def __init__(self):
        super().__init__([], 5, 0, 0, mine_action, False, False, None, 'mine')

def moat_reaction(my_game):
    return True

class Moat(Card):
    def __init__(self):
        super().__init__(['+2 Cards'], 2, 0, 0, None, False, True, moat_reaction, 'moat')
        
def remodel_action(my_game):
    card_to_trash = my_game.active_player.ai.trash_fn(my_game.shop, my_game.active_player.my_deck, my_game.active_player.coins)
    my_game.trash_card(card_to_trash)
    card_to_gain =  my_game.active_player.ai.gain_fn(my_game.shop, my_game.active_player.my_deck, card_to_trash.cost + 2)
    my_game.gain_to_hand(card_to_gain)

class Remodel(Card):
    def __init__(self):
        super().__init__([], 4, 0, 0, remodel_action, False, False, None, 'remodel')

class Smithy(Card):
    def __init__(self):
        super().__init__(['+3 Cards'], 4, 0, 0, None, False, False, None, 'smithy')

class Village(Card):
    def __init__(self):
        super().__init__(['+1 Card', '+2 Actions'], 3, 0, 0 , None, False, False, None, 'village')

def workshop_action(my_game):
    card_to_gain =  my_game.active_player.ai.gain_fn(my_game.shop, my_game.active_player.my_deck, 4)
    my_game.gain_to_hand(card_to_gain)

class Workshop(Card):
    def __init__(self):
        super().__init__([], 3, 0, 0, workshop_action, False, False, None, 'workshop')
#####################################################
