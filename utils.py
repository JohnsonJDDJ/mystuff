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

    if prompt not in allowed_prompts:
        return prompt, "SM"

    return prompt 


def inspect(mystuff: MyStuffs, file):
    print(mystuff)
    time.sleep(0.5)
    return "M"


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

    confirm = input(f"Adding relation from {from_name} to {to_name}. Enter or [N]o.")
    if confirm == "N": return "M"

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


def add_stuff_dialogue(mystuff: MyStuffs, file):
    print(
        """
        =============================
        =====   Add New Stuff   =====
        =============================


        """
    )
    name = input("Enter name -> ")
    while name in mystuff.stuffs.keys():
        name = input("Duplicate name. Enter NAME (all caps) -> ")

    new_stuff = Stuff(name)

    prompt = None
    allowed_prompts = ["A", "D", "E", "N", "S"]

    while prompt != "S":
        print(
        f"""
        ==============================
        =====   New Stuff Page   =====
        ==============================
         - [A]ttribute (edit or add)
         - [D]escription (edit)
         - [E]ncrypted attribute (edit or add)
         - [N]ame (edit)
         - [S]ave and apply

{new_stuff}


        """
        )
        prompt = input("Yout input -> ")
        while prompt not in allowed_prompts:
            prompt = input("Try again. Yout input -> ")

        if prompt == "A":
            key = input("Attribute name -> ")
            value = input("Attribute value -> ")
            new_stuff.add_attribute(key, value)

        elif prompt == "D":
            des = input("Description -> ")
            new_stuff.edit_description(des)

        elif prompt == "E":
            key = input("Attribute name -> ")
            value = input("Attribute value -> ")
            enc_key = input("Encryption key -> ")
            new_stuff.add_secret_attribute(key, value, enc_key)
        
        elif prompt == "N":
            new_name = input("New NAME (all caps) -> ")
            new_stuff.edit_name(new_name)
        
        elif prompt == "S":
            mystuff.add_stuff(new_stuff)
    
    return "M"


def unsaved_changes_dialogue(mystuff: MyStuffs, file):
    print(
        f"""
        =============================
        ====   Unsaved Changes   ====
        =============================
         - [A]pply
         - [R]evert

        """
    )
    mystuff.view_unsaved_changes()
    allowed_prompts = ["A", "R"]
    prompt = input("Your input -> ")
    while prompt not in allowed_prompts:
        prompt = input("Try again. Your input -> ")

    if prompt == "A":
        mystuff.apply()
    elif prompt == "R":
        mystuff.revert()
        
    return "M"


def stuff_main_page_dialogue(name, mystuff: MyStuffs, file):
    print(
        f"""
        =============================
        ======   Stuffs Page   ======
        =============================
         - Inspect [C]hildren
         - [E]dit {name}
         - [I]nspect {name}
         - Inspect [N]eighbors
         - Inspect [P]arents
         - [R]emove {name}
         - Quit to [M]ain page (changes won't be lost).
        (To apply changes, return to main page)

        """
    )
    allowed_prompts = ["C", "E", "I", "N", "P", "R", "M"]
    prompt = input("Your input -> ")
    while prompt not in allowed_prompts:
        prompt = input("Try again. Your input -> ")

    if prompt == "M": return "M"

    return name, "S" + prompt 


def edit_stuff_dialogue(name, mystuff: MyStuffs, file):
    print(
        f"""
        ==============================
        =======   Edit Stuff   =======
        ==============================

{mystuff.get_stuff(name)}


        """
    )

    edits_map = dict()
    enc_key = None

    # Name
    new_name = input("Change name? Enter to skip -> ")
    if new_name:
        edits_map["name"] = new_name

    # Description
    des = input("Edit description? Enter to skip -> ")
    if des:
        edits_map["description"] = des

    # Attributes
    attr_map = dict()
    prompt = input("[A]dd/[E]dit/[R]emove attribtues? Enter to skip -> ")
    while prompt:
        if prompt == "R":
            key = input("Attribute to remove -> ")
            attr_map[key] = None
        elif prompt == "A" or prompt == "E":
            key = input("Attribte name -> ")
            value = input("Attribute value -> ")
            attr_map[key] = value
        else:
            prompt = input("Try again. [A]dd/[E]dit/[R]emove attribtues? Enter to skip -> ")
            continue
        prompt = input("[A]dd/[E]dit/[R]emove attribtues? Enter to skip -> ")
    if len(attr_map) > 0:
        edits_map["attributes"] = attr_map

    # Secrete attribtes
    sec_attr_map = dict()
    prompt = input("[A]dd/[E]dit/[R]emove encrypted attribtues? Enter to skip -> ")
    while prompt:
        if prompt == "R":
            key = input("Encrypted attribute to remove -> ")
            sec_attr_map[key] = None
        elif prompt == "A" or prompt == "E":
            key = input("Encrypted attribte name -> ")
            value = input("Encrypted attribte value -> ")
            enc_key = input("Encryption key -> ")
            sec_attr_map[key] = value
        else:
            prompt = input("[A]dd/[E]dit/[R]emove encrypted attribtues? Enter to skip -> ")
            continue
        prompt = input("[A]dd/[E]dit/[R]emove encrypted attribtues? Enter to skip -> ")
    if sec_attr_map:
        edits_map["encrypted_attributes"] = sec_attr_map

    mystuff.edit_stuff(name, encryption_key=enc_key, verbose=False, **edits_map)

    return name, "SM"


def inspect_children(name, mystuff: MyStuffs, file):
    print(mystuff.get_children(name))
    time.sleep(0.5)
    return name, "SM"


def inspect_stuff(name, mystuff: MyStuffs, file):
    print(mystuff.get_stuff(name))
    time.sleep(0.5)
    return name, "SM"


def inspect_neighbors(name, mystuff: MyStuffs, file):
    print(mystuff.get_neighbors(name))
    time.sleep(0.5)
    return name, "SM"


def inspect_parents(name, mystuff: MyStuffs, file):
    print(mystuff.get_parents(name))
    time.sleep(0.5)
    return name, "SM"


def remove_stuff_dialogue(name, mystuff: MyStuffs, file):
    print(
        f"""
        ==============================
        ======   Remove Stuff   ======
        ==============================
         - [C]ancel
         - [R]emove
         (This action cannot be undone)

{mystuff.get_stuff(name)}


        """
    )
    allowed_prompts = ["C", "R"]
    prompt = input("Your input -> ")
    while prompt not in allowed_prompts:
        prompt = input("Try again. Your input -> ")

    if prompt == "R":
        mystuff.remove_stuff(name)
        
    return "M"