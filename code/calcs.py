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
        return (attack * multiplier * (1 + critical_chance * critical_damage) * (100. / (100. + armor)))
    else:
        return (attack * multiplier * (1 + critical_chance * critical_damage) * (2. - 100. / (100. - armor)))

def calc_dps (armor, champ, extra, items, time):
    stats = {0: 'attack', 1: 'attack_scaling', 2: 'speed', 3: 'speed_scaling', 4: 'multiplier',
                5: 'flat_penetration', 6: 'percent_penetration', 7: 'critical_chance', 8: 'critical_damage'}
                
    if (extra == None):
        extra = {}
        for stat in stats:
            extra[stats[stat]] = 0
    
    total_attack               = champ.attack + extra['attack'] + (champ.attack_scaling + extra['attack_scaling']) * (champ.level - 1)
    speed_multiplier           = 1 + extra['speed'] + (champ.speed_scaling + extra['speed_scaling']) * (champ.level - 1)
    total_multiplier           = champ.multiplier + extra['multiplier']
    total_critical_chance      = champ.critical_chance + extra['critical_chance']
    total_critical_damage      = champ.critical_damage + extra['critical_damage']
    total_flat_penetration     = champ.flat_penetration + extra['flat_penetration']
    total_percent_penetration  = (1 - champ.percent_penetration) * (1 - extra['percent_penetration'])
    total_flat_reduction       = 0
    total_percent_reduction    = 0
    
    dps = 0
    bc = 0
    ie = 0
    gb = 0
    lw = 0
    for item in items:
        total_attack               += item.attack
        speed_multiplier           += item.speed
        total_critical_chance      += item.critical_chance
        total_flat_penetration     += item.flat_penetration
        if (lw == 0): total_percent_penetration  = 1 - total_percent_penetration * (1 - item.percent_penetration)
        if (ie == 0): total_critical_damage += item.critical_damage
        if (item.short.lower() == "bc"): bc = 1
        if (item.short.lower() == "ie"): ie = 1
        if (item.short.lower() == "gb"): gb = 1
        if (item.short.lower() == "lw"): lw = 1
        #print item.short
    
    
    gb_stats    = get_item_time("gb", time, champ.type)
    champ_stats = get_champ_time(champ, time)
    
    total_speed = champ.speed * (speed_multiplier + (gb*gb_stats['time']*gb_stats['speed'] + champ_stats['time']*champ_stats['speed'])/time)
    if (total_speed > 2.5): total_speed = 2.5
    
    n_attacks   = time*total_speed
    
    bc_stats    = get_item_attacks("bc", n_attacks)
    total_flat_reduction += bc*bc_stats['n']*bc_stats['value']/n_attacks
    
    total_armor = reduced_armor(armor, total_flat_penetration, total_percent_penetration, total_flat_reduction, total_percent_reduction)
    dps = calc_damage(total_attack, total_multiplier, total_critical_chance, total_critical_damage, total_armor) * total_speed
    
    return dps
