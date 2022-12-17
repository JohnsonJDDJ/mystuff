from collections import defaultdict
import json
from src import *
import time

SAVE_FILE = None

def load_state_dict(file=SAVE_FILE) -> MyStuffs:
    with open(file, 'r') as f:
        state_dict = json.load(f)
    state_dict["outgoing_from"] = defaultdict(list, state_dict["outgoing_from"])
    state_dict["pointing_into"] = defaultdict(list, state_dict["pointing_into"])
    return MyStuffs(state_dict)


def save_state_dict(mystuff: MyStuffs, file=SAVE_FILE):
    mystuff.prune()
    state_dict = mystuff.get_state_dict()
    with open(file, 'w') as f:
        json.dump(state_dict, f)


def inspect(mystuff: MyStuffs, file):
    print(mystuff)
    time.sleep(0.5)
    return "M"


def main_page_dialogue(mystuff: MyStuffs, file):
    print(
        """
        =============================
        =======   Main Page   =======
        =============================
         - [I]nspect MyStuff
         - [Q]uit program
         - Add a new [R]elation
         - [RR] remove a relation
         - Add a new [S]tuff
         - View/apply/revert [U]nsaved changes
         - Or inspect a particular Stuff by typing its [NAME]
            - Includes inspecting its information (including
              encrypted information) and its relations with
              other Stuffs.
            - Actions include editing or removing this Stuff.


        """
    )
    allowed_prompts = ["I", "Q", "R", "RR", "S", "U"]
    prompt = input("Your input -> ")
    while prompt not in allowed_prompts and prompt not in mystuff.stuffs.keys():
        prompt = input("No matching result found. Your input -> ")
    return prompt 


def quit_page_dialogue(mystuff: MyStuffs, file):
    print(
        """
        =============================
        =======   Quit Page   =======
        =============================
         - [A]bort
         - [S]ave


        """
    )
    allowed_prompts = ["A", "S"]
    prompt = input("Your input -> ")
    while prompt not in allowed_prompts:
        prompt = input("Try again. Your input -> ")

    if prompt == "S":
        save_state_dict(mystuff, file)
        
    return None

def add_relation_dialogue(mystuff: MyStuffs, file):
    print(
        f"""
        ==============================
        ======   Add Relation   ======
        ==============================

        For reference: {mystuff}

        """
    )
    from_name = input("Parent name -> ")
    while from_name not in mystuff.stuffs.keys():
        from_name = input("Not found. Parent name -> ")

    to_name = input("Child name -> ")
    while to_name not in mystuff.stuffs.keys():
        to_name = input("Not found. Parent name -> ")

    mystuff.add_dependence(from_name, to_name)

    return "M"


def remove_relation_dialogue(mystuff: MyStuffs, file):
    print(
        f"""
        =============================
        ====   Remove Relation   ====
        =============================

        For reference: {mystuff}

        """
    )
    name_A = input("Stuff A name -> ")
    while name_A not in mystuff.stuffs.keys():
        name_A = input("Not found. Stuff A name -> ")

    name_B = input("Stuff B name -> ")
    while name_B not in mystuff.stuffs.keys():
        name_B = input("Not found. Stuff B name -> ")

    mystuff.remove_dependence(name_A, name_B)
    mystuff.remove_dependence(name_B, name_A)

    return "M"