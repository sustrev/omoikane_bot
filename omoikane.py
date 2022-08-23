import interactions
from interactions.ext.paginator import Page, Paginator
import random

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
            Page(cypher.notes(character), title="Notes"),
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
            description="If taking other advancement option, this isn't being tracked yet. Type anything (not blank!).",
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
@bot.command(
    name="setup",
    description="Create a new character",
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
    output = cypher.setup_character(name=name, full_name=full_name, desc=descriptor, ctype=ctype, focus=focus, flavor = flavor, m = might, s = speed, i = intellect, m_e = might_edge, s_e = speed_edge, i_e = intellect_edge)
    await ctx.send(output)

# Edit character sheet
# Edit Skills
@bot.command(
    name="edit_skills",
    description="Edit your skills page on your character sheet",
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def edit_skills(ctx: interactions.CommandContext, character: str):
    current_trained = cypher.trained_lookup(character)
    current_spec = cypher.spec_lookup(character)
    current_inability = cypher.inability_lookup(character)
    name_component = interactions.TextInput(
        style = interactions.TextStyleType.SHORT,
        label = "Name: (Don't change this!)",
        custom_id = 'character',
        value = character,
    )
    trained_component = interactions.TextInput(
        style = interactions.TextStyleType.PARAGRAPH,
        label = "Trained:",
        custom_id = 'trained_update',
        value = current_trained,
    )
    spec_component = interactions.TextInput(
        style = interactions.TextStyleType.PARAGRAPH,
        label = "Specialized:",
        custom_id = 'spec_update',
        value = current_spec,
    )
    inability_component = interactions.TextInput(
        style = interactions.TextStyleType.PARAGRAPH,
        label = "Inability:",
        custom_id = 'inability_update',
        value = current_inability,
    )
    modal = interactions.Modal(
        title="Edit Skills",
        custom_id = "edit_skills",
        components = [name_component, trained_component, spec_component, inability_component],
    )
    await ctx.popup(modal)

@bot.modal("edit_skills")
async def modal_response_skills(ctx, character: str, trained_update: str, spec_update: str, inability_update: str):
    output = cypher.skills_update(character, trained_update, spec_update, inability_update)
    await ctx.send(output)

# Edit Abilities
@bot.command(
    name="edit_abilities",
    description="Edit your abilities page on your character sheet",
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def edit_abilities(ctx: interactions.CommandContext, character: str):
    current_abilities = cypher.ability_lookup(character)
    name_component = interactions.TextInput(
        style = interactions.TextStyleType.SHORT,
        label = "Name: (Don't change this!)",
        custom_id = 'character',
        value = character,
    )
    abilities_component = interactions.TextInput(
        style = interactions.TextStyleType.PARAGRAPH,
        label = "Abilities:",
        custom_id = 'abilities_update',
        value = current_abilities,
    )
    modal = interactions.Modal(
        title="Edit Abilities",
        custom_id = "edit_abilities",
        components = [name_component, abilities_component],
    )
    await ctx.popup(modal)

@bot.modal("edit_abilities")
async def modal_response_abilities(ctx, character: str, abilities_update: str):
    output = cypher.ability_update(character, abilities_update)
    await ctx.send(output)

# Edit inventory
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
        value = character,
    )
    cypher_component = interactions.TextInput(
        style = interactions.TextStyleType.PARAGRAPH,
        label = "Cyphers:",
        custom_id = 'cypher_update',
        value = current_cypher,
    )
    equip_component = interactions.TextInput(
        style = interactions.TextStyleType.PARAGRAPH,
        label = "Equipment:",
        custom_id = 'equip_update',
        value = current_equipment,
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

# Edit notes page
@bot.command(
    name="edit_notes",
    description="Edit your notes page on your character sheet",
    options = [
        interactions.Option(
            name="character",
            description="What character?",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def edit_notes(ctx: interactions.CommandContext, character: str):
    current_notes = cypher.notes_lookup(character)
    name_component = interactions.TextInput(
        style = interactions.TextStyleType.SHORT,
        label = "Name: (Don't change this!)",
        custom_id = 'character',
        value = character,
    )
    notes_component = interactions.TextInput(
        style = interactions.TextStyleType.PARAGRAPH,
        label = "Notes:",
        custom_id = 'notes_update',
        value = current_notes,
    )
    modal = interactions.Modal(
        title="Edit Notes",
        custom_id = "edit_notes",
        components = [name_component, notes_component],
    )
    await ctx.popup(modal)

@bot.modal("edit_notes")
async def modal_response_notes(ctx, character: str, notes_update: str):
    output = cypher.ability_update(character, notes_update)
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