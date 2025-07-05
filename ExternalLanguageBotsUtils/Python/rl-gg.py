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
import csv

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

import pandas as pd

def count_turns(gamestate):
    if not 'CompletedActions' in gamestate:
        return 0
    
    actions = gamestate['CompletedActions']
    count = 1
    
    for action in actions:
        if action == 'END_TURN':
            count += 1
            
    return count

def append_array_to_csv(array, filename):
    # Convert the NumPy array to a DataFrame
    df = pd.DataFrame([array])
    
    # Check if the file exists to determine the write mode
    if not os.path.isfile(filename):
        # If the file doesn't exist, write with headers
        df.to_csv(filename, index=False, header=False)
    else:
        # If the file exists, append without headers
        df.to_csv(filename, mode='a', index=False, header=False)


## writes the weight vector into a file for later analysis
def report_preference_vector(gamestate, vector):
    turn_number = count_turns(gamestate)
    file_name = f"C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\Logs\\Preference_vectors\\turn_{turn_number}.csv"
    append_array_to_csv(vector, file_name)
    debug(f'appended for turn {turn_number}')
    

# Returns the action that rl-gg wants to play
def evil_clone_make_decision(data, model):
    gamestate_encoding = map_gamestate_to_vector(data['State'])
        
    weight_vector, _states = model.predict(gamestate_encoding)
    
    #debug(weight_vector)
    
    #report_preference_vector(data['State'], weight_vector)

    
    action_preferences = evaluate_action_space(data["Actions"], data["State"], weight_vector)
    the_chosen_one = np.argmax(action_preferences)
    
    
    return the_chosen_one

MODEL_FILEPATH = 'C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\Models\\PPO_V14\\8.8.2024\\3200_training_iterations.zip'
#MODEL_FILEPATH = "C:\\Users\\lashm\\OneDrive\\Desktop\\Long_trained_models\\NewModels\\PPO_vs_EvilCloneBot\\PPO_V1\\3\\PPO_512_256_128\\12_training_iterations.zip" # repitition 3 of smallest NN size
#MODEL_FILEPATH = "C:\\Users\\lashm\\OneDrive\\Desktop\\Long_trained_models\\NewModels\\PPO_vs_EvilCloneBot\\PPO_V1\\5\\PPO_512_256_256_128\\13_training_iterations.zip" # second nn run 5
#MODEL_FILEPATH = "C:\\Users\\lashm\\OneDrive\\Desktop\\Long_trained_models\\NewModels\\PPO_vs_EvilCloneBot\\PPO_V1\\5\\PPO_512_256_256_128_128\\5_training_iterations.zip" #512 256 256 128 128 largest NN run 5
###   Make sure to set the right observation size prior to running an experiment!

model = PPO.load(MODEL_FILEPATH)
#debug(f"just loaded model {MODEL_FILEPATH}")

if __name__ == '__main__':

    action_filename = 'actions.pkl'
    gamestate_filename = 'gamestate.pkl'

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
