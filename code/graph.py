import matplotlib.pyplot as plt

from code.calcs import *
from code.champ import *
from code.item  import *
from code.extra import *


def get_label (champ, level, items, time):
    """
    Returns label (text) with the champion name, the short names of the items and time of attack
    """
    
    label = champ.name + "_l=" + str(level)
    n = 0
    for item in items:
        if (n == 0):
            label += "_" + item.short 
        else:
            label += "+" + item.short 
    
    label += "_t=" + str(time)
    
    return label
    
def make_graph (graph_type, armor_val, builds, boost, file):
    """
    Creates and shows graph of type 'graph_type', with builds 'builds' and saves it to 'file' (optional)
    """
    
    armor_range = range(armor_val['min'], armor_val['max'], 1)
       
    for build in builds:
        dps = []
        champ = build['champ']
        extra = build['extra']
        items = build['items']
        time  = build['time']
        total_price = 0
        
        for armor in armor_range:
            temp = calc_dps(armor, champ, extra, items, time, boost)
            if (graph_type == 'dpsgold'):
                for item in items:
                    total_price += item.price
                temp -= calc_dps(armor, champ, extra, [], time, boost)
                temp /= total_price/1000.
            dps.append(temp)
        
        plt.plot(armor_range, dps, label = get_label(champ, extra['level'], items, time))
        
    plt.legend()
    plt.xlabel("Armor")
    if   (type == 'dps'):
        plt.ylabel("DPS")
    elif (type == 'dpsgold'):
        plt.ylabel("DPS/gold")
        
    fig = plt.gcf()
    DefaultSize = fig.get_size_inches()
    fig.set_size_inches( (DefaultSize[0]*2, DefaultSize[1]*2) )
    
    if file:
        path = "graphs/" + file + ".png"
        fig.savefig(path)
        print "Graph saved to %s." % (path)
    
    print "Graph drawn: %s" % (graph_type)
    plt.show()
    
