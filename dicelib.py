import re

from strlib import *
from discordlib import create_roll_embed
from random import randint


def parse_dice_roll(to_roll: str) -> list[int]|str:
    """
    Parses the dice roll instruction and returns numeric values.

    Params:
        to_roll: The dice rolling instruction

    Returns:
        [int: Parsed dice roll instruction]
    """
    
    # Stistows: parses to_roll to extract dice and dice_amount of dice
    match_res = re.match(r"(\d+)*[dD]+(\d+)", to_roll)
    
    if match_res is None:
       return "Error: Invalid dice roll."
    
    return [int(n) if n is not None else 1 for n in match_res.group(1, 2)]
    

def filter_dice_rolls(rolls: list[int], choice: str) -> list[int]:
    """
    Filters out a selection of dice based on the choice argument given.

    Params:
        rolls: The rolled dice list generated by rolling_time
        choice: The choice operation given

    Returns:
        [int: Filtered dice roll result(s)]
    """

    # hi_lo, selection = None, 1

    res = re.match(r"([hlHL])(\d+)|(\d+)([hlHL])", choice)
    if not res:
        return "Error: Invalid choice parameter given."

    grp1, grp2 = res.group(1, 2)
    hi_lo, selection = (grp1, int(grp2)) if grp2.isdigit() else (grp2, int(grp1))
    
    hi_lo = res.group(1) if not res.group(1).isdigit() else res.group(2)
    selection = int(res.group(1)) if res.group(1).isdigit() else int(res.group(2))
        
    # Stistows: Reduce the selection of rolled dice based on parameters
    return sorted(rolls, reverse = True if hi_lo == 'h' else False)[:selection]


def rolling_time(dice_amount: int, dice_type: int) -> list[int]:
    """
    Returns a randomized list of integers based on the rolling parameters.

    Params:
        dice_amount: The amount of total dice to be rolled
        dice_type: int the type of dice to be rolled as an integer signifying number of faces of dice
    
    Returns:
        [int: Resulting dice roll(s)]
    """
    return [randint(1, dice_type) for _ in range(dice_amount)]    


def parse_arguments(op1: str, op2: str, op3: str) -> tuple:
    """
    Parses any additional operation given by a roll command and returns
    them in a deterministic order.

    Params:
        op1: The first operation given
        op2: The second operation given

    Returns:
        (bool, choice | None, modifier | None)
        
        bool:     Whether or not the operations given were valid
        choice:   The dice filtering option (if one is provided)
        modifier: The stat modifier (if one is provided)
    """
    to_roll, choice, modifier, skill = None, None, None, None
    
    def is_choice(op: str) -> bool:
        if ((op[0].isdigit() and op[-1] in {"h", "l"}) or
            (op[-1].isdigit() and op[0] in {"h", "l"})):
                return True
        return False

    def is_modifier(op: str) -> bool:
        if (get_lazy_key(stat_keys, op) or
            op.isdigit() or
            op[0] in {"+", "-"} and op[1:].isdigit()):
                return True
        return False

    for op in [op1, op2, op3]:
        if op is None: continue

        if re.match(r"(\d+)*[dD]+(\d+)", op) is not None:
            to_roll = op

        elif get_lazy_key(adv_keys, op) or get_lazy_key(dis_keys, op):
            if choice is not None:
                return [False]

            choice = "h1" if get_lazy_key(adv_keys, op) else "l1"
            to_roll = "2d20" if to_roll is None else to_roll
        
        elif get_lazy_key(skill_keys, op, 4):
            if skill is not None:
                return [False]
            
            skill = op
            
        elif is_choice(op):
            if choice is not None:
                return [False]
            choice = op
            
        elif is_modifier(op):
            if modifier is not None:
                return [False]
            modifier = op if get_lazy_key(stat_keys, op) else int(op)

        else:
            return [False]

    return [True, to_roll, choice, modifier, skill]


def get_roll_results(op1: str, op2: str, op3: str) -> tuple:
    """
    Returns the results of a roll command.

    Params:
        to_roll: The dice rolling instruction
        op1: The first extra operation
        op2: The second extra operation
    
    Returns:
        (str | None, discord.Embed | None)

        str: The string that will be printed directly within the replying msg
        discord.Embed: The rich embed object displaying the results
    """
    
    res = parse_arguments(op1, op2, op3)

    if not res[0]:
        return "Invalid extra operations.", None

    to_roll, choice, modifier, skill = res[1:]

    parsed = parse_dice_roll("d20" if to_roll is None else to_roll)
    
    if type(parsed) == str:
        return parsed, None

    rolls = rolling_time(*parsed)
    selected = filter_dice_rolls(rolls, choice) if choice else None
    embed = create_roll_embed(parsed[1], rolls, selected, modifier, skill)
    
    return "", embed