from code.champ import *
from code.item  import *
from code.extra import *

def optimal_build (armor, champ, extra, preset_items, time, boost, item_opt, n_items, tiers, price_range):
    """
    Calculates the optimal build (most dps) for armor 'armor' with constraints 'n_items', 'tiers' and 'price_range'
    """
    
    old_dps   = 0
    champ_dps = calc_dps(armor, champ, extra, preset_items, time, boost)
    
    if   (item_opt == 'more'):
        all_items = filter_items_tiers(tiers)
    elif (item_opt == 'fast'):
        all_items = filter_items_tiers(tiers, load_items('item_less.dat'))
    
    for items in combinations_with_replacement(all_items, n_items):
        new_items = list(preset_items) + list(items)
        
        total_price = 0
        for item in new_items:
            total_price += item.price
            
        if ((total_price < price_range['min']) or (total_price > price_range['max'])):
            continue
        
        dps = calc_dps(armor, champ, extra, new_items, time, boost)
        if (type == 'dpsgold') and (total_price != 0):
            dps -= champ_dps
            dps /= total_price
        if (dps > old_dps):
            optimal_items = new_items
            old_dps = dps

    return optimal_items
    
def optimal_path_best_dps (armor, champ, extra, items, time, boost, n_slots):
    """
    Calculate the path that maximizes the dps for each item for that build, i.e., discover in what order should the items be bought. Only uses n_slots and tries to buy the pieces before the big items.
    """
    
    if (n_slots < len(items)):
        print "Not enough slots to build all the items."
        return False
    
    optimal_path  = []
    current_build = []
    
    items_remain = []
    for item in items:
        items_remain.append(item)
        
        pieces = []
        for itm in get_combine(item):
            items_remain.append(itm)
            if get_combine(itm):
                items_remain += get_combine(itm)
            
        items_remain += pieces
    
    while (len(items_remain) > 0):
        old_dps = calc_dps(armor, champ, extra, current_build, time, boost)
        old_dps_no_slots = calc_dps(armor, champ, extra, current_build, time, boost)
        has_space = 0
        
        for item in items_remain:
            test_items = list(current_build)
            test_items.append(item)
            dps = calc_dps(armor, champ, extra, test_items, time, boost)
            
            if (dps > old_dps):
                if (len(current_build) < n_slots) and (item.tier == 'Basic'):
                    old_dps = dps
                    best_item = item
                    has_space = 1
                elif list_in_list(get_combine(item), current_build):
                    old_dps = dps
                    best_item = item
                    has_space = 1
                elif (at_least_one_in(get_combine(item), current_build)) and (len(current_build) >= n_slots) and (dps > old_dps_no_slots):
                    old_dps_no_slots = dps
                    best_item_no_slots = item
        
        if (has_space == 0):
            best_item = best_item_no_slots
                
        if (DEBUG): print best_item.name
        optimal_path.append(best_item)
        for item in get_combine(best_item):
            if (item in current_build):
                current_build.remove(item)
            elif (has_space == 0):
                items_remain.remove(item)
                for itm in get_combine(item):
                    if (itm in current_build):
                        current_build.remove(itm)
                    else:
                        items_remain.remove(itm)
                    
        current_build.append(best_item)
        items_remain.remove(best_item)
  
    return optimal_path

def reduced_armor (armor, flat_penetration, percent_penetration, flat_reduction, percent_reduction):
    """
    Returns the new armor after reductions and penetrations are applied.
    """
    
    total_armor = armor - flat_reduction
    if (total_armor) < 0:
        return total_armor
    
    total_armor = (total_armor * (1 - percent_reduction) - flat_penetration) * (1 - percent_penetration)
    if (total_armor) < 0:
        total_armor = 0
        
    return total_armor
    
def calc_damage (attack, multiplier, critical_chance, critical_damage, armor):
    """
    Returns damage from one attack
    """

    if (armor >= 0):
        return (attack * multiplier * (1 + critical_chance * critical_damage) * (100. / (100. + armor)))
    else:
        return (attack * multiplier * (1 + critical_chance * critical_damage) * (2. - 100. / (100. - armor)))

def calc_dps (armor, champ=get_champ('Ashe'), extra=None, items=[], time=5, boost={'item': 1, 'champ':1}):
    """
    Returns the dps of a certain build
    """

    stats = {0: 'attack', 1: 'attack_scaling', 2: 'speed', 3: 'speed_scaling', 4: 'multiplier',
                5: 'flat_penetration', 6: 'percent_penetration', 7: 'critical_chance', 8: 'critical_damage'}
                
    if (extra == None):
        extra = {}
        for stat in stats:
            extra[stats[stat]] = 0
        extra['level'] = champ.level
    
    champ_AD_boost = get_champ_AD_boost(champ, extra['level'], time)
    champ_passive_AD_boost = get_champ_passive_boost(champ, extra['level'])
    
    total_attack               = champ.attack + extra['attack'] + (champ.attack_scaling + extra['attack_scaling']) * (extra['level'] - 1) + boost['champ']*champ_passive_AD_boost
    total_attack              += boost['champ']*champ_AD_boost['time']*champ_AD_boost['AD']/time
    speed_multiplier           = 1 + extra['speed'] + (champ.speed_scaling + extra['speed_scaling']) * (extra['level'] - 1)
    total_multiplier           = champ.multiplier + extra['multiplier']
    if (champ.name.lower() == 'corki'): total_multiplier += boost['champ']*0.1      #going to go to a function as soon as I code Cait's passive
    total_critical_chance      = champ.critical_chance + extra['critical_chance']
    total_critical_damage      = champ.critical_damage + extra['critical_damage']
    total_flat_penetration     = champ.flat_penetration + extra['flat_penetration']
    total_percent_penetration  = (1 - champ.percent_penetration) * (1 - extra['percent_penetration'])
    total_flat_reduction       = 0
    total_percent_reduction    = 0
    
    dps = 0
    b  = 0
    bc = 0
    gb = 0
    ie = 0
    lw = 0
    
    for item in items:
        total_attack               += item.attack
        speed_multiplier           += item.speed
        total_critical_chance      += item.critical_chance
        if ((item.short.lower() == "b")  and (b  == 0)) or ((item.short.lower() == "gb") and (gb == 0)):
            total_flat_penetration += item.flat_penetration
        if (lw == 0):
            total_percent_penetration  = total_percent_penetration * (1 - item.percent_penetration)
        if (ie == 0):
            total_critical_damage += item.critical_damage
        if (item.short.lower() == "b"):  b  = 1
        if (item.short.lower() == "bc"): bc = 1
        if (item.short.lower() == "ie"): ie = 1
        if (item.short.lower() == "gb"): gb = 1
        if (item.short.lower() == "lw"): lw = 1
        if (DEBUG): print item.short 
    
    if (total_critical_chance > 1): total_critical_chance = 1
    total_percent_penetration  = 1 - total_percent_penetration
        
    gb_AS_boost    = get_item_AS_boost("gb", time, champ.type)
    champ_AS_boost = get_champ_AS_boost(champ, extra['level'], time)
    
    total_speed = champ.speed * (speed_multiplier + (boost['item']*gb*gb_AS_boost['time']*gb_AS_boost['speed'] + boost['champ']*champ_AS_boost['time']*champ_AS_boost['speed'])/time)    #Average Attack Speed from boosts
    if (total_speed > 2.5): total_speed = 2.5
    
    n_attacks = time*total_speed
    
    bc_boost = get_item_boost("bc", n_attacks)
    total_flat_reduction += bc*bc_boost['n']*bc_boost['value']/n_attacks   #Average Armor Reduction from boosts
    
    total_armor = reduced_armor(armor, total_flat_penetration, total_percent_penetration, total_flat_reduction, total_percent_reduction)
    
    return calc_damage(total_attack, total_multiplier, total_critical_chance, total_critical_damage, total_armor) * total_speed
