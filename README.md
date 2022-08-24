# omoikane_bot
Discord bot to implement Monte Cook's Cypher TTRPG as well as a few other fun, engagement, and utility features

## Discord Bot Functions
To comply with Discord's bot interaction best practices, all bot functions are called via slash command and/or button integration. The following commands are available:
* /ability is a lookup utility for all abilities in the Cypher core rulebook. Please note that this is case-sensitive and spelling counts. The one exception is the ability "Blessings of the Gods" because the ability description is too verbose for Discord. 
* /advance manages the four advancements per tier. It keeps track of which type of advancement was taken, doesn't allow duplicates, and appropriately subtracts XP from a player's total. Once four advancements have been taken, advances tier level.
* /choose takes a string input with choices separated by `|` ("one|two|five") and returns one of the choices at random, for coin flips and other decision-making moments left up to chance.
* /cypher rolls a random cypher and level from a list of cyphers; the file `Cypher/Cyphers.csv` is what this is set to pull from. Currently, I'm using custom-made cinematic-flavored cyphers with ideas pulled from a selection of cypher cards from Metal Weave Games' "Subtle Cyphers Based on TV Tropes" with additional influence from tvtropes.com.
* /dice rolls xdx dice and provides a single numerical value. It does not break down full dice results, but it *does* add a bit of text when a "1" is rolled.
* /drip begins a first in-first out feed of the file `Assets/dripper.txt`, and then generates a "More!" button to iterate through the file line-by-line. I use this to "drip" world lore throughout the week to assist with engagement in the game server. Currently, this file includes text from a currently-running game.
* /edit_abilities brings up a modal form with current abilities filled in and allows for players to edit their list of abilities.
* /edit_inventory brings up a modal form with current inventory filled in and allows for players to edit their inventory (cyphers and equipment).
* /edit_notes brings up a modal form with current notes filled in and allows for players to edit their notes.
* /edit_skills brings up a modal form with current skills filled in and allows for players to edit their skills (trained, specialized, and inability).
* /recover allows players to regain points in their might, speed, or intellect pools after a rest or recovery ability. It does not allow a player to recover more points than their maximum pool value.
* /rest rolls 1d6 + character tier level. It does not track abilities/advancements that add additional recovery points per rest.
* /roll rolls a d20 with a Cypher-related printout. This can be used as a straight d20 roll without modifiers, or it can be used to calculate the roll with difficulty, training, assets, and effort. 
* /sheet pulls up a 5 page character sheet with a dropdown menu and button navigation. This is locked to the user who calls the function.
* /spend allows players to track points (might, speed, intellect, and XP) for ability and effort use, re-rolls, and taking damage.
* /status pulls up just the first page of the character sheet for current stats without the additional navigation to other pages, for quick reference.
* /xp awards XP! 

![Cypher utility demo](https://github.com/sustrev/omoikane_bot/blob/main/Demo/cypher_util_demo.gif?raw=true)

## Requirements
This bot leans heavily on Python, Pandas, and local files. The following libraries must also be installed for the bot to run properly:
* interactions-py, found at https://github.com/interactions-py/library
* paginator, an extension of interactions-py, https://github.com/interactions-py/paginator

You will also need a Discord bot token; many tutorials are available regarding initial Discord bot setup.

## How to Run
After cloning this repository for yourself, you will need to additionally add a secrets.py to link your bot token (You *can* also hard-code your token in, but at your own risk. Protect your token!). I also suggest running this bot in a virtual environment so you can best manage library versions. Then, point your terminal to omoikane.py! Feel free to edit any files to fit your own purpose, from deleting the placeholder NPCs on the character spreadsheet to implementing your own lore/text for NLTK/dripper/etc. You are likewise free to use this code in whole or in part for your own personal projects.

## Credits
Much of this bot is created specifically for Monte Cook's Cypher system. This bot is meant to take the place of a basic VTT environment, so that games can be played solely on Discord. This bot is *not* meant to take place of supporting Monte Cook by purchasing a copy of the playbook. Therefore, I have purposely avoided providing features that would negate the necessity of the book during character creation and leveling up. Please visit [Monte Cook Games](https://www.montecookgames.com/store/product/cypher-system-rulebook-2/) to purchase your own copy, if you haven't already; it's integral to understanding the game utility features this bot provides. This bot is in no way affiliated with Monte Cook, this is just a profit-free passion project.

