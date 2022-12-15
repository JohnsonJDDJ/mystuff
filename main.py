from collections import defaultdict
from encrypt import encrypt

class Stuff():

    def __init__(self, name: str, description: str="", 
                 state_dict: dict=None, encrypt_func=encrypt) -> None:
        self.name = name
        self.description = description
        self.encrypt_func = encrypt_func
        self.attributes = dict()
        self.encrypted_attributes = dict()

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
        self.name = new_name

    
    def edite_description(self, new_description: str) -> None:
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
        return str


class MyStuffs():

    def __init__(self, state_dict: dict=None) -> None:
        self.stuffs = dict()
        self.outgoing_from = defaultdict(set)
        self.pointing_into = defaultdict(set)

        if state_dict != None:
            if type(state_dict) != dict:
                raise TypeError("Only accept `state_dict` as dictionaries.")

            expanded_stuffs = state_dict["stuffs"]
            for name, stuff_info in expanded_stuffs.items():
                self.stuffs[name] = Stuff(name, state_dict=stuff_info)

            self.outgoing_from = state_dict["outgoing_from"]
            self.pointing_into = state_dict["pointing_into"]

    
    def add_stuff(self, stuff:Stuff) -> None:
        if type(stuff) != Stuff:
            raise TypeError("Invalid type. Must be of type Stuff.")

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
        self.outgoing_from[from_name].add(to_name)
        self.pointing_into[to_name].add(from_name)


    def remove_stuff(self, name: str) -> None:
        self.stuffs.pop(name, None)
        self.outgoing_from.pop(name, None)
        self.pointing_into.pop(name, None)

    
    def get_stuff(self, name: str) -> Stuff:
        if name not in self.stuffs:
            raise KeyError(f"Stuff wth name {name} not found.")
        return self.stuffs[name]


    def get_info(self, name: str) -> dict:
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


    def __repr__(self) -> str:
        return "MyStuff: " + self.stuffs.__repr__()