import pandas as pd
import random

cypher_df = pd.read_csv('cyphers.csv')
abilities_df = pd.read_excel('All_Abilities.xlsx')

def cypher_level_roller(str):
    n,s = str.split('d')
    n = int(n)
    s = int(s)
    rolls = []
    for i in range(n):
        rolls.append(random.randint(1, s))
    val = sum(rolls)
    return val

def print_cypher():
    cypher_num = random.randint(0, 54)
    cypher_row = cypher_df.iloc[[cypher_num]]
    cypher = cypher_row.values.tolist()[0]
    
    output = """>>> __**{}**__
*{}*

{}
Level: {}""".format(cypher[0], cypher[1], cypher[2], cypher_level_roller(cypher[3]))
    
    return output

def print_ability(ability):
    if ability not in abilities_df['Ability'].tolist():
        output = "Sorry, {} was not found. Check your spelling and capitalization, or tell Shrani to fix it.".format(ability)
        return output
    
    cost = abilities_df.loc[abilities_df['Ability'] == ability, 'Cost'].item()
    pool = abilities_df.loc[abilities_df['Ability'] == ability, 'Pool'].item()
    desc = abilities_df.loc[abilities_df['Ability'] == ability, 'Description'].item()
    
    if cost == 0:
        output = """>>> __**{}**__
{}""".format(ability, desc)
    
    else:
        output = """>>> __**{}**__
Cost: {} {}
{}""".format(ability, cost, pool, desc)
    
    return output

def list_ability():
    abilities_df = pd.read_excel('All_Abilities.xlsx')
    ability_list = abilities_df['Ability'].tolist()
    return ability_list

def print_roll(difficulty, training, assets, effort):

    valid_difficulty = {0:'Routine', 1:'Simple', 2:'Standard', 3:'Demanding', 4:'Difficult', 5:'Challenging', 6:'Intimidating', 7:'Formidable', 8:'Heroic', 9:'Immortal', 10:'Impossible'}
    valid_training = {-1:'Inability', 0:'Untrained', 1:'Trained', 2:'Specialized'}
    valid_assets = [0, 1, 2]
    valid_effort = [0, 1, 2, 3, 4, 5, 6]

    ## Sanity Checks
    if difficulty not in valid_difficulty.keys():
        output = "That is not a valid difficulty!"
        return output
    if training not in valid_training.keys():
        output = "That is not a valid skill level!"
        return output
    if assets not in valid_assets:
        output = "That is not a valid number of assets!"
        return output
    if effort not in valid_effort:
        output = "That is not a valid level of effort!"
        return output
    
    special_message = ""
    success = 0
    
    roll = random.randint(1,20)
    meet_or_beat = (difficulty - training - assets - effort) * 3
    if roll >= meet_or_beat:
        success = 1
    if roll == 1:
        special_message = "***GM INTRUSION...***"
    if roll == 17:
        special_message = "If this roll was an attack, deal +1 damage."
    if roll == 18:
        special_message = "If this roll was an attack, deal +2 damage."
    if roll == 19:
        special_message = "If this roll was an attack, deal +3 damage. Otherwise, you get a minor effect!"
    if roll == 20:
        special_message = "If this roll was an attack, deal +4 damage. Otherwise, you get a major effect!"
        
    if effort == 0:
        cost = 0
    if effort > 0:
        cost = (effort*2) + 1
        
    if special_message == "" and success == 1 and effort > 0:
        output = """>>> __**Roll Results:**__
Roll: {}
{}, {}, {} assets, {} effort
Number to Beat: {}... Success!
Pool Cost: {} - Edge""".format(roll, valid_difficulty[difficulty], valid_training[training], assets, effort, meet_or_beat, cost)
        return output
    
    if special_message == "" and success == 1 and effort == 0:
        output = """>>> __**Roll Results:**__
Roll: {}
{}, {}, {} assets, {} effort
Number to Beat: {}... Success!""".format(roll, valid_difficulty[difficulty], valid_training[training], assets, effort, meet_or_beat)
        return output
    
    if special_message == "" and success == 0 and effort > 0:
        output = """>>> __**Roll Results:**__
Roll: {}
{}, {}, {} assets, {} effort
Number to Beat: {}...
Pool Cost: {} - Edge""".format(roll, valid_difficulty[difficulty], valid_training[training], assets, effort, meet_or_beat, cost)
        return output
    
    if special_message == "" and success == 0 and effort == 0:
        output = """>>> __**Roll Results:**__
Roll: {}
{}, {}, {} assets, {} effort
Number to Beat: {}...""".format(roll, valid_difficulty[difficulty], valid_training[training], assets, effort, meet_or_beat)
        return output
    
    if special_message != "" and success == 1 and effort > 0:
        output = """>>> __**Roll Results:**__
Roll: {}
{}, {}, {} assets, {} effort
Number to Beat: {}... Success!
Pool Cost: {} - Edge
{}""".format(roll, valid_difficulty[difficulty], valid_training[training], assets, effort, meet_or_beat, cost, special_message)
        return output
    
    if special_message != "" and success == 1 and effort == 0:
        output = """>>> __**Roll Results:**__
Roll: {}
{}, {}, {} assets, {} effort
Number to Beat: {}... Success!
{}""".format(roll, valid_difficulty[difficulty], valid_training[training], assets, effort, meet_or_beat, special_message)
        return output
    
    if special_message != "" and success == 0 and effort > 0:
        output = """>>> __**Roll Results:**__
Roll: {}
{}, {}, {} assets, {} effort
Number to Beat: {}...
Pool Cost: {} - Edge
{}""".format(roll, valid_difficulty[difficulty], valid_training[training], assets, effort, meet_or_beat, cost, special_message)
        return output
    
    if special_message != "" and success == 0 and effort == 0:
        output = """>>> __**Roll Results:**__
Roll: {}
{}, {}, {} assets, {} effort
Number to Beat: {}...
{}""".format(roll, valid_difficulty[difficulty], valid_training[training], assets, effort, meet_or_beat, special_message)
        return output