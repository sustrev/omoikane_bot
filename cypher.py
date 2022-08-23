import pandas as pd
import random
import ast

cypher_df = pd.read_csv('Cypher/Cyphers.csv')
abilities_df = pd.read_excel('Cypher/All_Abilities.xlsx')
character_sheet_path = 'Cypher/Character_Sheets.xlsx'

# For rolling a d20 with Cypher formatting
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

# For rolling xdx (nothing fancy here but crit failing)
def roll(num, sides):
    n = int(num)
    s = int(sides)
    rolls = []
    for i in range(n):
        rolls.append(random.randint(1, s))
    val = sum(rolls)
    if n == 1 and sum(rolls) == 1:
        return("Ouch, crit fail. You rolled a **1**. Better luck next time!")
    else:
        return("Rolling " + str(num) + "d" + str(sides) + ": **" + str(val) + "**")

# For rolling a random cypher from cypher_df
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

# For looking up a specific Cypher ability
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
    abilities_df = pd.read_excel(character_sheet_path)
    ability_list = abilities_df['Ability'].tolist()
    return ability_list

# For Cypher character sheet lookups
def profile(name):
    character_df = pd.read_excel(character_sheet_path)
    # Pretty-prints character profile
    full = character_df.loc[character_df['name'] == name, 'Full_Name'].item()
    desc = character_df.loc[character_df['name'] == name, 'Descriptor'].item()
    ctype = character_df.loc[character_df['name'] == name, 'Type'].item()
    focus = character_df.loc[character_df['name'] == name, 'Focus'].item()
    flav = character_df.loc[character_df['name'] == name, 'Flavor'].item()
    tier = character_df.loc[character_df['name'] == name, 'Tier'].item()
    effort = character_df.loc[character_df['name'] == name, 'Effort'].item()
    xp = character_df.loc[character_df['name'] == name, 'XP'].item()
    m_c = character_df.loc[character_df['name'] == name, 'Might_C'].item()
    m_p = character_df.loc[character_df['name'] == name, 'Might_P'].item()
    m_e = character_df.loc[character_df['name'] == name, 'Might_E'].item()
    s_c = character_df.loc[character_df['name'] == name, 'Speed_C'].item()
    s_p = character_df.loc[character_df['name'] == name, 'Speed_P'].item()
    s_e = character_df.loc[character_df['name'] == name, 'Speed_E'].item()
    i_c = character_df.loc[character_df['name'] == name, 'Int_C'].item()
    i_p = character_df.loc[character_df['name'] == name, 'Int_P'].item()
    i_e = character_df.loc[character_df['name'] == name, 'Int_E'].item()
    cond  = condition_lookup(name)
    
    output = """>>> __**{}**__
*{} {} who {}*
*{}*
__Tier: {}             Effort: {}             XP: {}__
Might     | {}     Pool: {}      Edge: {}
Speed     | {}     Pool: {}      Edge: {}
Intellect | {}     Pool: {}      Edge: {}
Condition: {}""".format(full, desc, ctype, focus, flav, tier, effort, xp, m_c, m_p, m_e, s_c, s_p, s_e, i_c, i_p, i_e, cond)
    
    return output

def condition_lookup(name):
    character_df = pd.read_excel(character_sheet_path)
    m_c = character_df.loc[character_df['name'] == name, 'Might_C'].item()
    s_c = character_df.loc[character_df['name'] == name, 'Speed_C'].item()
    i_c = character_df.loc[character_df['name'] == name, 'Int_C'].item()
    
    counter = 0
    
    if m_c == 0:
        counter += 1
    if s_c == 0:
        counter += 1
    if i_c == 0:
        counter += 1
        
    if counter == 0:
        condition = 'Hale'
    if counter == 1:
        condition = 'Impaired: Effort costs 1 extra point per level applied. Minor and major effects do not apply on your rolls.'
    if counter == 2:
        condition = 'Debilitated: You can only move, and only an immediate distance. If your Speed Pool is 0, you cannot move at all.'
    if counter == 3:
        condition = 'Dead.'
    if counter not in [0, 1, 2, 3]:
        condition = 'Lookup Failed'
        
    return condition

def skills(name):
    character_skills = pd.read_excel(character_sheet_path)
    # Pretty-prints skills
    full = character_skills.loc[character_skills['name'] == name, 'Full_Name'].item()
    train = character_skills.loc[character_skills['name'] == name, 'Trained'].item()
    spec = character_skills.loc[character_skills['name'] == name, 'Specialized'].item()
    inab = character_skills.loc[character_skills['name'] == name, 'Inability'].item()
    
    output = """>>> __**{}**__
Trained       | {}
Specialized | {}
Inability      | {}""".format(full, train, spec, inab)
    
    return output

def abilities(name):
    character_ab = pd.read_excel(character_sheet_path)
    # Pretty-prints abilities
    full = character_ab.loc[character_ab['name'] == name, 'Full_Name'].item()
    abilities = character_ab.loc[character_ab['name'] == name, 'Abilities'].item()
    
    output = """>>> __**{}**__
{}""".format(full, abilities)
    
    return output

def equipment(name):
    character_eq = pd.read_excel(character_sheet_path)
    # Pretty-prints equpiment
    full = character_eq.loc[character_eq['name'] == name, 'Full_Name'].item()
    cypher = character_eq.loc[character_eq['name'] == name, 'Cypher'].item()
    equip = character_eq.loc[character_eq['name'] == name, 'Equipment'].item()
    
    output = """>>> __**{}**__
Cypher     | {}
Equipment  | {}""".format(full, cypher, equip)
    
    return output

def notes(name):
    character_df = pd.read_excel(character_sheet_path)
    # Pretty-prints equpiment
    full = character_df.loc[character_df['name'] == name, 'Full_Name'].item()
    notes = character_df.loc[character_df['name'] == name, 'Notes'].item()
    
    output = """>>> __**{}**__
{}""".format(full, notes)
    
    return output


# For spending points
def spend(name, might=0, speed=0, intel=0, xp=0):
    character_df = pd.read_excel(character_sheet_path)
    m_c = character_df.loc[character_df['name'] == name, 'Might_C'].item()
    s_c = character_df.loc[character_df['name'] == name, 'Speed_C'].item()
    i_c = character_df.loc[character_df['name'] == name, 'Int_C'].item()
    xp_c = character_df.loc[character_df['name'] == name, 'XP'].item()
    
    new_mc = m_c - might
    new_sc = s_c - speed
    new_ic = i_c - intel
    new_xp = xp_c - xp
    
    if new_mc < 0 or new_sc < 0 or new_ic < 0 or new_xp < 0:
        output = "Spending failed: not enough funds!"
        return output
    
    else:
        character_df.loc[character_df['name'] == name, 'Might_C'] = new_mc
        character_df.loc[character_df['name'] == name, 'Speed_C'] = new_sc
        character_df.loc[character_df['name'] == name, 'Int_C'] = new_ic
        character_df.loc[character_df['name'] == name, 'XP'] = new_xp
        character_df.to_excel(character_sheet_path, index=False)
        output = "Character updated accordingly."
        return output

# For recovering points
def recover(name, might=0, speed=0, intel=0):
    character_df = pd.read_excel(character_sheet_path)
    m_c = character_df.loc[character_df['name'] == name, 'Might_C'].item()
    s_c = character_df.loc[character_df['name'] == name, 'Speed_C'].item()
    i_c = character_df.loc[character_df['name'] == name, 'Int_C'].item()
    
    new_mc = m_c + might
    new_sc = s_c + speed
    new_ic = i_c + intel
    
    m_p = character_df.loc[character_df['name'] == name, 'Might_P'].item()
    s_p = character_df.loc[character_df['name'] == name, 'Speed_P'].item()
    i_p = character_df.loc[character_df['name'] == name, 'Int_P'].item()
    
    if new_mc > m_p or new_sc > s_p or new_ic > i_p:
        output = "Recovery failed: Your pools won't hold those values!"
        return output
    
    else:
        character_df.loc[character_df['name'] == name, 'Might_C'] = new_mc
        character_df.loc[character_df['name'] == name, 'Speed_C'] = new_sc
        character_df.loc[character_df['name'] == name, 'Int_C'] = new_ic
        character_df.to_excel(character_sheet_path, index=False)
        output = "Character updated accordingly."
        return output

# For gaining XP
def add_xp(name, amount):
    character_df = pd.read_excel(character_sheet_path)
    xp_c = character_df.loc[character_df['name'] == name, 'XP'].item()
    new_xp = xp_c + amount
    character_df.loc[character_df['name'] == name, 'XP'] = new_xp
    character_df.to_excel(character_sheet_path, index=False)
    output = "XP awarded!"
    return output

# For using XP to advance
def advance(name, pools=None, effort=None, edge=None, skill=None, other=None):
    character_df = pd.read_excel(character_sheet_path)
    
    tier = character_df.loc[character_df['name'] == name, 'Tier'].item()
    effort_c = character_df.loc[character_df['name'] == name, 'Effort'].item()
    xp = character_df.loc[character_df['name'] == name, 'XP'].item()
    m_c = character_df.loc[character_df['name'] == name, 'Might_C'].item()
    m_p = character_df.loc[character_df['name'] == name, 'Might_P'].item()
    m_e = character_df.loc[character_df['name'] == name, 'Might_E'].item()
    s_c = character_df.loc[character_df['name'] == name, 'Speed_C'].item()
    s_p = character_df.loc[character_df['name'] == name, 'Speed_P'].item()
    s_e = character_df.loc[character_df['name'] == name, 'Speed_E'].item()
    i_c = character_df.loc[character_df['name'] == name, 'Int_C'].item()
    i_p = character_df.loc[character_df['name'] == name, 'Int_P'].item()
    i_e = character_df.loc[character_df['name'] == name, 'Int_E'].item()
    
    advance = character_df.loc[character_df['name'] == name, 'Advancement'].item()
    adv = ast.literal_eval(advance)
    
    requested_advs = []
    
    if pools is not None:
        requested_advs.append('pool')
    if effort is not None:
        requested_advs.append('effort')
    if edge is not None:
        requested_advs.append('edge')
    if skill is not None:
        requested_advs.append('skill')
    if other is not None:
        requested_advs.append('other')
        
    if len(requested_advs) > 3:
        output="Please only request 3 or fewer advancements at once."
        return output
    else:
        val=True
        
    ### Check adv against requested_advs
    for req in requested_advs:
        if req in adv:
            output="You've already chosen one of these advancements for this tier. Stopping."
            return output
    
    xp_needed = len(requested_advs) * 4
    if xp < xp_needed:
        output="You don't have enough XP to advance in this way!"
        return output
    else:
        val=True
        
    if 'pool' in requested_advs:
        if len(pools) == 4:
            m_a, s_a, i_a = pool_parser(pools)
            if m_a + s_a + i_a != 4:
                output="Pool input invalid, stopping."
                return output
            else:
                character_df.loc[character_df['name'] == name, 'Might_C'] = m_c + m_a
                character_df.loc[character_df['name'] == name, 'Speed_C'] = s_c + s_a
                character_df.loc[character_df['name'] == name, 'Int_C'] = i_c + i_a
                character_df.loc[character_df['name'] == name, 'Might_P'] = m_p + m_a
                character_df.loc[character_df['name'] == name, 'Speed_P'] = s_p + s_a
                character_df.loc[character_df['name'] == name, 'Int_P'] = i_p + i_a
                
                adv.append('pool')
                character_df.loc[character_df['name'] == name, 'Advancement'] = str(adv)
                
                xp = xp - 4
                character_df.loc[character_df['name'] == name, 'XP'] = xp
        else:
            output = "Pool input invalid, stopping."
            return output
    else:
        val=True
        
    if 'effort' in requested_advs:
        character_df.loc[character_df['name'] == name, 'Effort'] = effort_c + 1
        adv.append('effort')
        character_df.loc[character_df['name'] == name, 'Advancement'] = str(adv)
        xp = xp - 4
        character_df.loc[character_df['name'] == name, 'XP'] = xp
    else:
        val=True
        
    if 'edge' in requested_advs:
        if edge.lower() == 'm':
            character_df.loc[character_df['name'] == name, 'Might_E'] = m_e + 1
        if edge.lower() == 's':
            character_df.loc[character_df['name'] == name, 'Speed_E'] = s_e + 1
        if edge.lower() == 'i':
            character_df.loc[character_df['name'] == name, 'Int_E'] = i_e + 1
        
        adv.append('edge')
        character_df.loc[character_df['name'] == name, 'Advancement'] = str(adv)
        xp = xp - 4
        character_df.loc[character_df['name'] == name, 'XP'] = xp
    else:
        val=True
        
    if 'skill' in requested_advs:
        adv.append('skill')
        character_df.loc[character_df['name'] == name, 'Advancement'] = str(adv)
        xp = xp - 4
        character_df.loc[character_df['name'] == name, 'XP'] = xp
    else:
        val=True

    if 'other' in requested_advs:
        adv.append('other')
        character_df.loc[character_df['name'] == name, 'Advancement'] = str(adv)
        xp = xp - 4
        character_df.loc[character_df['name'] == name, 'XP'] = xp
    else:
        val=True
        
    if len(adv) >= 4:
        character_df.loc[character_df['name'] == name, 'Tier'] = tier + 1
        adv = adv[4:]
        character_df.loc[character_df['name'] == name, 'Advancement'] = str(adv)
    else:
        val=True
    
    character_df.to_excel(character_sheet_path, index=False)
    
    output = "Advancement complete!"
    return output

def pool_parser(adv_string):
    m = 0
    s = 0
    i = 0
    for n in adv_string.lower():
        if n == 'm':
            m += 1
        if n == 's':
            s += 1
        if n == 'i':
            i += 1
            
    return m,s,i

# For resting
def rest(name):
    character_df = pd.read_excel(character_sheet_path)
    tier = character_df.loc[character_df['name'] == name, 'Tier'].item()
    roll = random.randint(1,6)
    rest_amt = roll + tier
    rest_type = character_df.loc[character_df['name'] == name, 'Rest'].item()
    rest_msg = ""
    output = """>>> __**Rest Result:**__
Rest Duration Used: {}
Points Refreshed: {}
Please use `/recover` next to divide these points among your stat pools.
{}""".format(rest_type, rest_amt, rest_msg)
    
    character_df.loc[character_df['name'] == name, 'Rest'] = rest_cycle(rest_type)
    character_df.to_excel(character_sheet_path, index=False)
    
    return output

def rest_cycle(current):
    rest_type_list = ['1 Action', '10 Minutes', '1 Hour', '10 Hours']
    if current in rest_type_list:
        place = rest_type_list.index(current)
        if place < 3:
            next_rest = rest_type_list[place + 1]
        else:
            next_rest = rest_type_list[0]
    else:
        next_rest = rest_type_list[0]
    
    return next_rest

# For Cypher character sheet setup
def setup_character(name, full_name, desc, ctype, focus, flavor = "", m = 8, s = 8, i = 8, m_e = 0, s_e = 0, i_e = 0, train = 'None', spec = 'None', inability = 'None', ability_list = 'None', cypher = 'None', equip = 'None'):
    character_df = pd.read_excel(character_sheet_path)
    d = {'name':[name], 
        'Full_Name':[full_name], 
        'Descriptor':[desc], 
        'Type':[ctype], 
        'Focus':[focus], 
        'Flavor':[flavor], 
        'Tier':[1], 
        'Effort':[1], 
        'XP':[0], 
        'Might_C':[m], 
        'Might_P':[m], 
        'Might_E':[m_e], 
        'Speed_C':[s], 
        'Speed_P':[s], 
        'Speed_E':[s_e], 
        'Int_C':[i], 
        'Int_P':[i], 
        'Int_E':[i_e], 
        'Advancement':[[]],
        'Rest': ['1 Action'],
        'Trained': [train],
        'Specialized': [spec],
        'Inability': [inability],
        'Abilities': [ability_list],
        'Cypher': [cypher],
        'Equipment': [equip]}
    char_df = pd.DataFrame.from_dict(data=d)
    new_character_df = character_df.append(char_df, ignore_index=True)
    new_character_df.to_excel(character_sheet_path, index=False)
    return("New character added! Please edit skills, abilities, and inventory from their respective slash commands.")

# Edit character sheet

# Maintain skills
def trained_lookup(name):
    character_df = pd.read_excel(character_sheet_path)
    trained = character_df.loc[character_df['name'] == name, 'Trained'].item()
    return(trained)

def spec_lookup(name):
    character_df = pd.read_excel(character_sheet_path)
    specialized = character_df.loc[character_df['name'] == name, 'Specialized'].item()
    return(specialized)

def inability_lookup(name):
    character_df = pd.read_excel(character_sheet_path)
    inability = character_df.loc[character_df['name'] == name, 'Inability'].item()
    return(inability)

def skills_update(name, trained, specialized, inability):
    character_df = pd.read_excel(character_sheet_path)
    character_df.loc[character_df['name'] == name, 'Trained'] = trained
    character_df.loc[character_df['name'] == name, 'Specialized'] = specialized
    character_df.loc[character_df['name'] == name, 'Inability'] = inability
    character_df.to_excel(character_sheet_path, index=False)
    return("Skills updated!")

# Maintain ability_list
def ability_lookup(name):
    character_df = pd.read_excel(character_sheet_path)
    abilities = character_df.loc[character_df['name'] == name, 'Abilities'].item()
    return(abilities)

def ability_update(name, abilities):
    character_df = pd.read_excel(character_sheet_path)
    character_df.loc[character_df['name'] == name, 'Abilities'] = abilities
    character_df.to_excel(character_sheet_path, index=False)
    return("Abilities updated!")

# Maintain inventory
def cypher_lookup(name):
    character_df = pd.read_excel(character_sheet_path)
    cypher = character_df.loc[character_df['name'] == name, 'Cypher'].item()
    return(cypher)

def equip_lookup(name):
    character_df = pd.read_excel(character_sheet_path)
    equip = character_df.loc[character_df['name'] == name, 'Equipment'].item()
    return(equip)

def inventory_update(name, cypher, equip):
    character_df = pd.read_excel(character_sheet_path)
    character_df.loc[character_df['name'] == name, 'Cypher'] = cypher
    character_df.loc[character_df['name'] == name, 'Equipment'] = equip
    character_df.to_excel(character_sheet_path, index=False)
    return("Inventory updated!")

# Maintain notes
def notes_lookup(name):
    character_df = pd.read_excel(character_sheet_path)
    notes = character_df.loc[character_df['name'] == name, 'Notes'].item()
    return(notes)

def notes_update(name, notes):
    character_df = pd.read_excel(character_sheet_path)
    character_df.loc[character_df['name'] == name, 'Notes'] = notes
    character_df.to_excel(character_sheet_path, index=False)
    return("Notes updated!")
