import numpy as np

import gymnasium as gym
from gymnasium import spaces
import json
import socket
import subprocess
import random
import pickle
import os 
import signal
import time
import psutil
import struct

ACTION_SPACE = 129

def write_to_file(filename, msg):
    with open(filename, 'a') as file:
        file.write(msg)


class TalesOfTribute(gym.Env):
    metadata = {"render_modes": ["text"]}

    def __init__(self, render_mode=None, size=5):

        # Sockets are connections between computers (or the same computer) that allow for communication in between programs
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # In case your local firewall blocks some ports, replace 12345 with the port you want to bind to
        # if you change the port here, it will also need to be changed in rl-bridge.py
        server_address = ('localhost', 12345)
        print('starting up on %s port %s' % server_address)
        self.sock.bind(server_address)
        
        self.process = None
        self.connection = None

        # In a next we would need to encode the observation/state and the action space.
        # The problem: each action space differs in size depending on the current cards on the board.
        # This is why we just encode a weight vector to evaluate actions.
        # This makes the output size consistent which should be much
        # easier for the agent to learn.

        # Define the observation space for floating-point numbers
        # The shape argument specifies the shape of the array, which in your case is 14075
        # TODO put the minimal and maximal value of the state observation here
        low_bound = -100  # Replace with the actual lower bound for your numbers, if known
        high_bound = 100  # Replace with the actual upper bound for your numbers, if known
        self.observation_space = spaces.Box(low=low_bound, high=high_bound, shape=(14079,), dtype=np.float32)        
        self.last_observation = None

        # Out of the selection, we return a weighting vector
        # TODO put the minimal and maximal heuristic value here
        self.action_space = spaces.Box(low=-10, high=150, shape=(ACTION_SPACE,))



        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    # I aimed to provide you some little helper functions
    # for sending and receiving information between the agent and the environment
    def receive_data_from_agent(self):
        # First, receive the length of the incoming pickle data (4 bytes for 'I' format)
        length_bytes = self.connection.recv(4)
        message_length = struct.unpack('!I', length_bytes)[0]

        # Now that you know the length, receive the rest of the message
        message = b''
        while len(message) < message_length:
            part = self.connection.recv(message_length - len(message))
            if not part:
                raise Exception("Connection closed or error")
            message += part

        # Unpickle the complete message
        return pickle.loads(message)

    def send_data_to_agent(self, data):
        # Serialize your data
        data = pickle.dumps(data)

        #print("pickle message:", data, len(data))
        # Prefix the message with its length, packed into 4 bytes
        prefixed_data = struct.pack('!I', len(data)) + data

        # Send the prefixed message
        self.connection.sendall(prefixed_data)
        
    def step(self, action):
        # each step, there will be a common communication pattern between the agent and the environment
        # first the two patrons will be exchanged between the agent and the environment
        # after that, the agent will receive the game state and will send an action back to the environment
        # Here, I implemented to randomly choose the patrons, such that the agent learns to use all of them.
        # This could later be replaced to a more clever selection of patrons for maximizing performance.

        #print("Send action: ", action)
        self.send_data_to_agent(action)

        # get the next observation for the RL agent to process
        decoded_message = self.receive_data_from_agent()
        
        #print("Received message: ", decoded_message[0])
        if decoded_message[0] == "Gamestate":
            observation = decoded_message[1]
            reward = decoded_message[2]
            terminated = False      # has the game been ended due to the game rules

        else:
            observation = self.last_observation
            reward = decoded_message[1] * 2     # at the end of the game, we give a reward of 1 for winning and 0 for losing. ##UPDATED!!!! Bas changed this to 2 for winning, 0 for losing.
            #file_name = 'C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\ScriptsOfTribute-Core-master\\Bots\\ExternalLanguageBotsUtils\\Python\\RLTraining\\Winners_Log.txt'
            #with open(file_name, 'a') as file:
            #    file.write(f"{reward} - end game message\n")
            terminated = True               # has the game been ended due to the game rules

        #print("Received observation: ", observation.shape)

        truncated = False       # has the game been ended due to external circumstances, e.g. time limit reached
        info = dict()           # storing additional information of the current game state or run

        self.last_observation = observation
        return observation, reward, terminated, truncated, info    
    
    def reset(self, seed=None, options=None):
        #print("reset")

        # We need the following line to seed self.np_random
        super().reset(seed=seed)


        if self.process is not None and psutil.pid_exists(self.process.pid):
            # Check if the process has not already ended
            if self.process.poll() is None:
                try:
                    # Try to terminate the process
                    self.process.terminate()
                    # Wait for the process to terminate
                    self.process.wait(timeout=5)
                except Exception as e:
                    pass
                    #print(f"Error while terminating process: {e}")

        # Close the socket connection
        if self.connection is not None:
            try:
                self.connection.close()
            except Exception as e:
                pass
                #print(f"Error while closing connection: {e}")


        self.sock.listen()
        #Paths on my computer:
        
        # C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\ScriptsOfTribute-Core-master\\GameRunner\\bin\\Release\\net7.0\\GameRunner
        
        # cmd:python ../../../../Bots/ExternalLanguageBotsUtils/Python/rl-bridge.py
        
        # cwd = C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\ScriptsOfTribute-Core-master\\GameRunner\\bin\\Release\\net7.0\\
            
        # create a game using the commandline. #TODO: The link in the next line needs to be changed to your path setup
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(script_dir, '../../../..'))

        self.process = subprocess.Popen([f'{root_dir}/GameRunner/bin/Release/net7.0/GameRunner',
                          "cmd:python ../../../../Bots/ExternalLanguageBotsUtils/Python/rl_bridge.py",
                          "MaxPrestigeBot", # Evil clone bot is in the RL folder
                          "-n", "1", 
                          "-t", "1"], 
                          cwd=f"{root_dir}/GameRunner/bin/Release/net7.0/")

        # Wait for a connection, the python agent that takes part in the game will try to connect to this program
        #print('waiting for a connection')
        self.connection, client_address = self.sock.accept()
        #print('connection from', client_address)

        # get the next observation for the RL agent to process
        observation = self.receive_data_from_agent()[1]
        #print("Received observation: ", observation.shape)

        info = None
        self.last_observation = observation
        return observation, info
    
    def render(self):
        if self.render_mode == "test":
            return str(self.last_observation())
        
    
    def close(self):
        self.sock.close()
        if self.process is not None:
            os.kill(self.process.pid, signal.SIGTERM)  # Send the signal to all the process groups


import re
import csv
import sys

def run_evaluation_games(direct, opponent):
    folder_path = direct
    os.chdir(folder_path)
    
    # Command to run the rl_bridge.py script
    ## Example uses Beam Search as opponent bot and 100 games for evaluation.
    ## Adjust threads and # of evaluation games as hardware allows. I have 10 threads b/c computation limitations. Aim for maybe 1000 games per evaluation?
    testing_opponent = opponent
    
    command = f'GameRunner {testing_opponent} "cmd:python ../../../../Bots/ExternalLanguageBotsUtils/Python/rl-gg.py " -n 1000 -t 10'
    
    # Run the command    
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Extract the output
    output = result.stdout

    match = re.search(r'Final amount of P2 wins:\s*(\d+)/\d+\s*\(\d+%\)', output)
    
    if match:
        # Extract the number of wins
        wins = int(match.group(1))
        csv_file = 'C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\Logs\\Winrate.csv'
        # Check if the CSV file exists
        file_exists = os.path.isfile(csv_file)
        
        # Append the number of wins to the CSV file
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # If the file doesn't exist, write the header
            if not file_exists:
                writer.writerow(["Wins"])
            
            # Write the number of wins as a new row
            writer.writerow([wins])
        
        print(f"Saved {wins} wins to the CSV file.")
    else:
        print("Could not determine the number of wins.")

    #change working directory back to avoid issues
    RL_folder = 'C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\ScriptsOfTribute-Core-master\\Bots\\ExternalLanguageBotsUtils\\Python\\RLTraining'
    os.chdir(RL_folder)

if __name__ == "__main__":
    from stable_baselines3 import PPO
    from stable_baselines3.common.logger import configure


    



    direct = f"WESEF_dayof"
    date = '3.15.2025'
    
    models_dir = f"Models\\{direct}"
    logdir = f"Logs\\{direct}"

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    if not os.path.exists(logdir):
        os.makedirs(logdir)


    env = TalesOfTribute()
    env.reset()
    
    policy_kwargs=dict(
        net_arch=dict(pi=[128, 128], vf=[128, 128])
        )
    
    TIMESTEPS = 10000
    iterations = 0
    
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir, device = "cuda")
    #model = PPO.load(f"C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\Models\\PPO_V14\\8.8.2024\\3200_training_iterations.zip", env, verbose=1, tensorboard_log=logdir, device="cuda")
    
    
    #new_model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="Testing final V14 against ", policy_kwargs=policy_kwargs, device = "cuda")
    #new_model.set_parameters(model.get_parameters)
    #model = new_model
    
    
    #model.set_device("cuda")
    print(f'Using device {model.device}')
    
    
    while True:
        iterations += 1
        print(iterations)
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"WESEF Demonstration")
        model.save(f'{models_dir}/{date}/{iterations}_training_iterations')
        
        ##evaluation command:
        #  cd C:\Users\lashm\OneDrive\Desktop\SoT_RL_WORKING\ScriptsOfTribute-Core-master\GameRunner\bin\Release\net7.0
        #  .\GameRunner "cmd:python ../../../../Bots/ExternalLanguageBotsUtils/Python/rl-gg.py" RandomBot -n 500 -t 5