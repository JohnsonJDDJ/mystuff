from collections import defaultdict
from encrypt import encrypt

class Stuff():

    def __init__(self, name: str, description: str="", 
                 encrypt_func=encrypt) -> None:
        self.name = name
        self.description = description
        self.encrypt_func = encrypt_func
        self.attributes = dict()
        self.encrypted_attributes = dict()


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

    def __init__(self) -> None:
        self.stuffs = dict()
        self.outgoing_from = defaultdict(set)
        self.pointing_into = defaultdict(set)

    
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
        self.outgoing_from[from_name].add(to_name)
        self.pointing_into[to_name].add(from_name)


    def remove_stuff(self, name: str) -> None:
        self.stuffs.pop(name, None)
        self.outgoing_from.pop(name, None)
        self.pointing_into.pop(name, None)

    
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

    def __repr__(self) -> str:
        return "MyStuff: " + self.stuffs.__repr__()