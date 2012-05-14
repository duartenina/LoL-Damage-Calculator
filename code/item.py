import csv

from code.extra import *


class item:
    def __init__ (self, item_data):
        if (item_data == None):
            self.name = "None"
            self.attack = 0
            self.speed = 0
            self.flat_penetration = 0
            self.percent_penetration = 0
            self.critical_chance = 0
            self.critical_damage = 0
            self.multiplier = 0
            self.price = 0
            self.short = "N"
        else:
            self.name = item_data[0]
            self.attack = float(item_data[1])
            self.speed = float(item_data[2])
            self.flat_penetration = float(item_data[3])
            self.percent_penetration = float(item_data[4])
            self.critical_chance = float(item_data[5])
            self.critical_damage = float(item_data[6])
            self.multiplier = float(item_data[7])
            self.price = float(item_data[8])
            self.short = item_data[9]
            
            
def load_items ():
    temp = csv.reader(open('item.dat'))
    items = []
    for t in temp:
        items.append(item(t))
    return items            
    
def get_item (name, items):
    for item in items:
        if ((item.name.lower() == name.lower()) or (item.short.lower() == name.lower())):
            return item
    
    return None
    
def create_item_set ():
    all_items = load_items()
    items = []
    exit = 0
    
    print "The champion will be using these items (maximum of 5).\nInsert the item name (examples: 'InfinityEdge' or 'IE'; 'End' to end the build)\n"
    for i in xrange(5):
        item = None
        while not item:
            item_name = raw_input("Item %d of 5: " % (i+1))
            if (item_name.lower() == "end"):
                exit = 1
                break
            item = get_item(item_name, all_items)
        if (exit == 1):
            break
        items.append(item)

    return items
    
def create_fixed_item_set (opt):
    all_items = load_items()
    items = []
    
    items.append(get_item("InfinityEdge", all_items))
    items.append(get_item("InfinityEdge", all_items))
    items.append(get_item("PhantomDancer", all_items))
    if ((opt != 3) and (opt != 5)): items.append(get_item("Bloodthirster", all_items))
    if ((opt == 1) or (opt == 3) or (opt == 5)): items.append(get_item("BlackCleaver", all_items))
    if ((opt == 2) or (opt == 3)): items.append(get_item("LastWhisper", all_items))
    if ((opt == 4) or (opt == 5)): items.append(get_item("GhostBlade", all_items))
        
    return items    

def get_item_list ():
    all_items = load_items()
    
    item_list = []
    
    for item in all_items:
        item_list.append(item.name)
    
    return item_list
    
def get_item_time (item_name, run_time):
    time  = 0
    speed = 0
    
    if (item_name == 'gb'):
        item_time  = 8
        speed      = 0.5
    
    if (run_time < item_time):
        time = run_time
    else:
        time = item_time
        
    return {'time': time, 'speed': speed}
    