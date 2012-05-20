from code.champ import *
from code.item  import *
from code.extra import *


def reduced_armor (armor, flat_penetration, percent_penetration, flat_reduction, percent_reduction):
    
    total_armor = armor - flat_reduction
    if (total_armor) < 0:
        return total_armor
    
    total_armor = (total_armor * (1 - percent_reduction) - flat_penetration) * (1 - percent_penetration)
    if (total_armor) < 0:
        total_armor = 0
        
    return total_armor
    
def calc_damage (attack, multiplier, critical_chance, critical_damage, armor):
    if (armor >= 0):
        return (attack * multiplier * (1 + critical_chance * critical_damage) * (100 / (100 + armor)))
    else:
        return (attack * multiplier * (1 + critical_chance * critical_damage) * (2 - 100 / (100 - armor)))

def calc_dps (calc_type, armor,champ, items, time):
    total_attack               = champ.attack + champ.attack_scaling * (champ.level - 1)
    speed_multiplier           = 1 + champ.speed_scaling * (champ.level - 1)
    total_multiplier           = champ.multiplier
    total_critical_chance      = champ.critical_chance
    total_critical_damage      = champ.critical_damage
    total_flat_penetration     = champ.flat_penetration
    total_percent_penetration  = champ.percent_penetration
    total_flat_reduction       = 0
    total_percent_reduction    = 0
    
    dps = 0
    bc = 0
    ie = 0
    gb = 0
    total_price = 0
    for item in items:
        total_price                += item.price
        total_attack               += item.attack
        speed_multiplier           += item.speed
        total_critical_chance      += item.critical_chance
        total_flat_penetration     += item.flat_penetration
        total_percent_penetration  += item.percent_penetration
        if (ie == 0): total_critical_damage += item.critical_damage
        if (item.short.lower() == "bc"): bc = 1
        if (item.short.lower() == "ie"): ie = 1
        if (item.short.lower() == "gb"): gb = 1
    
    gb_stats    = get_item_time("gb", time, champ.type)
    champ_stats = get_champ_time(champ, time)
    
    total_speed = champ.speed * (speed_multiplier + (gb*gb_stats['time']*gb_stats['speed'] + champ_stats['time']*champ_stats['speed'])/time)
    n_attacks   = time*total_speed
    
    bc_stats    = get_item_attacks("bc", n_attacks)
    
    total_flat_reduction += bc*bc_stats['n']*bc_stats['value']/n_attacks
    
    total_armor = reduced_armor(armor, total_flat_penetration, total_percent_penetration, total_flat_reduction, total_percent_reduction)
    dps = calc_damage(total_attack, total_multiplier, total_critical_chance, total_critical_damage, total_armor) * n_attacks / time
    
    if   (calc_type == 'dps'):
        return dps
    elif (calc_type == 'dpspergold'):
        return dps/total_price
