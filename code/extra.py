from itertools import combinations_with_replacement
from time import sleep
import sys
import random

#Debug option
DEBUG = 0

def error(issue):                #Simple error function
    sys.stderr.write("There is a problem with the %s.\n" % (issue))
    sys.exit()
    
def wait ():                     #Pause function
    raw_input("Press Enter to continue.")
    
def is_number(number):           #Check if a number is a float or not (similar to isdigit())
    try:
        float(number)
        return True
    except ValueError:
        return False    

def to_int (string):
    if (string == ""):
        return 0
    
    return int(string)
    
def to_float (string):
    if (string in ["", "."]):
        return 0
        
    return float(string)
        
def list_in_list (list1, list2):
    """
    Test if all items in list1 are also in list2
    """
    
    if (list1 == []):
        return False
    
    list2_copy = list(list2)
    
    for i in list1:
        if not (i in list2_copy):
            return False
        list2_copy.remove(i)
    else:
        return True
       
def at_least_one_in (list1, list2):
    """
    Test if there is at least one of the items in list1 also in list2
    """
    
    for i in list1:
        if (i in list2):
            return True
    else:
        return False
