from collections import defaultdict
from copy import deepcopy
from encrypt import encrypt

class Stuff():

    def __init__(self, name: str, description: str="", 
                 state_dict: dict=None, encrypt_func=encrypt) -> None:
        self.name = name.upper()
        self.description = description
        self.encrypt_func = encrypt_func
        self.attributes = dict()
        self.encrypted_attributes = dict()
        self.all_categories = ("name", "description", 
                               "encrypt_func", "attributes", 
                               "encrypted_attributes")

        if state_dict != None:
            if type(state_dict) != dict:
                raise TypeError("Only accept `state_dict` as dictionaries.")
            
            self.name = state_dict["name"]
            self.description = state_dict["description"]
            self.attributes = state_dict["attributes"]
            self.encrypted_attributes = state_dict["encrypted_attributes"]


    def get_name(self) -> str:
        return self.name

    
    def get_description(self) -> str:
        return self.description

    
    def get_attributes(self) -> dict:
        return self.attributes


    def get_secret_attributes(self) -> dict:
        return self.encrypted_attributes


    def get_info(self) -> dict:
        info = dict()
        info["name"] = self.name
        info["description"] = self.description
        info["attributes"] = self.attributes
        info["encrypted_attributes"] = self.encrypted_attributes
        return info


    def edit_name(self, new_name: str) -> None:
        self.name = new_name.upper()

    
    def edit_description(self, new_description: str) -> None:
        self.description = new_description


    def remove_attribute(self, key: str) -> None:
        self.attributes.pop(key, None)


    def remove_secret_attribute(self, key: str) -> None:
        self.encrypted_attributes.pop(key, None)


    def add_attribute(self, key: str, value: str) -> None:
        self.attributes[key] = value


    def add_attributes(self, key_value_pairs: dict) -> None:
        for key, value in key_value_pairs.items():
            self.attributes[key] = value


    def add_secret_attribute(self, key: str, value: str,
                              encryption_key: str) -> None:
        encrypted_value = encrypt(value, encryption_key)
        self.encrypted_attributes[key] = encrypted_value


    def add_secret_attributes(self, key_value_pairs: dict, 
                              encryption_key: str) -> None:
         for key, value in key_value_pairs.items():
            self.add_secret_attribute(key, value, encryption_key)


    def __repr__(self) -> str:
        return "Stuff<" + self.name + ">"


    def __str__(self) -> str:
        str = self.name
        if self.description or self.attributes:
            str += "\n"+"="*len(self.name)
        if self.description:
            str += "\n" + self.description
        if self.attributes:
            for k,v in self.attributes.items():
                str += "\n - " + k + ": " + v
        if self.encrypted_attributes:
            str += "\n"+"!!Encrypted!!"
            for k,v in self.encrypted_attributes.items():
                str += "\n - " + k + ": " + v
        return str


class MyStuffs():

    def __init__(self, state_dict: dict=None) -> None:
        self.stuffs = dict()
        self.outgoing_from = defaultdict(list)
        self.pointing_into = defaultdict(list)
        self.unsaved_changes = dict()

        if state_dict != None:
            if type(state_dict) != dict:
                raise TypeError("Only accept `state_dict` as dictionaries.")

            expanded_stuffs = state_dict["stuffs"]
            for name, stuff_info in expanded_stuffs.items():
                self.stuffs[name] = Stuff(name, state_dict=stuff_info)

            self.outgoing_from = state_dict["outgoing_from"]
            self.pointing_into = state_dict["pointing_into"]

    # =========================
    # ========== GET ==========
    
    def get_stuff(self, name: str) -> Stuff:
        if name not in self.stuffs:
            raise KeyError(f"Stuff wth name {name} not found.")
        return self.stuffs[name]


    def get_stuff_info(self, name: str) -> dict:
        return self.get_stuff(name).get_info()


    def get_neighbors(self, name: str) -> dict:
        if name not in self.stuffs:
            raise KeyError(f"Stuff wth name {name} not found.")
        neighbors = set()
        neighbors = neighbors.union(self.outgoing_from[name])
        neighbors = neighbors.union(self.pointing_into[name])
        # TODO: implement for connection length > 1
        
        result = dict()
        for node in neighbors:
            result[node] = self.stuffs[node]

        return result


    def get_children(self, parent_name: str) -> dict:
        if parent_name not in self.stuffs:
            raise KeyError(f"Stuff wth name {parent_name} not found.")
        # TODO: implement for connection length > 1

        children_name = self.outgoing_from[parent_name]
        children = dict()
        for child_name in children_name:
            children[child_name] = self.stuffs[child_name]

        return children

    
    def get_parents(self, child_name: str) -> dict:
        if child_name not in self.stuffs:
            raise KeyError(f"Stuff wth name {child_name} not found.")
        # TODO: implement for connection length > 1

        parents_name = self.pointing_into[child_name]
        parents = dict()
        for parent_name in parents_name:
            parents[parent_name] = self.stuffs[parent_name]

        return parents


    def get_children_parents(self, name: str, verbose=False) -> tuple:
        children = self.outgoing_from[name]
        parents = self.pointing_into[name]

        if verbose and len(children) > 0:
            print(f"Effected children: {children}.")
        if verbose and len(parents) > 0:
            print(f"Effected parents: {parents}.")
        
        return children, parents


    def get_state_dict(self) -> dict:

        def expand_stuffs(dict: dict) -> dict:
            if len(dict) == 0:
                return {}
            new_dict = {}
            for k, v in dict.items():
                v_info = v.get_info()
                new_dict[k] = v_info
            return new_dict

        state_dict = dict()
        expaneded_stuffs = expand_stuffs(self.stuffs)
        state_dict["stuffs"] = expaneded_stuffs
        state_dict["outgoing_from"] = self.outgoing_from
        state_dict["pointing_into"] = self.pointing_into
        return state_dict
    
    # =========================
    # ========== ADD ==========

    def add_stuff(self, stuff:Stuff) -> None:
        name = stuff.get_name()

        if name in self.stuffs:
            raise KeyError(f"Duplicate name {stuff.get_name()}.")
        else:
            self.stuffs[name] = stuff


    def add_dependence(self, from_name: str, to_name: str) -> None:
        if from_name not in self.stuffs:
            raise KeyError(f"Stuff with name {from_name} not found.")
        if to_name not in self.stuffs:
            raise KeyError(f"Stuff with name {to_name} not found.")
        if from_name == to_name:
            raise ValueError("Cannot add dependence with itself.")
        self.outgoing_from[from_name].append(to_name)
        self.pointing_into[to_name].append(from_name)

    # =========================
    # ======== REMOVE =========
    
    def remove_dependence(self, from_name: str, to_name: str) -> None:
        if from_name not in self.stuffs:
            raise KeyError(f"Stuff with name {from_name} not found.")
        if to_name not in self.stuffs:
            raise KeyError(f"Stuff with name {to_name} not found.")
        
        self.outgoing_from[from_name].remove(to_name, None)
        self.pointing_into[to_name].remove(from_name, None)


    def remove_stuff(self, name: str, verbose=True) -> None:
        self.stuffs.pop(name, None)

        children, parents = self.get_children_parents(name, verbose=verbose)

        for child in children:
            self.remove_dependence(name, child)
        self.outgoing_from.pop(name, None)

        for parent in parents:
            self.remove_dependence(parent, name)
        self.pointing_into.pop(name, None)

        self.prune()

    # ==========================
    # ========== EDIT ==========

    def view_unsaved_changes(self) -> None:
        print("Unsaved changes. revert() to cancel, apply() to save.")
        for item in self.unsaved_changes.values():
            print(item[1], "\n")

    
    def edit_stuff(self, sname: str, encryption_key: str=None, verbose=True, **kwargs) -> None:
        '''
        Edit attributes of the Stuff with name `name`. To delete an
        attribute or an encrypted attribute, set the value of that
        attribute to be `None`. 
        '''
        if sname not in self.stuffs:
            raise KeyError(f"Stuff wth name {sname} not found.")
        allowed_categories = Stuff("").all_categories
        for category in kwargs.keys():
            if category not in allowed_categories:
                raise ValueError(f"Keyword argument {category} is not a valid field of a Stuff {allowed_categories}.")
        
        new_stuff = deepcopy(self.stuffs[sname])
        new_name = None
        new_edits = False

        for category, content in kwargs.items():

            if category == "name":
                if type(content) != str:
                    raise TypeError(f"Value for {category} should be a String.")
                if content == sname: continue
                elif content != sname and content in self.stuffs:
                    raise KeyError(f"Duplicate name {content}.")

                new_stuff.edit_name(content)
                new_name = content.upper()

            elif category == "description":
                if type(content) != str:
                    raise TypeError(f"Value for {category} should be a String.")
                if content == self.stuffs[sname].get_description(): continue

                new_stuff.edit_description(content)

            elif category == "encrypt_func":
                print("Edits to the encryption function are not supported.")

            elif category == "attributes":
                if type(content) != dict:
                    raise TypeError(f"Value for {category} should be a dictioncary.")
                if content == self.stuffs[sname].get_attributes(): continue

                for k, v in content:
                    if v == None and k in new_stuff.get_attributes():
                        new_stuff.remove_attribute(k)
                    else:
                        new_stuff.add_attribute(k, v)

            elif category == "encrypted_attributes":
                if type(content) != dict:
                    raise TypeError(f"Value for {category} should be a dictioncary.")
                for k, v in content.items():
                    if v == None and k in new_stuff.get_secret_attributes():
                        new_stuff.remove_secret_attribute(k)
                    elif encryption_key == None:
                        raise ValueError("Encryption key required.")
                    else:
                        new_stuff.add_secret_attribute(k, v, encryption_key)

            else:
                raise SystemError("An unexpected error occured.")

            new_edits = True
        
        if new_edits:
            self.unsaved_changes[sname] = (new_name, new_stuff)
            if verbose: self.view_unsaved_changes()
        else:
            self.unsaved_changes.pop(sname, None)
            if verbose: print("No new edits made.")
                

    def revert(self) -> None:
        self.unsaved_changes = dict()

    
    def apply(self, verbose=True) -> None:
        for name, (new_name, stuff) in self.unsaved_changes.items():
            children, parents = self.get_children_parents(name, verbose=verbose)
            if new_name != None:
                for child in children:
                    self.pointing_into[child].remove(name)
                    self.pointing_into[child].append(new_name)
                self.outgoing_from[new_name] = self.outgoing_from.pop(name)

                for parent in parents:
                    self.outgoing_from[parent].remove(name)
                    self.outgoing_from[parent].append(new_name)
                self.pointing_into[new_name] = self.pointing_into.pop(name)
            
            self.stuffs.pop(name)
            self.stuffs[new_name if new_name else name] = stuff

        self.unsaved_changes = {}

        self.prune()


    def prune(self) -> None:
        to_pop = {}
        for k, v in self.outgoing_from.items():
            if v == []:
                to_pop.add(k)
        for k in to_pop:
            self.outgoing_from.pop(k)

        to_pop = {}
        for k, v in self.pointing_into.items():
            if v == []:
                to_pop.add(k)
        for k in to_pop:
            self.pointing_into.pop(k)


    def __repr__(self) -> str:
        repr = "MyStuff: "
        for k in self.stuffs.keys():
            repr += "<" + k + ">  "
        repr += "\n"
        for parent, children in self.outgoing_from.items():
            repr += parent + " -> " + children.__repr__() + "\n"
        return repr