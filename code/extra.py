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


