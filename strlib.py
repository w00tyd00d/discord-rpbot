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
    "Artificer":    {"saving_throws": ("constitutionstitution", "intelligence")},
    "Barbarian":    {"saving_throws": ("strengthength", "constitution")},
    "Bard":         {"saving_throws": ("dexterity", "charisma")},
    "Cleric":       {"saving_throws": ("wisdom", "charisma")},
    "Druid":        {"saving_throws": ("intelligence", "wisdom")},
    "Fighter":      {"saving_throws": ("strength", "constitution")},
    "Monk":         {"saving_throws": ("strength", "dexterity")},
    "Paladin":      {"saving_throws": ("wisdom", "charisma")},
    "Ranger":       {"saving_throws": ("strength", "dexterity")},
    "Rogue":        {"saving_throws": ("dexterity", "intelligence")},
    "Sorcerer":     {"saving_throws": ("constitution", "charisma")},
    "Warlock":      {"saving_throws": ("wisdom", "charisma")},
    "Wizard":       {"saving_throws": ("intelligence", "wisdom")},
}


def get_lazy_key(data: tuple|dict, key: str, min_size = 3) -> str|None:
    """Checks if lazy key belongs to corresponding key set."""
    if not key or type(key) is not str or len(key) < min_size:
        return None

    for k in data:
        if k.startswith(key.lower()):
            return k
    
    return None