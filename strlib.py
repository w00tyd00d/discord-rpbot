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

job_keys = {
    "Artificer":    {"saving_throws": ("CON", "INT")},
    "Barbarian":    {"saving_throws": ("STR", "CON")},
    "Bard":         {"saving_throws": ("DEX", "CHA")},
    "Cleric":       {"saving_throws": ("WIS", "CHA")},
    "Druid":        {"saving_throws": ("INT", "WIS")},
    "Fighter":      {"saving_throws": ("STR", "CON")},
    "Monk":         {"saving_throws": ("STR", "DEX")},
    "Paladin":      {"saving_throws": ("WIS", "CHA")},
    "Ranger":       {"saving_throws": ("STR", "DEX")},
    "Rogue":        {"saving_throws": ("DEX", "INT")},
    "Sorcerer":     {"saving_throws": ("CON", "CHA")},
    "Warlock":      {"saving_throws": ("WIS", "CHA")},
    "Wizard":       {"saving_throws": ("INT", "WIS")},
}


def get_lazy_key(data: tuple|dict, key: str, min_size = 3) -> str|None:
    """Checks if lazy key belongs to corresponding key set."""
    if not key or type(key) is not str or len(key) < min_size:
        return None

    for k in data:
        if k.startswith(key.lower()):
            return k
    
    return None