import discord

from strlib import *

embed_thumbnail = "https://i.imgur.com/jrDS0br.png"


def create_roll_embed(dice_type: int, rolls: list[int], selection: list[int] = None, modifier: int|str = None, prof: int|str = None) -> discord.Embed:
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
    roll_type = f"{skill.capitalize()}\n" if skill else f"D{dice_type} "

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
    
    plvl, pmod = 0, 0
    
    if modifier is not None or prof is not None:
        modstr = ""

        if type(modifier) == str:
            # w00t: ADD PROFILE SUPPORT HERE
            modstr += f"{0:+} ({modifier.upper()[:3]})\n"
            modifier = 0

        elif type(prof) == str:
            
            ability = skill_keys[skill]
            modstr += f"{0:+} ({ability.upper()[:3]})\n"

        elif modifier is not None:
            modstr = f"{modifier:+}"
        
        if skill and plvl > 0:
            # w00t: ADD PROFILE SUPPORT HERE
            modstr += f"{plvl*pmod:+} ({"PRO" if plvl == 1 else "EXP"})"

        embed.add_field(name="Modifier", value=modstr)
    
    if modifier is None:
        # w00t: Hard set modifier to 0 for sum calculation
        modifier = 0

    result = sum(selection) if selection else sum(rolls)
    total = result + modifier + (plvl * pmod)
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


async def send_message(channel: discord.GroupChannel, msg: str, embed: discord.Embed = None):
    if channel is None:
        print("Error: Channel does not exist.")
        return
    await channel.send(msg, embed=embed)


async def send_direct_message(user: discord.Member, msg: str, embed: discord.Embed = None):
    await user.create_dm()
    await send_message(user.dm_channel, msg, embed=embed)