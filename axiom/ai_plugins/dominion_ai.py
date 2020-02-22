
class AI:
    def __init__(self, my_action_fn, my_discard_fn, my_discard_option_fn, my_buy_fn, my_trash_fn, my_trash_for_treasure_fn, my_gain_fn):
        self.action_fn = my_action_fn
        self.discard_fn = my_discard_fn
        self.discard_option_fn = my_discard_option_fn
        self.buy_fn = my_buy_fn
        self.trash_fn = my_trash_fn
        self.trash_for_treasure_fn = my_trash_for_treasure_fn
        self.gain_fn = my_gain_fn