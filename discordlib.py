import discord

from strlib import *

embed_thumbnail = "https://i.imgur.com/jrDS0br.png"


def create_roll_embed(dice_type: str, rolls: list[int], selection: list[int] = None, modifier: int|str = None) -> discord.Embed:
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
    
    embed = discord.Embed(
        title=f"D{dice_type} Roll Results",
        description=", ".join([str(n) for n in rolls]),
        color=discord.Color.blue()
    )
    
    embed.set_thumbnail(url=embed_thumbnail)

    if selection:
        embed.add_field(name="Selection", value=", ".join([str(n) for n in selection]))
    
    if modifier is not None:
        if is_lazy_key(stat_keys, modifier):
            # w00t: ADD PROFILE SUPPORT HERE
            modstr = f"{0:+} ({modifier.upper()[:3]})"
            modifier = 0
        else:
            modstr = f"{modifier:+}"

        embed.add_field(name="Modifier", value=modstr)
    else:
        # w00t: Hard set modifier to 0 for sum calculation
        modifier = 0
    
    result = sum(selection) if selection else sum(rolls)
    embed.add_field(name="Result", value=f'{result + modifier}', inline=False)
    
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