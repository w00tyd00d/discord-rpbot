import json, math, os

from pathlib import Path

_characters = {}

class Character:
    def __init__(self, id, **data):
        self.player_id = id
        
        self.name = data["name"]
        self.job = data["job"]
        self.level = data["level"]

        self.strength = data["strength"]
        self.dexterity = data["dexterity"]
        self.constitution = data["constitution"]
        self.wisdom = data["wisdom"]
        self.intelligence = data["intelligence"]
        self.charisma = data["charisma"]

        self.proficiencies = data["proficiencies"]
    
    @staticmethod
    def proficiency_calculation(lvl: int) -> int:
        return ((lvl - 1) // 4 + 2)  
    
    def get_stat_modifier(self, stat: str) -> int:
        if not hasattr(self, stat):
            return 0
        lvl = getattr(self, stat)
        return min(10, max(math.floor((lvl - 10) / 2), -5))
    
    def get_proficiency(self, skill: str) -> int:
        return self.proficiencies.get(skill, 0)
    
    def get_proficiency_modifier(self, skill: str, force_lvl = None):
        return Character.proficiency_calculation(self.level) * self.get_proficiency(skill)

    def edit_data(self, key: str, val: str|int) -> None:
        if hasattr(self, key):
            attr = getattr(self, key, False)
            if attr is not None and type(attr) != type(val):
                return
            setattr(self, key, val)
            self.save()
    
    def edit_proficiency(self, skill: str, val: int) -> None:
        if val == 0:
            self.proficiencies.pop(skill, None)
            return
            
        self.proficiencies[skill] = val
        self.save()
    
    def save(self):
        save_file = os.path.join(os.path.dirname(__file__), f"data/profiles/{self.player_id}.json")
        mode = "w+" #"r+" if Path(save_file) else "w+"
        
        with open(save_file, mode) as f:
            profile = json.loads(f.read())

            if self.name not in profile.characters:
                profile.characters[self.name] = {}
            
            profile.characters[self.name].update(self.__dict__)

            f.write(json.dumps(profile))


def profile_exists(id: int) -> str:
    return Path(f"data/profiles/{id}.json").exists()


def load_character(id: int, character: str = None):
    if not profile_exists(id):
        return

    with open(f"data/profiles/{id}.json", "r+") as f:
        f_data = f.read()
        if f_data == "": return
        data = json.loads(f_data)
    
        character = character if character else data["current_character"]
        if not character: return
        
        _characters[id] = Character(id, **data["characters"][character])
        data["current_character"] = character

        f.seek(0)
        f.truncate()
        f.write(json.dumps(data))


def get_character(id: int) -> Character:
    if id not in _characters:
        load_character(id)
    
    if id in _characters:
        return _characters[id]
    
    return None