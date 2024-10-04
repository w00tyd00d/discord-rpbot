import discord, json, os

from discordlib import *
from dicelib import *
from pathlib import Path
from discord.ext import commands

class Struct:
    def __init__(self, data):
        self.__dict__.update(data)

class Character:
    def __init__(self, **data):
        self.player_id = data["player_id"]
        
        self.name = data["name"]
        self.job = data["job"]
        self.level = data["level"]

        self.strength = data["strength"]
        self.dexterity = data["dexterity"]
        self.constitution = data["constitution"]
        self.wisdom = data["wisdom"]
        self.intelligence = data["intelligence"]
        self.charisma = data["charisma"]

        self.proficiencies = data["proficiencies"]
    
    def get_proficiency(self, skill: str) -> int:
        if skill not in self.proficiencies:
            return 0
        return self.proficiencies[skill]
    
    def edit_data(self, key: str, val: str|int) -> None:
        if hasattr(self, key):
            if type(getattr(self, key, False)) != type(val):
                return
            setattr(self, key, val)
    
    def edit_proficiency(self, skill: str, val: int) -> None:
        if val == 0:
            self.proficiencies.pop(skill, None)
            return
            
        self.proficiencies[skill] = val
    
    def save(self):
        save_file = os.path.join(os.path.dirname(__file__), f"data/profiles/{self.player_id}.json")
        mode = "r+" if Path(save_file) else "w+"
        
        with open(save_file, mode) as f:
            profile = json.loads(f.read())

            if self.name not in profile.characters:
                profile.characters[self.name] = {}
            
            profile.characters[self.name].update(self.__dict__)

            f.write(json.dumps(profile))      


with open(os.path.join(os.path.dirname(__file__), "settings.json")) as f:
    settings = Struct(json.loads(f.read()))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

guild = None # set at on_ready event

save_file = os.path.join(os.path.dirname(__file__), "data/main.json")

# Serialized data
dungeon_master_id = None

"""
player_id: {
    current_character: str,
    characters: dict
}
"""
characters = {}


def save_data():
    with open(save_file, "w") as f:
        data = { 
            "DM": dungeon_master_id
        }

        f.write(json.dumps(data))


def load_data():
    if not Path(save_file).exists():
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


def profile_exists(id: int) -> str:
    return Path(f"data/profiles/{id}.json").exists()


def load_character(id: int, character: str = None):
    if not profile_exists(id):
        return

    with open(f"data/profiles/{id}.json", "r+"):
        f_data = f.read()
        if f_data == "": return
        data = json.loads(f_data)
    
        character = character if character else data["current_character"]
        if not character:
            return
        
        characters[id] = Character(**data["characters"][character])
        
        data["current_character"] = character
        f.write(json.dumps(data))


def get_character(id: int) -> Character:
    if id not in characters:
        load_character(id)
    
    if id in characters:
        return characters[id]
    
    return {}
    

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
async def roll_dice(ctx, op1 = None, op2 = None, op3 = None):
    string, embed = get_roll_results(op1, op2, op3)
    await send_message(ctx.channel, string, embed)


@bot.command(name="rolldm")
async def roll_dice_dm(ctx, op1 = None, op2 = None, op3 = None):
    string, embed = get_roll_results(op1, op2, op3)
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
