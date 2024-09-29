import discord, json, os, re

from pathlib import Path
from discord.ext import tasks, commands
from random import randint

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


# parse input to return "dice", "dice_amount", "low or high", and "selection"
def parsing(to_roll, choice = None):
    errors=[]
    #parses to_roll to extract dice and dice_amount of dice
    match_res = re.match(r"(\d+)*[a-z|A-Z]+(\d+)", to_roll)
    if match_res is None:
        return "Error: Invalid dice roll"
    dice_amount, dice_type = map(int, match_res.group(1, 2))
    dice_amount = 1 if dice_amount == None else dice_amount
    if dice_amount is None:
        return "Error: No dice included in input"

    # filter for if no choice is provided
    if choice is None:
        hi_lo = None
        selection = dice_amount
    else:
        choice = choice.lower()
        if len(choice) == 1:
            return "Error: Selection string not accepted ensure both l or h and a number"
        match choice:
            case 'adv', 'advantage', 'ad':
                hi_lo = 'h'
                selection = 1
                dice_amount = 2
            case 'dis', 'disadvantage', 'di', 'disadv':
                hi_lo = 'l'
                selection = 1
                dice_amount = 2
            case _:
                if choice.startswith('h') or choice.endswith('h'):
                    hi_lo = 'h'
                elif choice.startswith('l') or choice.endswith('l'):
                    hi_lo = 'l'
                else:
                    return"Error: incorrect letter chosen, please ensure either l or h is at the start or end of string"

                choice_res = re.findall(r'\d+', choice)
                if len(choice_res)>1:
                    return "Error: Selection string not accepted"
                else:
                    
                    selection = int(choice_res[0])

                if selection > dice_amount:
                    print("Error: Not enough dice rolled for selection")
                    selection = min(dice_amount, selection)

    return dice_amount, dice_type, hi_lo, selection

def filtering(rolls, hi_lo, selection):
    # Reduce the selection of rolled dice based on parameters
    selected = sorted(rolls, reverse = True if hi_lo == 'h' else False)[:selection]
    return selected

# dice_amount: int showing amount of total dice to be rolled
# dice_type: int the type of dice to be rolled as an integer signifying number of faces of dice
def rolling_time(dice_amount, dice_type):
    return [randint(1, dice_type) for _ in range(dice_amount)]    

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
    await send_message(ctx.channel, "Test successful!")


@bot.command(name="dm")
async def register_dm(ctx, user):
    pass


@bot.command(name="roll")
async def roll_dice(ctx, to_roll, choice = None):
    parsed = parsing(to_roll, choice)
    if parsed[0:5] == 'Error':
        await send_message(ctx.channel, parsed)
    else:
        dice_amount, dice_type, hi_lo, selection = parsed
        rolls = rolling_time(dice_amount, dice_type)
        if hi_lo is None:
            await send_message(ctx.channel, f'Rolled dice output: {rolls}, Sum of rolls: {sum(rolls)}')
        else:
            selected = filtering(rolls, hi_lo, selection)
            await send_message(ctx.channel, f'Selected dice: {selected}, Sum of selected dice: {sum(selected)}, every dice outcome:{rolls}')
    pass

@bot.command(name="rollstats")
async def roll_stats(ctx):
    rolls = []
    for _ in range(0,6):
        rolls = rolling_time(4, 6)
        selected = filtering(rolls, 'h', 3)
        await send_message(ctx.channel, f'Stats total: {sum(selected)}, rolled dice: {rolls}, dice selected (highest 3): {selected}')

@bot.command(name="rolldm")
async def roll_dice_dm(ctx, to_roll, choice = None):
    pass

if __name__ == "__main__":
    bot.run(settings.discord_token)