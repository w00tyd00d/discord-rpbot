import discord, json, os

from discordlib import *
from dicelib import *
from pathlib import Path
from discord.ext import commands

class Struct:
    def __init__(self, data):
        self.__dict__.update(data)

with open(os.path.join(os.path.dirname(__file__), "settings.json")) as f:
    settings = Struct(json.loads(f.read()))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

guild = None # set at on_ready event

save_file = os.path.join(os.path.dirname(__file__), "data/main.json")

# Serialized data
dungeon_master_id = None


def save_data():
    with open(save_file, "w") as f:
        data = { 
            "DM": dungeon_master_id
        }

        f.write(json.dumps(data))


def load_data():
    if not Path(save_file):
        print(f"Invalid file path: {save_file}")
        return
        
    with open(save_file) as f:
        f_data = f.read()
        if f_data == "": return
        data = json.loads(f_data)

    global dungeon_master_id
    dungeon_master_id = data["DM"]


def get_member(id: int) -> discord.Member:
    """Returns a discord.Member object from the guild using a user id."""
    return guild.get_member(int(id))


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
    global guild
    guild = bot.get_guild(settings.guild_id)
    
    if settings.debug_mode:
        user = get_member(settings.debug_user_id)
        await send_direct_message(user, "Logged in!")
    
    load_data()
    

@bot.command()
async def test(ctx):
    await send_message(ctx.channel, "Test successful!")
    await send_message(ctx.channel, f"The current DM is : {get_member(dungeon_master_id).display_name}")


@bot.command(name="dm")
async def register_dm(ctx, user : discord.Member = None):
    user = user if user is not None else ctx.author

    global dungeon_master_id
    dungeon_master_id = user.id

    await send_message(ctx.channel, f"{user.display_name} is now the DM!")

    save_data()


@bot.command(name="roll")
async def roll_dice(ctx, to_roll = "d20", op1 = None, op2 = None):
    string, embed = get_roll_results(to_roll, op1, op2)
    await send_message(ctx.channel, string, embed)


@bot.command(name="rolldm")
async def roll_dice_dm(ctx, to_roll = "d20", op1 = None, op2 = None):
    string, embed = get_roll_results(to_roll, op1, op2)
    dm = get_member(dungeon_master_id)

    if ctx.author != dm or not embed:
        await send_direct_message(ctx.author, string, embed)

    if embed:
        string = f"{ctx.author.display_name} rolled the dice!\n" # ADD QUIP FUNCTION HERE
        await send_direct_message(dm, string, embed)
    

@bot.command(name="rollstats")
async def roll_stats(ctx):
    all_rolls = []
    all_selected = []
    
    for i in range(6):
        rolls = rolling_time(4, 6)
        selected = filter_dice_rolls(rolls, 'h3')

        all_rolls.append(rolls)
        all_selected.append(selected)
    
    embed = create_stat_roll_embed(all_rolls, all_selected)
    await send_message(ctx.channel, "", embed)


if __name__ == "__main__":
    bot.run(settings.discord_token)
