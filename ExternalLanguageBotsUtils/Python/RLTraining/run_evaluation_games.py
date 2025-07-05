def run_evaluation_games():
    folder_path = "C:\\Users\\lashm\\OneDrive\\Desktop\\SoT_RL_WORKING\\ScriptsOfTribute-Core-master\\GameRunner\\bin\\Release\\net7.0"
    os.chdir(folder_path)
    
    # Command to run the rl_bridge.py script
    ## Example uses Beam Search as opponent bot and 100 games for evaluation.
    ## Adjust threads and # of evaluation games as hardware allows. I have 10 threads b/c computation limitations. Aim for maybe 1000 games per evaluation?
    testing_opponent = 'BeamSearchBot'
    
    command = f'GameRunner {testing_opponent} "cmd:python ../../../../Bots/ExternalLanguageBotsUtils/Python/rl-gg.py " -n 1 -t 1'
    
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