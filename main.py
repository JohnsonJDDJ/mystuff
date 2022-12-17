print("=== Initializing ===")

from src import *
import sys
from utils import *

SAVE_FILE = sys.argv[1]

ACTION_MAP = {"I": inspect, 
              "M": main_page_dialogue,
              "Q": quit_page_dialogue}

me = load_state_dict(SAVE_FILE)
print("=== Saved JSON Loaded ===")
print(me)



action = "M"
while action:

    action = ACTION_MAP[action](me, SAVE_FILE)