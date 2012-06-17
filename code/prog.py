import sys, os

from code.champ import *
from code.graph import *
from code.item  import *
from code.extra import *


def get_time ():
    time = "a"
    while not (time.isdigit()):
        time = raw_input("The champion will attack continually for how much time (1 to 60 seconds)?\n")
        if (time.isdigit()):
            break
        else:
            print "Incorrect input."
    
    time = int(time)
    if (time < 1): time = 1
    if (time > 60): time = 60
    
    return time


def main_menu ():
    champs    = []
    item_sets = []
    times     = []
    
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
        champs.append(get_champ(None))
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

if __name__ == '__main__':
    main_menu()

