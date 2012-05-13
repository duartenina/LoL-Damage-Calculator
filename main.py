import sys, os

from champdata import *
from itemdata  import *
from calcs     import *
from graphs    import *
from funcs     import *

#*******************global variables*******************



#*******************functions*******************

def main_menu ():
    champs    = []
    item_sets = []
    times     = []
    
    all_champs = load_champs()
    all_items  = load_items()
    
    print "\n******League of Legends Damage Calculator******\n"
    
    while 1:
        n_builds = raw_input("How many builds do you want to graph (1 to 6)?\n")
        if (n_builds.isdigit()):
            break
        else:
            print "Input error."
    
    n_builds = int(n_builds)
    if (n_builds < 1): n_builds = 1
    if (n_builds > 6): n_builds = 6
    
    print "\nThe program will now loop", n_builds, "times to build the information needed.\n"
      
    for i in xrange(n_builds):
        print "Build number %d of %d" % (i+1, n_builds)
        champs.append(get_champ(None, all_champs))
        champs[i] = change_champ(champs[i])
        print ""
        item_sets.append(create_item_set())
        print ""
        times.append(get_time())
        
    draw_graph(champs, item_sets, times)
    
def draw_graph (champs, item_sets, times):
    while 1:
        armor = raw_input("\nGraph from 0 armor to (maximum = 500)?\n")
        if (armor.isdigit()):
            break
        else:
            print "Input error."
    
    armor = int(armor)
    if (armor < 1): armor = 1
    if (armor > 500): armor = 500
    
    print ""
    
    while 1:
        option = raw_input("Graph 'DPS' or 'DPSperGold' ('End' to finish)?\n").lower()
        if   (option == "end"):
            break
        elif (option == "dps"):
            make_dps_armor_graph (armor, champs, item_sets, times)
        elif (option == "dpspergold"):
            make_dpspergold_armor_graph (armor, champs, item_sets, times)
        else:
            print "Incorrect option."
    
#*******************main*******************

main_menu()
