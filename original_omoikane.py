import interactions
import cypher
import generate_plot
import discord
#from interactions.ext.voice import VoiceState, VoiceClient
from interactions import Client
import random


import youtube_dl
ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': 'audio/%(title)s.%(ext)s'
}


token = 'ODcwMDgzNDAwNzAxMjA2NTQ4.YQHmUA.Jo8Ad4CJs5KJfzOVVEOR4B9ZvG0'
bot: Client = Client(token=token)
#Original instruction
#bot: VoiceClient = VoiceClient(token=token)

# arHSM fork
#bot: VoiceClient = VoiceClient(token=token)
#bot.load("interactions.ext.voice", voice_client=True)


### interactions slash commands

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
    output = generate_plot.roll(number, sides)
    await ctx.send(output)

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
    output = generate_plot.two_seed_generator(feeder, exclusions)
    await ctx.send(output)
    
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
    output = generate_plot.filler(filler)
    await ctx.send(output)
    
    
@bot.command(
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
    
    
@bot.command(
    name="process",
    description="does a secret thing",
    options = [
        interactions.Option(
            name="link",
            description="more secrets",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        ## Add to playlist stuff here???
    ],
)
async def process(ctx: interactions.CommandContext, link: str):
    output = "Working on it!"
    await ctx.send(output)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    
#@bot.command(
#    name="connect",
#    description="hoooopefully makes Omoikane connect to voice. no promises.",
#)
#async def connect(ctx: interactions.CommandContext, channel: interactions.Channel):
#    await bot.connect_vc(channel_id=int(channel.id), guild_id=int(ctx.guild_id), self_deaf=True, self_mute=False)






    
bot.start()