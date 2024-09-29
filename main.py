import discord, json, os, re

from pathlib import Path
from discord.ext import tasks, commands

class Struct:
    def __init__(self, data):
        self.__dict__.update(data)

with open(os.path.join(os.path.dirname(__file__), "settings.json")) as f:
    settings = Struct(json.loads(f.read()))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

save_file = os.path.join(os.path.dirname(__file__), "data/main.json")

# Serialized data
dungeon_master = None


def save_data():
    with open(save_file, "w") as f:
        data = { 
            "DM": dungeon_master
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

    global dungeon_master
    dungeon_master = data["DM"]


async def send_message(channel: discord.GroupChannel, msg: str, embed: discord.Embed = None):
    await channel.send(msg, embed=embed)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
    if settings.debug_mode:
        await send_message("Logged in!")
    
    load_data()
    

@bot.command()
async def test(ctx):
    await send_message("Test successful!")


@bot.command(name="dm")
async def register_dm(ctx, user):
    pass


@bot.command(name="roll")
async def roll_dice(ctx, to_roll, choice = None):
    pass


@bot.command(name="rolldm")
async def roll_dice_dm(ctx, to_roll, choice = None):
    pass