from calcs import *
from funcs import *
import matplotlib.pyplot as plt

graph_settings = ['k.', 'r.', 'g.', 'b.', 'm.', 'y.']

def get_label (champ, items, time):
    label = champ.name + " at " + str(champ.level) + " with "
    for item in items:
        label += item.short + " "
    
    label += "during " + str(time) + "s"
    
    return label
    
def make_dps_armor_graph (armor_max, champs, items, times):
    if ((len(items) != len(times)) or (len(champs) != len(items))):
        return None

    n_graphs = len(items)
    if (n_graphs > 6): n_graphs = 6
    
    armor_range = range(armor_max)
        
    for i in xrange(n_graphs):
        dps = []
        for armor in armor_range:
            dps.append(calc_dps(armor, champs[i], items[i], times[i]))
        plt.plot(armor_range, dps, graph_settings[i], label = get_label(champs[i], items[i], times[i]))

    plt.legend()
    plt.xlabel("Armor")
    plt.ylabel("DPS")
    
    fig = plt.gcf()
    DefaultSize = fig.get_size_inches()
    fig.set_size_inches( (DefaultSize[0]*2, DefaultSize[1]*2) )
    
    fig.savefig("graphs\dps_armor_graph.png")
    fig.show()
    wait()
    
def make_dpspergold_armor_graph (armor_max, champs, items, times):
    if ((len(items) != len(times)) or (len(champs) != len(items))):
        return None

    n_graphs = len(items)
    if (n_graphs > 6): n_graphs = 8
    
    armor_range = range(armor_max)
        
    for i in xrange(n_graphs):
        dps = []
        for armor in armor_range:
            dps.append(calc_dps_gold(armor, champs[i], items[i], times[i]))
        plt.plot(armor_range, dps, graph_settings[i], label = get_label(champs[i], items[i], times[i]))

    plt.legend()
    plt.xlabel("Armor")
    plt.ylabel("DPS/gold")
    
    fig = plt.gcf()
    DefaultSize = fig.get_size_inches()
    fig.set_size_inches( (DefaultSize[0]*2, DefaultSize[1]*2) )
    
    fig.savefig("graphs\dpspergold_armor_graph.png")
    fig.show()
    wait()
