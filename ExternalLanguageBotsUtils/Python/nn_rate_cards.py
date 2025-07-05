import numpy as np
import json
import re
import sys
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the JSON file
json_file_path = os.path.join(script_dir, 'cards.json')

# Open and read the JSON file
with open(json_file_path) as f:
    cardsjson = json.load(f)


patron_key = {'Treasury' : 0, 'Ansei' : 1, 'Crows' : 2, 'Rajhin' : 3, 'Psijic' : 4, 'Orgnum' : 5, 'Hlaalu' : 6, 'Pelin' : 7, 'Red Eagle' : 8}
effect_slot_key = {
    'Coin' : 0,
    'Power' : 1,
    'Prestige' : 2,
    'OppLosePrestige' : 3,
    'Remove' : 4,
    'Acquire' : 5,
    'Destroy' : 6,
    'Draw' : 7,
    'Discard' : 8,
    'Return' : 9,
    'Toss' : 10,
    'KnockOut' : 11,
    'Patron' : 12,
    'Create' : 13,
    'Heal' : 14
    }

def parse_effects(text):
    # Use regular expression to find all occurrences of the pattern 'EFFECT_NAME number'
    pattern = r"(\w+)\s+(\d+)"
    matches = re.finditer(pattern, text)
    
    # Convert each match into a tuple and collect them into a list
    result = [(match.group(1), int(match.group(2))) for match in matches]
    return result

def convert_gamestate_cardname_to_cardsjson_cardname(gamestate_cardname):
    if gamestate_cardname == 'ANSEIS_VICTORY':
        return "Ansei's Victory"
    elif gamestate_cardname == 'HIRA\'S_END' or gamestate_cardname == 'HIRAS_END' or gamestate_cardname == 'Hira\'s End':
        return "Hira's End"
    elif gamestate_cardname == 'LEGIONS_ARRIVAL' or gamestate_cardname == 'LEGION\'S_ARRIVAL' or gamestate_cardname == 'Legion\'s Arrival':
        return "Legion's Arrival"
    elif gamestate_cardname == 'RINGS_GUILE' or gamestate_cardname == 'RING\'S_GUILE' or gamestate_cardname == 'Ring\'s Guile':
        return "Ring's Guile"
    elif gamestate_cardname == 'ARCHERS_VOLLEY' or gamestate_cardname == 'ARCHER\'S_VOLLEY' or gamestate_cardname == 'Archers\' Volley':
        return "Archers' Volley"
    elif gamestate_cardname == 'CLANWITCH':
        return "Clan-Witch"
    elif gamestate_cardname == 'KARTH_MANHUNTER':
        return "Karth Man-Hunter"
    elif gamestate_cardname == "KING_ORGNUM'S_COMMAND" or gamestate_cardname == "KING_ORGNUM\'S_COMMAND" or gamestate_cardname == "King Orgnum's Command":
        return "King Orgnum's Command"
    elif gamestate_cardname == "SEA_RAIDERS_GLORY" or gamestate_cardname == "SEA_RAIDER\'S_GLORY" or gamestate_cardname == "Sea Raider's Glory":
        return "Sea Raider's Glory"
    elif gamestate_cardname == "SHADOWS_SLUMBER" or gamestate_cardname == "Shadow\'s Slumber" or gamestate_cardname == "SHADOW\'S_SLUMBER":
        return "Shadow's Slumber"
    elif gamestate_cardname == "TOLL_OF_FLESH":
        return "Toll of Flesh"
    elif gamestate_cardname == "TOLL_OF_SILVER":
        return "Toll of Silver"
    elif gamestate_cardname == "MURDER_OF_CROWS":
        return "Murder of Crows"
    elif gamestate_cardname == "LAW_OF_SOVEREIGN_ROOST":
        return "Law of Sovereign Roost"
    elif gamestate_cardname == "POOL_OF_SHADOW":
        return "Pool of Shadow"
    elif gamestate_cardname == "HIRAS_END" or gamestate_cardname == "HIRA\'S_END" or gamestate_cardname == "Hira's End":
        return "Hira's End"
    elif gamestate_cardname == "MARCH_ON_HATTU" or gamestate_cardname == "March on Hattu":
        return "March on Hattu"
    elif gamestate_cardname == "ANSEI'S_VICTORY" or gamestate_cardname == "ANSEI\'S_VICTORY" or gamestate_cardname == "Ansei\'s Victory":
        return "Ansei's Victory"
    elif gamestate_cardname == "WAY_OF_THE_SWORD" or gamestate_cardname == "Way of the Sword":
        return "Way of the Sword"
    elif gamestate_cardname == "KNIGHTS_OF_SAINT_PELIN":
        return "Knights of Saint Pelin"
    elif gamestate_cardname == "BAG_OF_TRICKS":
        return "Bag of Tricks"
    elif gamestate_cardname == "POUNCE_AND_PROFIT":
        return "Pounce and Profit"
    elif gamestate_cardname == "RINGS_GUILE" or gamestate_cardname == "RING\'S_GUILE" or gamestate_cardname == "Ring's Guile":
        return "Ring's Guile"
    elif gamestate_cardname == "SHADOWS_SLUMBER" or gamestate_cardname == "SHADOW\'S_SLUMBER" or gamestate_cardname == "Shadow's Slumber":
        return "Shadow's Slumber"
    elif gamestate_cardname == "SLIGHT_OF_HAND":
        return "Slight of Hand"
    elif gamestate_cardname == "KING_ORGNUMS_COMMAND" or gamestate_cardname == "KING_ORGNUM\'S_COMMAND" or gamestate_cardname == "King Orgnum's Command":
        return "King Orgnum's Command"
    elif gamestate_cardname == "SEA_RAIDERS_GLORY" or gamestate_cardname == "SEA_RAIDER\'S_GLORY" or gamestate_cardname == "Sea Raider's Glory":
        return "Sea Raider's Glory"
    elif gamestate_cardname == "WRIT_OF_COIN":
        return "Writ of Coin"
            
    else:
        name = gamestate_cardname
        
    name = name.replace('_', ' ').title()
    return name

#Gets a card object from cardsjson given a card name
def find_card_by_name(card_name):
    card_name = convert_gamestate_cardname_to_cardsjson_cardname(card_name)
    
    for card_object in cardsjson:
        if card_object.get('Name').replace('_',' ').title() == card_name.replace('_',' ').title():
            return card_object

def vectorize_card(card_name): # Comes from the vectorize_play_card_action in map_action_to_vector.py
    vector = np.zeros(24)
    
    #First convert the name to cardsjson format
    card_name = convert_gamestate_cardname_to_cardsjson_cardname(card_name)
    
    # Make a card object
    card = find_card_by_name(card_name)
    
    #print(card_name, file = sys.stderr)
    vector[patron_key[card['Deck']]] = 1
    
    effectsvec = np.zeros(15)
    
    combo_1_effects = card['Activation']
    if combo_1_effects != None:
        for effect in parse_effects(combo_1_effects):
            effectsvec[effect_slot_key[effect[0]]] = effect[1]
        
    combo_2_effects = card['Combo 2']
    if combo_2_effects != None:
        for effect in parse_effects(combo_2_effects):
            effectsvec[effect_slot_key[effect[0]]] += effect[1]
                
    combo_3_effects = card['Combo 3']
    if combo_3_effects != None:
        for effect in parse_effects(combo_3_effects):
            effectsvec[effect_slot_key[effect[0]]] += effect[1]
            
    combo_4_effects = card['Combo 4']
    if combo_4_effects != None:
        for effect in parse_effects(combo_4_effects):
            effectsvec[effect_slot_key[effect[0]]] += effect[1]
            
    vector[9:] = effectsvec
    
    return vector

def create_card_selection_vector(card_name):
    vec = np.zeros(129)
    
    vec[105:129] = vectorize_card(card_name)
    
    return vec # This is a vector that describes a card as if it were every type of action at once (play, activate agent, buy, etc)

def nn_rate_card(card_name, weight_vector):
    #weight vector shape is (129,)
    
    card_vector = create_card_selection_vector(card_name) # So the issue is that we're plugging multiple cards into here at the same time
    
    card_rating = np.dot(card_vector, weight_vector)
    return card_rating