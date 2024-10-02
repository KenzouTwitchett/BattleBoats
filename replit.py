# replit module "clone" for local building not inside of replit
# obviously when using replit this can be ignored
# although it does still get used

import os

def clear():
    #pass
    os.system("cls" if os.name == "nt" else "clear")


