# replit module "clone" for local building not inside of replit
# obviously when using replit this can be ignored

import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")
