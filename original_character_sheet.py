import pandas as pd
import ast
import random

def profile(name):
    character_df = pd.read_excel('Characters.xlsx')
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
    character_df = pd.read_excel('Characters.xlsx')
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

def setup_character(name, full_name, desc, ctype, focus, flavor = "", m = 8, s = 8, i = 8, m_e = 0, s_e = 0, i_e = 0):
    character_df = pd.read_excel('Characters.xlsx')
    d = {'name':[name], 'Full_Name':[full_name], 'Descriptor':[desc], 'Type':[ctype], 'Focus':[focus], 'Flavor':[flavor], 'Tier':[1], 'Effort':[1], 'XP':[0], 'Might_C':[m], 'Might_P':[m], 'Might_E':[m_e], 'Speed_C':[s], 'Speed_P':[s], 'Speed_E':[s_e], 'Int_C':[i], 'Int_P':[i], 'Int_E':[i_e], 'Advancement':[[]]}
    char_df = pd.DataFrame.from_dict(data=d)
    new_character_df = character_df.append(char_df, ignore_index=True)
    new_character_df.to_excel('Characters.xlsx', index=False)
    return("New character added!")

def spend(name, might=0, speed=0, intel=0, xp=0):
    character_df = pd.read_excel('Characters.xlsx')
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
        character_df.to_excel('Characters.xlsx', index=False)
        output = "Character updated accordingly."
        return output
    
def recover(name, might=0, speed=0, intel=0):
    character_df = pd.read_excel('Characters.xlsx')
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
        character_df.to_excel('Characters.xlsx', index=False)
        output = "Character updated accordingly."
        return output
    
def add_xp(name, amount):
    character_df = pd.read_excel('Characters.xlsx')
    xp_c = character_df.loc[character_df['name'] == name, 'XP'].item()
    new_xp = xp_c + amount
    character_df.loc[character_df['name'] == name, 'XP'] = new_xp
    character_df.to_excel('Characters.xlsx', index=False)
    output = "XP awarded!"
    return output
    
def advance(name, pools=None, effort=None, edge=None, skill=None, other=None):
    character_df = pd.read_excel('Characters.xlsx')
    
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
    
    character_df.to_excel('Characters.xlsx', index=False)
    
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

def skills(name):
    character_skills = pd.read_excel('Character_Skills.xlsx')
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
    character_ab = pd.read_excel('Character_Abilities.xlsx')
    # Pretty-prints abilities
    full = character_ab.loc[character_ab['name'] == name, 'Full_Name'].item()
    abilities = character_ab.loc[character_ab['name'] == name, 'Abilities'].item()
    
    output = """>>> __**{}**__
{}""".format(full, abilities)
    
    return output

def equipment(name):
    character_eq = pd.read_excel('Character_Inventory.xlsx')
    # Pretty-prints equpiment
    full = character_eq.loc[character_eq['name'] == name, 'Full_Name'].item()
    cypher = character_eq.loc[character_eq['name'] == name, 'Cypher'].item()
    equip = character_eq.loc[character_eq['name'] == name, 'Equipment'].item()
    
    output = """>>> __**{}**__
Cypher     | {}
Equipment  | {}""".format(full, cypher, equip)
    
    return output

def rest(name):
    character_df = pd.read_excel('Characters.xlsx')
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
    character_df.to_excel('Characters.xlsx', index=False)
    
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