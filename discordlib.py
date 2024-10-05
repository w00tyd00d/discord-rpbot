import discord, math

from strlib import *
from characterlib import Character

embed_thumbnail = "https://i.imgur.com/jrDS0br.png"


def create_roll_embed(character, dice_type: int, rolls: list[int], selection: list[int] = None, modifier: int|str = None, prof: int|str = None) -> discord.Embed:
    """
    Creates and returns an embed to display the results of a roll command.

    Params:
        rolls: This list of resulting rolls made
        selection: The filtered selection, if one exists
        modifier: The additional modifier, if one exists

    Returns:
        discord.Embed: A rich discord embed object containing the results of the
            roll command
    """

    skill = get_lazy_key(skill_keys, prof, 4)
    roll_type = f"D{dice_type} "
    
    if skill:
        roll_type = f"{skill.capitalize()}\n"
    elif modifier and (key := get_lazy_key(stat_keys, modifier)):
        roll_type = f"{key.capitalize()}\n"

    group = selection if selection is not None else rolls
    color = discord.Color.dark_gold() if 20 in group else discord.Color.blue()
    
    if (dice_type == 20 and
        color != discord.Color.dark_gold() and
        1 in group):
            color = discord.Color.dark_red()

    embed = discord.Embed(
        title=f"{roll_type}Roll Results",
        description=", ".join([str(n) for n in rolls]),
        color=color
    )
    
    embed.set_thumbnail(url=embed_thumbnail)

    if selection:
        embed.add_field(name="Selection", value=", ".join([str(n) for n in selection]))
    
    prof_mod = 0
    
    if modifier is not None or prof is not None:
        modstr = ""

        # Stat modifier
        if type(modifier) is str and character:
            stat = get_lazy_key(stat_keys, modifier)
            modifier = character.get_stat_modifier(stat)
            modstr += f"{modifier:+} ({stat.upper()[:3]})\n"

        elif type(prof) is str and character:
            stat = get_lazy_key(stat_keys, skill_keys[skill])
            modifier = character.get_stat_modifier(stat)
            modstr += f"{modifier:+} ({stat.upper()[:3]})\n"

        elif modifier is not None and type(modifier) is int:
            modstr = f"{modifier:+}"
        
        # Proficiency modifier
        if skill and character and (prof_lvl := character.get_proficiency(skill)) > 0:
            prof_mod = character.get_proficiency_modifier(skill)
            modstr += f"{prof_mod:+} ({"EXP" if prof_lvl > 1 else "PRO"})"

        if modstr:
            embed.add_field(name="Modifier", value=modstr)
    
    if modifier is None or not type(modifier) is int:
        # w00t: Hard set modifier to 0 for sum calculation
        modifier = 0

    result = sum(selection) if selection else sum(rolls)
    total = result + modifier + prof_mod
    embed.add_field(name="Result", value=f'{total}', inline=False)
    
    return embed


def create_stat_roll_embed(rolls: list[list], selections: list[list]) -> discord.Embed:
    """
    Creates and returns an embed to display the results of a roll stats command.

    Params:
        rolls: This list of each resulting roll made for each stat
        selections: The filtered selection of each stat roll

    Returns:
        discord.Embed: A rich discord embed object containing the results of the
            roll stats command
    """
    
    desc_string = "\n".join([", ".join([str(n) for n in roll]) for roll in rolls])
    
    embed = discord.Embed(
        title="Stat Roll Results",
        description=desc_string,
        color=discord.Color.blue()
    )
    
    embed.set_thumbnail(url=embed_thumbnail)

    selstr = "\n".join([", ".join([str(n) for n in roll]) for roll in selections])
    result = ", ".join([str(sum(r)) for r in selections])
    
    embed.add_field(name="Selection", value=selstr)
    embed.add_field(name="Result", value=result, inline=False)
    
    return embed


def create_character_embed(character) -> discord.Embed:
    """
    Creates and returns an embed to display the player's character stats.

    Params:
        character: The character object wished to be inspected

    Returns:
        discord.Embed: A rich discord embed object containing the data of
            a character
    """
    
    embed = discord.Embed(
        title=character.name,
        description=f"Level {character.level} {character.job}",
        color=discord.Color.blue()
    )
    
    embed.set_thumbnail(url=embed_thumbnail)
    
    embed.add_field(name="Strength",        value=f"{character.strength} ({character.get_stat_modifier("strength"):+})")
    embed.add_field(name="Intelligence",    value=f"{character.intelligence} ({character.get_stat_modifier("intelligence"):+})")
    
    embed.add_field(name=" ", value=" ", inline=False)
    
    embed.add_field(name="Dexterity",       value=f"{character.dexterity} ({character.get_stat_modifier("dexterity"):+})")
    embed.add_field(name="Wisdom",          value=f"{character.wisdom} ({character.get_stat_modifier("wisdom"):+})")
    
    embed.add_field(name=" ", value=" ", inline=False)
    
    embed.add_field(name="Constitution",    value=f"{character.constitution} ({character.get_stat_modifier("constitution"):+})")
    embed.add_field(name="Charisma",        value=f"{character.charisma} ({character.get_stat_modifier("charisma"):+})")
    
    embed.add_field(name=" ", value=" ", inline=False)

    saving_throws = "\n".join(get_lazy_key(stat_keys, stat).capitalize() for stat in job_keys[character.job]["saving_throws"])
    proficiencies = "\n".join(f"{prof.capitalize()}{" (EXP)" if character.get_proficiency(prof) == 2 else ""}" for prof in character.proficiencies.keys())
    prof_bonus = Character.proficiency_calculation(character.level)

    embed.add_field(name="Saving Throws",   value=f"{saving_throws}\n({prof_bonus:+})")
    embed.add_field(name="Proficiencies",   value=proficiencies)
    
    return embed


async def send_message(channel: discord.GroupChannel, msg: str, embed: discord.Embed = None):
    if channel is None:
        print("Error: Channel does not exist.")
        return
    await channel.send(msg, embed=embed)


async def send_direct_message(user: discord.Member, msg: str, embed: discord.Embed = None):
    await user.create_dm()
    await send_message(user.dm_channel, msg, embed=embed)