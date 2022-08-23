import interactions
from interactions.ext.paginator import Page, Paginator
import random
import asyncio

import cypher
import fun
import secrets

token = secrets.token()
bot = interactions.Client(token=token)

# Roll a d20 with Cypher formatting
@bot.command(
    name="roll",
    description="Roll for it!",
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

# Roll xdx
@bot.command(
    name="dice",
    description="Roll xdx",
    options = [
        interactions.Option(
            name="number",
            description="Number of dice",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
        interactions.Option(
            name="sides",
            description="Number of sides",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
    ],
)
async def dice(ctx: interactions.CommandContext, number: int, sides: int):
    output = cypher.roll(number, sides)
    await ctx.send(output)

# Roll a random cypher from dataframe
@bot.command(
    name="cypher",
    description="Rolls a random tropey cypher",
)
async def roll_cypher(ctx: interactions.CommandContext):
    output = cypher.print_cypher()
    await ctx.send(output)

# Look up a specific Cypher ability
# This is currently case-sensitive (and spelling sensitive)
@bot.command(
    name="ability",
    description="Ability lookup",
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

# Look at a specific character sheet
# Sometimes we don't want the full sheet,
# so this first one is just for stat pools.
@bot.command(
    name="status",
    description="View character status",
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def status(ctx: interactions.CommandContext, character: str):
    output = cypher.profile(character)
    await ctx.send(output)

# Sometimes, we DO want the full character sheet!
@bot.command(
    name="sheet",
    description="View full character sheet",
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
            Page(cypher.profile(character), title="Stats"),
            Page(cypher.skills(character), title="Skills"),
            Page(cypher.abilities(character), title="Abilities"),
            Page(cypher.equipment(character), title="Equipment"),
        ],
        author_only=True,
    ).run()

# Spend points
@bot.command(
    name="spend",
    description="Spend from pools",
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
    output = cypher.spend(name=character, might=might, speed=speed, intel=intellect, xp=xp)
    await ctx.send(output)

# Recover points
@bot.command(
    name="recover",
    description="Recover lost points",
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
    output = cypher.recover(name=character, might=might, speed=speed, intel=intellect)
    await ctx.send(output)

# Award XP
@bot.command(
    name="xp",
    description="Award XP",
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
    output = cypher.add_xp(name=character, amount=amount)
    await ctx.send(output)

# Advance
@bot.command(
    name="advance",
    description="Spend XP on advancement",
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
            description="If taking another advancement option from the rulebook, this isn't being tracked yet. Type whatever, just don't leave it blank.",
            type=interactions.OptionType.STRING,
            required=False,
        ),
    ],
)
async def advance(ctx: interactions.CommandContext, character: str, pools: str=None, effort: str=None, edge: str=None, skill: str=None, other: str=None):
    output = cypher.advance(name=character, pools=pools, effort=effort, edge=edge, skill=skill, other=other)
    await ctx.send(output)

# Rest
@bot.command(
    name="rest",
    description="Rest up",
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
    output = cypher.rest(name=character)
    await ctx.send(output)

# Set up a new character sheet
# I want to use a FORM for this. That would be cool!

# Edit character sheet
@bot.command(
    name="edit_inventory",
    description="Edit your inventory page on your character sheet",
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def edit_inventory(ctx: interactions.CommandContext, character: str):
    current_cypher = cypher.cypher_lookup(character)
    current_equipment = cypher.equip_lookup(character)
    name_component = interactions.TextInput(
        style = interactions.TextStyleType.SHORT,
        label = "Name: (Don't change this!)",
        custom_id = 'character',
        placeholder = character,
    )
    cypher_component = interactions.TextInput(
        style = interactions.TextStyleType.PARAGRAPH,
        label = "What cyphers are you currently holding?",
        custom_id = 'cypher_update',
        placeholder= current_cypher,
    )
    equip_component = interactions.TextInput(
        style = interactions.TextStyleType.PARAGRAPH,
        label = "What equipment do you have?",
        custom_id = 'equip_update',
        placeholder = current_equipment,
    )
    modal = interactions.Modal(
        title="Edit Inventory",
        custom_id = "edit_inventory",
        components = [name_component, cypher_component, equip_component],
    )
    await ctx.popup(modal)

@bot.modal("edit_inventory")
async def modal_response_inventory(ctx, character: str, cypher_update: str, equip_update: str):
    output = cypher.inventory_update(character, cypher_update, equip_update)
    await ctx.send(output)









# Message Dripper, FIFO, from txt file
# The "dripper" is started with a slash command,
# then spawns a button that can be pressed to continue
button = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label = "More!",
        custom_id="drip_button"
        )    
    
@bot.command(
    name="drip",
    description="Drip start!",
)
async def drip(ctx: interactions.CommandContext):
    dripfile = 'Assets/dripper.txt'
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
    dripfile = 'Assets/dripper.txt'
    with open(dripfile, 'r+', encoding='utf8') as f:
        firstline = f.readline()
        data = f.read()
        f.seek(0)
        f.write(data)
        f.truncate()
    await ctx.send(firstline, components=button)

# NLTK n-gram fake plot creator
@bot.command(
    name="plot",
    description="Generate random plotting things!",
    options = [
        interactions.Option(
            name="feeder",
            description="1 or 2 words to get it started (optional)",
            type=interactions.OptionType.STRING,
            required=False,
        ),
        interactions.Option(
            name="exclusions",
            description="What words would you like to exclude? (optional)",
            type=interactions.OptionType.STRING,
            required=False,
        ),
    ],
)
async def plot(ctx: interactions.CommandContext, feeder: str = None, exclusions: str = None):
    output = fun.two_seed_generator(feeder, exclusions)
    await ctx.send(output)

# Mad libs style string filler
@bot.command(
    name="filler",
    description="Fills instances of verb, noun, person, place, adj, adv, color, and emotion, mad lib style.",
    options = [
        interactions.Option(
            name="text",
            description="Full text to fill",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def filler(ctx: interactions.CommandContext, text: str):
    output = fun.filler(text)
    await ctx.send(output)

# Make the bot make the choices
bot.command(
    name="choose",
    description="Forces the bot to make the hard decisions... or any decision at all. Use | to separate choices",
    options = [
        interactions.Option(
            name="text",
            description="All choices, separated by |",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def choose(ctx: interactions.CommandContext, text: str):
    options = text.split("|")
    choice = random.choice(options)
    await ctx.send(choice)






bot.start()