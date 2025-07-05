import json
import sys
import random
import socket
import pickle 
import os
from map_gamestate_to_vector import map_gamestate_to_vector
from rl_bridge import evaluate_action_space
from map_action_to_vector import map_action_to_vector
from RLTraining.sot_rl_environment import TalesOfTribute
from stable_baselines3 import PPO
import numpy as np

END_OF_TRANSMISSION = "EOT"
FINISHED_TOKEN = "FINISHED"

def get_game_state():
    data = ''
    while (data_fraction := input()) != END_OF_TRANSMISSION:
        data += data_fraction
    #debug(data)
    if data.startswith(FINISHED_TOKEN):
        # Game is over
        _, winner, reason, context = data.split(' ', 3)
        #debug(winner)
        #debug(reason)
        #debug(context)
        return (winner, reason, context), True
    return json.loads(data), False

def get_patrons_to_pick():
    data = input()
    patrons, round_nr = data.split()
    patrons = patrons.split(',')

    return patrons, round_nr
    
def debug(msg):
    print(msg, file=sys.stderr)


def evil_clone_make_decision(data, model):
    gamestate_encoding = map_gamestate_to_vector(data['State'])
    actions = data['Actions']
    
    #model = PPO.load("C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\Models\\PPO_V7\\7.23.2024\\712_training_iterations.zip")
    weight_vector, _states = model.predict(gamestate_encoding)
    
    action_preferences = evaluate_action_space(data["Actions"], data["State"], weight_vector)
    the_chosen_one = np.argmax(action_preferences)
    
    
    return the_chosen_one


#Generate a random opponent to play against from MODELS_DIR with a bias toward later models according to BIAS

def find_an_opponent(min_value = 0):
    
    MODELS_DIR = 'C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\Models\\PPO_V14\\8.8.2024'
    BIAS = 3.5
    num_files =  len([file for file in os.listdir(MODELS_DIR) if file.endswith('.zip')])
    if min_value > num_files:
        raise ValueError("min_value should not be greater than num_files")
    
    random_value = (1 - (random.random() ** BIAS))
    opponent_number = int(random_value * (num_files)) + min_value

    opponent_bot = f"{MODELS_DIR}\\{opponent_number}_training_iterations.zip"
    #debug(f'Running game against {opponent_bot}')
    return opponent_bot

model = PPO.load(find_an_opponent())

if __name__ == '__main__':

    action_filename = 'actions.pkl'
    gamestate_filename = 'gamestate.pkl'

    # Check if the file exists
    #if os.path.exists(action_filename):
    #    # Open the file in binary read mode and load the data using pickle
    #    with open(action_filename, 'rb') as file:
    #        past_actions = pickle.load(file)
    #else:
    #    #Initialize past_actions as an empty list if the file does not exist
    #    past_actions = set()
    #
    for _ in range(2):
        patrons, round_nr = get_patrons_to_pick()
        #debug(f'Received: {patrons} in round {round_nr}')
        print(random.choice(patrons))
        
    with open(gamestate_filename, 'a+b') as gs_file:
        
        while True:
            data, finished = get_game_state()
            #debug(data['Actions'])
    #        past_actions.update(data["Actions"])

    #        with open(action_filename, 'wb') as file:
    #            pickle.dump(past_actions, file)
            
            #if "State" in data:
            #    pickle.dump(data["State"], gs_file)


            if finished:
                #debug(data)
                break

            #data["State"]
            
            action = evil_clone_make_decision(data, model)
            print(action)
