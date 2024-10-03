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


def is_lazy_key(tup: tuple, key: str) -> bool:
    """Checks if lazy key belongs to corresponding key set."""
    if not key or len(key) < 3:
        return False

    for k in tup:
        if k.startswith(key.lower()):
            return True
    return False