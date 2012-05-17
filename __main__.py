import sys

import code.prog
import code.gui

if (len(sys.argv) > 1):
    if   (sys.argv[1] == '1'):
        code.prog.main_menu()
    elif (sys.argv[1] == '2'):
        code.gui.run()