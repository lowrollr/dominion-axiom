from cards import *

def default_shop():
    shop_contents = {}
    shop_action_amount = 10
    shop_vp_amount = 12
    shop_contents['copper'] = [Copper(), 60]
    shop_contents['silver'] = [Silver(), 40]
    shop_contents['gold'] = [Gold(), 30]
    shop_contents['curse'] = [Curse(), 30]
    shop_contents['estate'] = [Estate(), shop_vp_amount]
    shop_contents['duchy'] = [Duchy(), shop_vp_amount]
    shop_contents['province'] = [Province(), shop_vp_amount]
    shop_contents['cellar'] = [Cellar(), shop_action_amount]
    shop_contents['market'] = [Market(), shop_action_amount]
    shop_contents['merchant'] = [Merchant(), shop_action_amount]
    shop_contents['militia'] = [Militia(), shop_action_amount]
    shop_contents['mine'] = [Mine(), shop_action_amount]
    shop_contents['moat'] = [Moat(), shop_action_amount]
    shop_contents['remodel'] = [Remodel(), shop_action_amount]
    shop_contents['smithy'] = [Smithy(), shop_action_amount]
    shop_contents['village'] = [Village(), shop_action_amount]
    shop_contents['workshop'] = [Workshop(), shop_action_amount]
    
    return shop_contents
