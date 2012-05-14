from code.champ import *
from code.item  import *
from code.extra import *


def reduced_armor (armor, flat_penetration, percent_penetration):
    total_armor = (armor - flat_penetration) * (1 - percent_penetration)
    if (total_armor) < 0:
        total_armor = 0
        
    return total_armor
    
def calc_damage (attack, multiplier, critical_chance, critical_damage, armor):
    return (attack * multiplier * (1 + critical_chance * critical_damage) * (100 / (100 + armor)))

def calc_dps (armor,champ,items,time):
    total_attack               = champ.attack + champ.attack_scaling * (champ.level - 1)
    speed_multiplier           = 1 + champ.speed_scaling * (champ.level - 1) + champ.speed_multiplier
    total_multiplier           = champ.multiplier
    total_critical_chance      = champ.critical_chance
    total_critical_damage      = champ.critical_damage
    total_flat_penetration     = champ.flat_penetration
    total_percent_penetration  = champ.percent_penetration
    
    dps = 0
    bc = 0
    ie = 0
    gb = 0
    for item in items:
        total_attack               += item.attack
        speed_multiplier           += item.speed
        total_critical_chance      += item.critical_chance
        total_flat_penetration     += item.flat_penetration
        total_percent_penetration  += item.percent_penetration
        if (ie == 0): total_critical_damage += item.critical_damage
        if (item.short.lower() == "bc"): bc = 1
        if (item.short.lower() == "ie"): ie = 1
        if (item.short.lower() == "gb"): gb = 1
    
    gb_stats    = get_item_time("gb", time)
    champ_stats = get_champ_time(champ, time)
    
    total_speed = champ.speed * (speed_multiplier + (gb*gb_stats['time']*gb_stats['speed'] + champ_stats['time']*champ_stats['speed'])/time)
    n_attacks   = time*total_speed
    
    if (bc == 0):
        total_armor = reduced_armor(armor, total_flat_penetration, total_percent_penetration)
        dps = calc_damage(total_attack, total_multiplier, total_critical_chance, total_critical_damage, total_armor) * n_attacks / time
    elif (bc == 1):
        for i in xrange(3):
            total_armor = reduced_armor(armor, total_flat_penetration, total_percent_penetration)
            dps += calc_damage(total_attack, total_multiplier, total_critical_chance, total_critical_damage, total_armor)
            total_flat_penetration += 15
        total_armor = reduced_armor(armor, total_flat_penetration, total_percent_penetration)
        dps += calc_damage(total_attack, total_multiplier, total_critical_chance, total_critical_damage, total_armor) * (n_attacks - 3) 
        dps = dps / time
            
    return dps
    
def calc_dps_gold (armor,champ,items,time):
    total_attack               = champ.attack + champ.attack_scaling * (champ.level - 1)
    speed_multiplier           = 1 + champ.speed_scaling * (champ.level - 1)
    total_multiplier           = champ.multiplier
    total_critical_chance      = champ.critical_chance
    total_critical_damage      = champ.critical_damage
    total_flat_penetration     = champ.flat_penetration
    total_percent_penetration  = champ.percent_penetration
    
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
    
    gb_stats    = get_item_time("gb", time)
    champ_stats = get_champ_time(champ, time)
    
    total_speed = champ.speed * (speed_multiplier + (gb*gb_stats['time']*gb_stats['speed'] + champ_stats['time']*champ_stats['speed'])/time)
    n_attacks   = time*total_speed
    
    if (bc == 0):
        total_armor = reduced_armor(armor, total_flat_penetration, total_percent_penetration)
        dps = calc_damage(total_attack, total_multiplier, total_critical_chance, total_critical_damage, total_armor) * n_attacks / time
    elif (bc == 1):
        for i in xrange(3):
            total_armor = reduced_armor(armor, total_flat_penetration, total_percent_penetration)
            dps += calc_damage(total_attack, total_multiplier, total_critical_chance, total_critical_damage, total_armor)
            total_flat_penetration += 15
        total_armor = reduced_armor(armor, total_flat_penetration, total_percent_penetration)
        dps += calc_damage(total_attack, total_multiplier, total_critical_chance, total_critical_damage, total_armor) * (n_attacks - 3) 
        dps = dps / time
            
    return dps/total_price


    