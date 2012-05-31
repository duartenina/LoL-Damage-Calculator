import sys

import code.prog
import code.gui

opt_gui = 1

if (len(sys.argv) > 1):
    if (sys.argv[1].lower() in ['--shell', '-s', '-shell']):
        code.prog.main_menu()
        opt_gui = 0
    
if (opt_gui == 1):
    code.gui.run()