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

guild = None # set in on_ready

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


# parse input to return "dice", "dice_amount", "low or high", and "selection"
def parsing(to_roll, choice = None):
    
    #parses to_roll to extract dice and dice_amount of dice
    match_res = re.match(r"(\d+)*[a-z|A-Z]+(\d+)", to_roll)
    
    if match_res is None:
        return "Error: Invalid dice roll"
    
    dice_amount, dice_type = [int(n) if n is not None else 1 for n in match_res.group(1, 2)]
    
    # filter for if no choice is provided
    if choice is None:
        hi_lo = None
        selection = dice_amount
    else:
        choice = choice.lower()
        if len(choice) == 1:
            return "Error: Selection string not accepted ensure both l or h and a number"
        match choice:
            case 'adv' | 'advantage' | 'ad':
                hi_lo = 'h'
                selection = 1
                dice_amount = 2
                return dice_amount, dice_type, hi_lo, selection
            case 'dis' | 'disadvantage' | 'di' | 'disadv':
                hi_lo = 'l'
                selection = 1
                dice_amount = 2
                return dice_amount, dice_type, hi_lo, selection
            case _:
                if choice.startswith('h') or choice.endswith('h'):
                    hi_lo = 'h'
                elif choice.startswith('l') or choice.endswith('l'):
                    hi_lo = 'l'
                else:
                    return "Error: incorrect letter chosen, please ensure either l or h is at the start or end of string"

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
    

def get_member(id: int) -> discord.Member:
    return guild.get_member(int(id))


def check_extra_ops(op1, op2):
    choice, modifier = None, None

    for op in [op1, op2]:
        if op is None: continue
        
        if op.isdigit():
            if modifier is not None:
                return False, choice, modifier
            modifier = int(op)
        elif len(op) != 2:
            return False, choice, modifier
        
        if ((op[0].isdigit() and op[-1] in ("h", "l")) or
            (op[-1].isdigit() and op[0] in ("h", "l"))):
                if choice is not None:
                    return False, choice, modifier
                choice = op
        elif op[0] in ("+", "-") and op[1:].isdigit():
            if modifier is not None:
                return False, choice, modifier
            modifier = op

    return True, choice, modifier


def create_embed(rolls: list[int]) -> discord.Embed:
    pass
    
    # w00t: Keeping here for embed format reference.
    #  
    # embed = discord.Embed(
    #     title="Balatro: Golden Goblet",
    #     description=f"Week {week}\n\u200B",
    #     color=discord.Color.blue()
    # )
    #
    # embed.set_image(url = deck_images[deck])
    # embed.add_field(name="DECK", value=f"{deck} Deck")
    # embed.add_field(name="SEED", value=seed)
    #
    # return embed


def get_roll_results(to_roll, op1, op2):
    res, choice, modifier = check_extra_ops(op1, op2)

    if not res:
        return "Invalid extra operations.", None

    modifier = 0 if modifier is None else int(modifier)
    parsed = parsing(to_roll, choice)
    
    if parsed[0:5] == 'Error':
        return parsed, None

    dice_amount, dice_type, hi_lo, selection = parsed
    rolls = rolling_time(dice_amount, dice_type)
    
    if hi_lo is None:
        return f'Rolled dice output: {rolls}, Modifier is {modifier}, Sum of rolls: {sum(rolls) + modifier}', None
    else:
        selected = filtering(rolls, hi_lo, selection)
        return f'Selected dice: {selected}, Modifier is {modifier}, Sum of selected dice: {sum(selected) + modifier}, every dice outcome:{rolls}', None
    


async def send_message(channel: discord.GroupChannel, msg: str, embed: discord.Embed = None):
    if channel is None:
        print("Error: Channel does not exist.")
        return
    await channel.send(msg, embed=embed)


async def send_direct_message(user: discord.Member, msg: str, embed: discord.Embed = None):
    await user.create_dm()
    await send_message(user.dm_channel, msg, embed=embed)


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
async def roll_dice(ctx, to_roll, op1 = None, op2 = None):
    string, embed = get_roll_results(to_roll, op1, op2)
    await send_message(ctx.channel, string, embed)
    

@bot.command(name="rollstats")
async def roll_stats(ctx):
    for _ in range(6):
        rolls = rolling_time(4, 6)
        selected = filtering(rolls, 'h', 3)
        await send_message(ctx.channel, f'Stats total: {sum(selected)}, rolled dice: {rolls}, dice selected (highest 3): {selected}')
        

@bot.command(name="rolldm")
async def roll_dice_dm(ctx, to_roll, op1 = None, op2 = None):
    string, embed = get_roll_results(to_roll, op1, op2)
    dm = get_member(dungeon_master_id)

    if ctx.author != dm:
        await send_direct_message(ctx.author, string, embed)

    await send_direct_message(dm, string, embed)


if __name__ == "__main__":
    bot.run(settings.discord_token)
