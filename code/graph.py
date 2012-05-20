import matplotlib.pyplot as plt

from code.calcs import *
from code.champ import *
from code.item  import *
from code.extra import *


graph_settings = ['k.', 'r.', 'g.', 'b.', 'm.', 'y.']


def get_label (champ, items, time):
    label = champ.name + " at " + str(champ.level) + " with "
    for item in items:
        label += item.short + " "
    
    label += "during " + str(time) + "s"
    
    return label
    
def make_graph (graph_type, armor_max, builds, file):
    armor_range = range(armor_max)
       
    n = len(builds)
        
    for i in xrange(n):
        dps = []
        champ = builds[i]['champ']
        extra = builds[i]['extra']
        items = builds[i]['items']
        time  = builds[i]['time']
        
        for armor in armor_range:
            temp = calc_dps(graph_type, armor, champ, extra, items, time)
            dps.append(temp)
        
        plt.plot(armor_range, dps, graph_settings[i], label = get_label(champ, items, time))

    plt.legend()
    plt.xlabel("Armor")
    plt.ylabel("DPS")
    
    fig = plt.gcf()
    DefaultSize = fig.get_size_inches()
    fig.set_size_inches( (DefaultSize[0]*2, DefaultSize[1]*2) )
    
    if file:
        path = "graphs\\" + file + ".png"
        fig.savefig(path)
        print "Graph saved to %s." % (path)
    
    print "Graph drawn: %s" % (graph_type)
    plt.show()
    #wait()
 
