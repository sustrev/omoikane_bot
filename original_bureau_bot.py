import interactions
import cypher
import character_sheet
from interactions.ext.paginator import Page, Paginator
import random
import asyncio

token = 'OTU1OTIyNDAxODEwNTg3NzA5.YjouHA.vF0zcFkl9ko1iQNfjhT8W6P8mbM'
bot = interactions.Client(token=token)
guild_id=953355201824325722

@bot.command(
    name="roll_cypher",
    description="Rolls a random tropey cypher",
    scope=guild_id,
)
async def roll_cypher(ctx: interactions.CommandContext):
    output = cypher.print_cypher()
    await ctx.send(output)
    
@bot.command(
    name="ability",
    description="Ability lookup",
    scope=guild_id,
    options = [
        interactions.Option(
            name="text",
            description="What ability?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def ability(ctx: interactions.CommandContext, text: str):
    output = cypher.print_ability(text)
    await ctx.send(output)
    
@bot.command(
    name="roll",
    description="Roll for it!",
    scope=guild_id,
    options = [
        interactions.Option(
            name="difficulty",
            description="Difficulty Rating",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="training",
            description="How much training do you have?",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="assets",
            description="How many assets do you have?",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="effort",
            description="How much effort are you putting in?",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        
    ],
)
async def roll(ctx: interactions.CommandContext, difficulty: int = 0, training: int = 0, assets: int = 0, effort: int = 0):
    output = cypher.print_roll(difficulty, training, assets, effort)
    await ctx.send(output)
    
@bot.command(
    name="profile",
    description="View character sheet",
    scope=guild_id,
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def profile(ctx: interactions.CommandContext, character: str):
    output = character_sheet.profile(character)
    await ctx.send(output)
    
@bot.command(
    name="setup",
    description="Create a new character",
    scope=guild_id,
    options = [
        interactions.Option(
            name="name",
            description="Short name (for lookups)",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="full_name",
            description="Full name",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="descriptor",
            description="Descriptor",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="ctype",
            description="Type",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="focus",
            description="Focus",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="flavor",
            description="Flavor",
            type=interactions.OptionType.STRING,
            required=False,
        ),
        interactions.Option(
            name="might",
            description="Might Pool",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="speed",
            description="Speed Pool",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="intellect",
            description="Intellect Pool",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="might_edge",
            description="Might Edge",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="speed_edge",
            description="Speed Edge",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="intellect_edge",
            description="Intellect Edge",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
    ],
)
async def setup(ctx: interactions.CommandContext, name: str, full_name: str, descriptor: str, ctype: str, focus: str, flavor:str = "", might: int=8, speed: int=8, intellect: int=8, might_edge:int=0, speed_edge:int=0, intellect_edge:int=0):
    output = character_sheet.setup_character(name=name, full_name=full_name, desc=descriptor, ctype=ctype, focus=focus, flavor = flavor, m = might, s = speed, i = intellect, m_e = might_edge, s_e = speed_edge, i_e = intellect_edge)
    await ctx.send(output)
    
@bot.command(
    name="spend",
    description="Spend from pools",
    scope=guild_id,
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="might",
            description="How much might?",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="speed",
            description="How much speed?",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="intellect",
            description="How much intellect?",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="xp",
            description="How much XP?",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
    ],
)
async def spend(ctx: interactions.CommandContext, character: str, might: int=0, speed: int=0, intellect: int=0, xp: int=0):
    output = character_sheet.spend(name=character, might=might, speed=speed, intel=intellect, xp=xp)
    await ctx.send(output)
    
@bot.command(
    name="recover",
    description="Recover lost points",
    scope=guild_id,
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="might",
            description="How much might?",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="speed",
            description="How much speed?",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
        interactions.Option(
            name="intellect",
            description="How much intellect?",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
    ],
)
async def recover(ctx: interactions.CommandContext, character: str, might: int=0, speed: int=0, intellect: int=0):
    output = character_sheet.recover(name=character, might=might, speed=speed, intel=intellect)
    await ctx.send(output)
    
@bot.command(
    name="xp",
    description="Add XP!",
    scope=guild_id,
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="amount",
            description="How much XP?",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
    ],
)
async def xp(ctx: interactions.CommandContext, character: str, amount: int):
    output = character_sheet.add_xp(name=character, amount=amount)
    await ctx.send(output)

@bot.command(
    name="advance",
    description="Spend XP on advancement",
    scope=guild_id,
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="pools",
            description="If advancing pools, use format XXXX (example: mmsi)",
            type=interactions.OptionType.STRING,
            required=False,
        ),
        interactions.Option(
            name="effort",
            description="If advancing effort, type whatever here, just don't leave it blank.",
            type=interactions.OptionType.STRING,
            required=False,
        ),
        interactions.Option(
            name="edge",
            description="If advancing edge, type m, s, or i to choose.",
            type=interactions.OptionType.STRING,
            required=False,
        ),
        interactions.Option(
            name="skill",
            description="If advancing skill, this isn't being tracked yet. Type whatever, just don't leave it blank.",
            type=interactions.OptionType.STRING,
            required=False,
        ),
        interactions.Option(
            name="other",
            description="If advancing skill, this isn't being tracked yet. Type whatever, just don't leave it blank.",
            type=interactions.OptionType.STRING,
            required=False,
        ),
    ],
)
async def recover(ctx: interactions.CommandContext, character: str, pools: str=None, effort: str=None, edge: str=None, skill: str=None, other: str=None):
    output = character_sheet.advance(name=character, pools=pools, effort=effort, edge=edge, skill=skill, other=other)
    await ctx.send(output)
    

@bot.command(
    name="sheet",
    description="Improved character sheet",
    scope=guild_id,
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def sheet(ctx: interactions.CommandContext, character: str):
    await Paginator(
        client=bot,
        ctx=ctx,
        pages=[
            Page(character_sheet.profile(character), title="Stats"),
            Page(character_sheet.skills(character), title="Skills"),
            Page(character_sheet.abilities(character), title="Abilities"),
            Page(character_sheet.equipment(character), title="Equipment"),
        ],
        author_only=True,
    ).run()
    
button = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label = "More!",
        custom_id="drip_button"
        )    
    
@bot.command(
    name="drip",
    description="Drip start!",
    scope=guild_id,
)
async def drip(ctx: interactions.CommandContext):
    dripfile = 'dripper.txt'
    with open(dripfile, 'r+', encoding='utf8') as f:
        firstline = f.readline()
        data = f.read()
        f.seek(0)
        f.write(data)
        f.truncate()
    await ctx.send(firstline, components=button)
    
@bot.component("drip_button")
async def drip_button_response(ctx):
    await ctx.edit(components=None)
    dripfile = 'dripper.txt'
    with open(dripfile, 'r+', encoding='utf8') as f:
        firstline = f.readline()
        data = f.read()
        f.seek(0)
        f.write(data)
        f.truncate()
    await ctx.send(firstline, components=button)

@bot.command(
    name="rest",
    description="Rest up",
    scope=guild_id,
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def rest(ctx: interactions.CommandContext, character: str):
    output = character_sheet.rest(name=character)
    await ctx.send(output)
            
    
    
    
bot.start()