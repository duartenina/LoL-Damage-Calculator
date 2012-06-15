import matplotlib.pyplot as plt

from code.calcs import *
from code.champ import *
from code.item  import *
from code.extra import *

#Settings for the different curves of the graph
graph_settings = ['k.', 'r.', 'g.', 'b.', 'm.', 'y.', 'c.', 'w.']

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
    
def make_graph (graph_type, armor_max, builds, file):
    """
    Creates and shows graph of type 'graph_type', with builds 'builds' and saves it to 'file' (optional)
    """
    
    armor_range = range(armor_max)
       
    n = len(builds)
        
    for i in xrange(n):
        dps = []
        champ = builds[i]['champ']
        extra = builds[i]['extra']
        items = builds[i]['items']
        time  = builds[i]['time']
        total_price = 0
        
        for armor in armor_range:
            temp = calc_dps(armor, champ, extra, items, time)
            if (graph_type == 'dpspergold'):
                for item in items:
                    total_price += item.price
                temp -= calc_dps(armor, champ, extra, [], time)
                temp /= total_price/1000
            dps.append(temp)
        
        #plt.plot(armor_range, dps, graph_settings[i], label = get_label(champ, items, time))
        plt.plot(armor_range, dps, label = get_label(champ, extra['level'], items, time))
        
    plt.legend()
    plt.xlabel("Armor")
    if   (type == 'dps'):
        plt.ylabel("DPS")
    elif (type == 'dpspergold'):
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
    
