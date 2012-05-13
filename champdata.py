import csv
from funcs import *

class champion:
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
        
    def show_stats (self):
        print "\n%s at level ('lvl') %d" % (self.name, self.level)
        print "Attack Damage ('AD', 'ADlvl') = %f + %f per level" % (self.attack, self.attack_scaling)
        print "Attack Speed ('AS', 'ASlvl', 'ASm') = %f * (1 + %f per level + %f)" % (self.speed, self.speed_scaling, self.speed_multiplier)
        print "Penetration ('FArP', 'PArp') = %f + %f%%" % (self.flat_penetration, self.percent_penetration*100)
        print "Critical Chance ('CrC') = %f%% | Critical Damage ('CrD') = %f%%" % (self.critical_chance*100, self.critical_damage*100)
        print "Damage multiplier ('DM') = %f" % (self.multiplier)
        print "Type: %s\n" % (self.type)

def load_champs ():
    temp = csv.reader(open('champ.dat'))
    champs = []
    for t in temp:
        champs.append(champion(t))
        
    return champs
    
def get_champ (name, champs):
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
    
    return champ
    
def create_champ ():
    champ = champion(None)
    champ.name = "Custom"
    champs = load_champs()
    
    for arg in sys.argv:
        if (arg.isdigit()):
            temp = int(arg)
            if (temp < 1):
                temp = 1
            if (temp > 18):
                temp = 18
            champ.level = temp
        elif (get_champ(arg, champs)):
            temp = get_champ(arg, champs)
            champ.copy_champ(temp)
            champ.name += " " + temp.name
            
    if (champ.name == "Custom"):
        temp = get_champ("Ashe", champs)
        champ.copy_champ(temp)
        champ.name += " " + temp.name
        
    return champ       
    
def change_champ (champ):
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
