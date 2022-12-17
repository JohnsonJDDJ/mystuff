print("=== Initializing ===")

from src import *
import sys
from utils import *

SAVE_FILE = sys.argv[1]

MAIN_ACTION_MAP = {"I": inspect, 
                   "M": main_page_dialogue,
                   "Q": quit_page_dialogue,
                   "R": add_relation_dialogue,
                   "RR": remove_relation_dialogue,
                   "S": add_stuff_dialogue,
                   "U": unsaved_changes_dialogue}

STUFF_ACTION_MAP = {"SC": inspect_children,
                    "SE": edit_stuff_dialogue,
                    "SI": inspect_stuff,
                    "SM": stuff_main_page_dialogue,
                    "SN": inspect_neighbors,
                    "SP": inspect_parents,
                    "SR": remove_stuff_dialogue}

me = load_state_dict(SAVE_FILE)
print("=== Saved JSON Loaded ===")
print(me)

action = "M"
while action:
    if action in MAIN_ACTION_MAP.keys():
    #    =============================
    #    =======   Main Page   =======
    #    =============================
    #     - [I]nspect MyStuff
    #     - [Q]uit program
    #     - Add a new [R]elation
    #     - [RR] remove a relation
    #     - Add a new [S]tuff
    #     - View/apply/revert [U]nsaved changes
    #     - Or inspect a particular Stuff by typing its [NAME]
    #     - Includes inspecting its information (including
    #         encrypted information) and its relations with
    #         other Stuffs.
    #     - Actions include editing or removing this Stuff.

        action = MAIN_ACTION_MAP[action](me, SAVE_FILE)

    else:
    #    ===============================
    #    =======   Stuffs Page   =======
    #    ===============================
    #     - Inspect [C]hildren
    #     - [E]dit {name}
    #     - [I]nspect {name}
    #     - Inspect [N]eighbors
    #     - Inspect [P]arents
    #     - [R]emove {name}
    #     - Quit to [M]ain page (changes won't be lost).

        name = action[0]
        action = action[1]
        action = STUFF_ACTION_MAP[action](name, me, SAVE_FILE)

print("=== Program Stopped ===")