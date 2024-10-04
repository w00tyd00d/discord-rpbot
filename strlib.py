adv_keys = ("advantage",)
dis_keys = ("disadvantage",)

stat_keys = (
    "strength", 
    "dexterity", 
    "constitution", 
    "wisdom", 
    "intelligence",
    "charisma"
)

skill_keys = {
    "athletics": "STR",
    
    "acrobatics": "DEX",
    "sleight of hand": "DEX",
    "stealth": "DEX",
    
    "arcana": "INT",
    "history": "INT",
    "investigation": "INT",
    "nature": "INT",
    "religion": "INT",
    
    "animal handling": "WIS",
    "insight": "WIS",
    "medicine": "WIS",
    "perception": "WIS",
    "survival": "WIS",

    "deception": "CHA",
    "intimidation": "CHA",
    "performance": "CHA",
    "persuasion": "CHA"
}


def get_lazy_key(data: tuple|dict, key: str, min_size = 3) -> str|None:
    """Checks if lazy key belongs to corresponding key set."""
    if not key or len(key) < min_size:
        return None

    for k in data:
        if k.startswith(key.lower()):
            return k
    
    return None