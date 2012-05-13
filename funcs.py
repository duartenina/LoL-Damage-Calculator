def error(issue):
    sys.stderr.write("There is a problem with the %s.\n" % (issue))
    sys.exit()
    
def wait ():
    print "Press Enter to continue."
    raw_input()
    
def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False    

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
