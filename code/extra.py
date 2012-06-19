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
