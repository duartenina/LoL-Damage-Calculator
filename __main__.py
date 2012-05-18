import sys

import code.prog
import code.gui

gui = 1

if (len(sys.argv) > 1):
    if   (sys.argv[1].lower() in ['--shell', '-s', '-shell'):
        code.prog.main_menu()
        gui = 0
    
if (gui == 1):
    code.gui.run()