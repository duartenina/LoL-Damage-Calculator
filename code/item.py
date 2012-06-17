import csv

from code.extra import *

class item:
    """
    Class Item
    """
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
            self.tier = "None"
            self.combine = ""
            self.combine_cost = 0
        else:
            self.name = item_data[0]
            self.attack = float(item_data[1])
            self.speed = float(item_data[2])
            self.flat_penetration = float(item_data[3])
            self.percent_penetration = float(item_data[4])
            self.critical_chance = float(item_data[5])
            self.critical_damage = float(item_data[6])
            self.multiplier = float(item_data[7])
            self.price = int(item_data[8])
            self.short = item_data[9]
            self.tier = item_data[10]
            self.combine = item_data[11]
            self.combine_cost = int(item_data[12])

    def __getitem__ (self, prop):               #Returns item[prop]
        try: 
            return self.__dict__[prop]
        except KeyError:
            return 0
        
    def __setitem__ (self, prop, value):        #Applies item[prop] = value
        try: 
            self.__dict__[prop] = value
        except KeyError:
            return None
    
    def stats (self):                           #Returns tuple with all possible item stats
        return ('name', 'attack', 'speed', 'flat_penetration', 'percent_penetration', 'critical_chance', 'critical_damage', 'multiplier', 'price', 'short', 'tier', 'combine', 'combine_cost')
            
    def dict (self):                            #Returns dict with item stats: {'name': InfinityEdge, 'attack': 80, etc}
        dict = {}
        
        for stat in self.stats():
            dict[stat] = self[stat]
        
        return dict

def load_items (file='item.dat'):
    """
    Loads all items from file and returns list of item class instances (default file 'item.dat')
    """

    temp = csv.reader(open(file))
    items = []
    for t in temp:
        items.append(item(t))
    return items            
    
def filter_items_tiers (tiers={'None': 1, 'Basic': 1, 'Advanced': 1, 'Legendary': 1}, items=load_items()):
    new_items = []
    
    for item in items:
        if tiers[item.tier]:
            new_items.append(item)
        
    return new_items
    
def get_item (name, items=load_items()):
    """
    Returns item with name or short 'name' from list 'items' (default all items in item.dat)
    """
    
    for item in items:
        if ((item.name.lower() == name.lower()) or (item.short.lower() == name.lower())):
            return item
    
    return None
    
def create_item_set ():
    """
    Creates a item set in the terminal
    
    Deprecated
    """
    
    items = []
    exit = 0
    
    print "The champion will be using these items (maximum of 5).\nInsert the item name (examples: 'InfinityEdge' or 'IE'; 'End' to end the build)\n"
    for i in xrange(5):
        item = None
        while not item:
            item_name = raw_input("Item %d of " % (i+1))
            if (item_name.lower() == "end"):
                exit = 1
                break
            item = get_item(item_name)
        if (exit == 1):
            break
        items.append(item)

    return items
    
def create_fixed_item_set (opt):
    """
    Creates a fixed item set chosen from an opt
    
    Deprecated
    """

    items = []
    
    items.append(get_item("InfinityEdge"))
    items.append(get_item("InfinityEdge"))
    items.append(get_item("PhantomDancer"))
    if ((opt != 3) and (opt != 5)): items.append(get_item("Bloodthirster"))
    if ((opt == 1) or (opt == 3) or (opt == 5)): items.append(get_item("BlackCleaver"))
    if ((opt == 2) or (opt == 3)): items.append(get_item("LastWhisper"))
    if ((opt == 4) or (opt == 5)): items.append(get_item("GhostBlade"))
        
    return items    

def get_item_list (all_items=load_items()):
    """
    Returns list of item names from list of item class instances (default all items in item.dat)
    """
    
    item_list = []
    
    for item in all_items:
        item_list.append(item.name)
    
    return item_list
    
def get_item_time (item_name, run_time, champ_type):
    """
    Calculates the Attack Speed boost from items' actives and returns dict {'time': time, 'speed': speed},
     where time is how much time the item active is on and speed is the value of the boost
    """

    time  = 0
    speed = 0
    
    if (item_name == 'gb'):
        if (champ_type.lower() == "melee"):
            item_time = 8
        else:
            item_time = 4
        speed = 0.5
    
    if (run_time < item_time):
        time = run_time
    else:
        time = item_time
        
    return {'time': time, 'speed': speed}
    
def get_item_attacks (item_name, n_attacks):
    """
    Calculates the boost from items and returns dict {'n': n, 'value': value},
     where n is the number of attacks where the boost works and value is the value of the boost
    """

    n     = 1
    value = 0
    
    if (item_name == 'bc'):
        value = 45
    else:
        return None
    
    if   (int(n_attacks) == 1):
        value = 0
    elif (int(n_attacks) == 2):
        value /= 3
    elif (n_attacks > 3):
        n = n_attacks - 2 
        
    return {'n': n, 'value': value}    
    
