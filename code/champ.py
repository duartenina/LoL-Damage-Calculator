import csv
from math import *

from code.extra import *

class champion:
    """
    Champion Class
    """
    def __init__ (self, champ_data):
        if (champ_data == None):
            self.name = ""
            self.level = 18
            self.attack = 0.
            self.speed = 0.
            self.speed_multiplier = 0.
            self.attack_scaling = 0.
            self.speed_scaling = 0.
            self.flat_penetration = 0.
            self.percent_penetration = 0.
            self.critical_chance = 0.
            self.critical_damage = 1.
            self.multiplier = 1.
            self.type = ""
        else:
            self.name = champ_data[0]
            self.level = 18
            self.attack = float(champ_data[1])
            self.speed = float(champ_data[2])
            self.speed_multiplier = float(champ_data[3])
            self.attack_scaling = float(champ_data[4])
            self.speed_scaling = float(champ_data[5])
            self.flat_penetration = float(champ_data[6])
            self.percent_penetration = float(champ_data[7])
            self.critical_chance = float(champ_data[8])
            self.critical_damage = float(champ_data[9])
            self.multiplier = float(champ_data[10])
            self.type = champ_data[11]
        
    def copy_champ (self, champ):
        self.attack = champ.attack
        self.speed = champ.speed
        self.attack_scaling = champ.attack_scaling
        self.speed_scaling = champ.speed_scaling
        self.type = champ.type
        
    def show_stats (self):                #Prints all champ stats
        print "\n%s at level ('lvl') %d" % (self.name, self.level)
        print "Attack Damage ('AD', 'ADlvl') = %f + %f per level" % (self.attack, self.attack_scaling)
        print "Attack Speed ('AS', 'ASlvl', 'ASm') = %f * (1 + %f per level + %f)" % (self.speed, self.speed_scaling, self.speed_multiplier)
        print "Penetration ('FArP', 'PArp') = %f + %f%%" % (self.flat_penetration, self.percent_penetration*100)
        print "Critical Chance ('CrC') = %f%% | Critical Damage ('CrD') = %f%%" % (self.critical_chance*100, self.critical_damage*100)
        print "Damage multiplier ('DM') = %f" % (self.multiplier)
        print "Type: %s\n" % (self.type)

    def __getitem__ (self, prop):               #Returns champ[prop]
        try: 
            return self.__dict__[prop]
        except KeyError:
            return 0
        
    def __setitem__ (self, prop, value):        #Applies champ[prop] = value
        try: 
            self.__dict__[prop] = value
        except KeyError:
            return None
        
    def stats (self):                           #Returns tuple with all possible champ stats
        return ('name', 'level', 'attack', 'attack_scaling', 'speed', 'speed_multiplier', 'speed_scaling', 'flat_penetration', 'percent_penetration', 'critical_chance', 'critical_damage', 'multiplier', 'type')
            
    def dict (self):                            #Returns dict with champs stats: {'name': Ashe, 'level': 13, etc}
        dict = {}
        
        for stat in self.stats():
            dict[stat] = self[stat]
        
        return dict            
        
def load_champs (file='champ.dat'):
    """
    Loads all champs from file and returns list of champion class instances (default file 'champ.dat')
    """
    
    temp = csv.reader(open(file))
    champs = []
    for t in temp:
        champs.append(champion(t))
        
    return champs
    
def get_champ (name=None, champs=load_champs()):
    """
    Returns champ with name 'name' from list 'champs' (default all champions in champ.dat)
    If name == None, it will ask for name in terminal
    """
    
    champ = None
    
    while not champ:
        if (name == None):
            name = raw_input("What champion (example: Ashe)?\n")
            name = name.strip()
        
        for temp in champs:
            if (temp.name.lower() == name.lower()):
                champ = temp
                
        name = None
        
        if (champ == None):
            print "Champion not found.\n"
            name = None
    
    return champ
    
def get_champion_list (all_champs=load_champs()):
    """
    Returns list of champion names from list of champion class instances (default all champions in champ.dat)
    """
    
    champs = []
    
    for champ in all_champs:
        champs.append(champ.name)
    
    return champs
    
def create_champ ():
    """
    Creates champ from arguments
    
    Deprecated
    """
    
    champ = champion(None)
    champ.name = "Custom"
    
    for arg in sys.argv:
        if (arg.isdigit()):
            temp = int(arg)
            if (temp < 1):
                temp = 1
            if (temp > 18):
                temp = 18
            champ.level = temp
        elif (get_champ(arg)):
            temp = get_champ(arg)
            champ.copy_champ(temp)
            champ.name += " " + temp.name
            
    if (champ.name == "Custom"):
        temp = get_champ("Ashe")
        champ.copy_champ(temp)
        champ.name += " " + temp.name
        
    return champ       
    
def change_champ (champ):
    """
    Changes champ stats in terminal
    
    Deprecated
    """

    while 1:
        champ.show_stats()
        option = raw_input("What stat do you want to change ('End' to finish)\n").strip().lower()
        if   (option == "end"):
            break
        elif (option == "lvl"):
            new_stat = raw_input ("What level is the champion at (1 to 18)?\n")
            if (new_stat.isdigit()):
                new_stat = int(new_stat)
                if (new_stat < 1): new_stat = 1
                if (new_stat > 18): new_stat = 18
                champ.level = new_stat
        elif (option == "ad"):
            new_stat = raw_input ("What is the champion's Attack Damage?\n")
            if (is_number(new_stat)):
                new_stat = float(new_stat)
                champ.attack = new_stat
        elif (option == "adlvl"):
            new_stat = raw_input ("What is the champion's Attack Damage scaling?\n")
            if (is_number(new_stat)):
                new_stat = float(new_stat)
                champ.attack_scaling = new_stat
        elif (option == "as"):
            new_stat = raw_input ("What is the champion's Attack Speed?\n")
            if (is_number(new_stat)):
                new_stat = float(new_stat)
                champ.speed = new_stat
        elif (option == "aslvl"):
            new_stat = raw_input ("What is the champion's Attack Speed scaling?\n")
            if (is_number(new_stat)):
                new_stat = float(new_stat)
                champ.speed_scaling = new_stat
        elif (option == "farp"):
            new_stat = raw_input ("What is the champion's flat Armor Penetration?\n")
            if (is_number(new_stat)):
                new_stat = float(new_stat)
                champ.flat_penetration = new_stat
        elif (option == "parp"):
            new_stat = raw_input ("What is the champion's percent Armor Penetration?\n")
            if (is_number(new_stat)):
                new_stat = float(new_stat)
                champ.percent_penetration = new_stat
        elif (option == "crc"):
            new_stat = raw_input ("What is the champion's Critical Chance?\n")
            if (is_number(new_stat)):
                new_stat = float(new_stat)
                champ.critical_chance = new_stat
        elif (option == "crd"):
            new_stat = raw_input ("What is the champion's Critical Damage?\n")
            if (is_number(new_stat)):
                new_stat = float(new_stat)
                champ.critical_damage = new_stat
        elif (option == "dm"):
            new_stat = raw_input ("What is the champion's Damage Multiplier?\n")
            if (is_number(new_stat)):
                new_stat = float(new_stat)
                champ.multiplier = new_stat
        elif (option == "asm"):
            new_stat = raw_input ("What is the champion's Attack Speed Multiplier?\n")
            if (is_number(new_stat)):
                new_stat = float(new_stat)
                champ.speed = new_stat
                
        else:
            print "Stat not found."
    return champ    

def get_champ_passive_boost (champ, level):
    """
    Calculates the Attack Damage boost from abilities and returns dict {'time': time, 'AD': attack}, where time is how much time the ability is on and attack is the value of the boost
    """
    
    attack = 0
    
    name       = champ.name.lower()
    champs =   {'masteryi': {'rank_lvl': min((level+1)/2, 5), 'ranks': {1: 15, 2: 20, 3: 25, 4: 30, 5: 35}},
                'fiora':    {'rank_lvl': min((level+1)/2, 5), 'ranks': {1: 15, 2: 20, 3: 25, 4: 30, 5: 35}}}
    
    if name in champs:
        rank_lvl = champs[name]['rank_lvl']
        attack   = champs[name]['ranks'][rank_lvl]
    
    return attack
    
def get_champ_AD_boost (champ, level, run_time):
    """
    Calculates the Attack Damage boost from abilities and returns dict {'time': time, 'AD': attack}, where time is how much time the ability is on and attack is the value of the boost
    """

    name       = champ.name.lower()
    time       = 0
    skill_time = 0
    attack     = 0
    
    champs =   {'masteryi': {'rank_lvl': min((level+1)/2, 5), 'skill_time': 10,                        'ranks': {1: 15, 2: 20, 3: 25, 4: 30, 5: 35}},
                'vayne':    {'rank_lvl': min((level-1)/5, 3), 'skill_time': (min((level-1)/5, 3)+3)*2, 'ranks': {1: 25, 2: 40, 3: 55}}}
    
    if name in champs:
        skill_time = champs[name]['skill_time']
        rank_lvl   = champs[name]['rank_lvl']
        attack     = champs[name]['ranks'][rank_lvl]
    
    if (run_time < skill_time):
        time = run_time
    else:
        if (name == 'masteryi'):
            if (run_time < 35):
                time = 20 - run_time
            else:
                time = -15
        time = skill_time
    
    return {'time': time, 'AD': attack}
    
def get_champ_AS_boost (champ, level, run_time):
    """
    Calculates the Attack Speed boost from abilities and returns dict {'time': time, 'speed': speed}, where time is how much time the ability is on and speed is the value of the boost
    """

    name       = champ.name.lower()
    time       = 0
    skill_time = 0
    speed      = 0
    
    champs =   {'tristana':    {'rank_lvl': min((level+1)/2, 5), 'skill_time': 7,                         'ranks': {1: .30, 2: .45, 3: .60, 4: 0.75, 5: 0.90}},
                'missfortune': {'rank_lvl': min((level+1)/2, 5), 'skill_time': 6,                         'ranks': {1: .30, 2: .35, 3: .40, 4: 0.45, 5: 0.50}},
                'fiora':       {'rank_lvl': min(level/2, 5),     'skill_time': 3,                         'ranks': {1: .60, 2: .75, 3: .90, 4: 1.05, 5: 1.20}},
                'masteryi':    {'rank_lvl': min((level-1)/5, 3), 'skill_time': (min((level-1)/5, 3)+3)*2, 'ranks': {1: .40, 2: .60, 3: .80}},
                'sivir':       {'rank_lvl': min((level-1)/5, 3), 'skill_time': 10,                        'ranks': {1: .30, 2: .45, 3: .60}},
                'twitch':      {'rank_lvl': min((level+1)/2, 5), 'skill_time': 10,                        'ranks': {1: .30, 2: .40, 3: .50, 4: 0.60, 5: 0.70}}}
                
    if name in champs:
        skill_time = champs[name]['skill_time']
        rank_lvl   = champs[name]['rank_lvl']
        speed      = champs[name]['ranks'][rank_lvl]
    
    if (run_time < skill_time):
        time = run_time
    else:
        time = skill_time
    
    return {'time': time, 'speed': speed}
    
