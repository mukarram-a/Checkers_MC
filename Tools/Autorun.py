import subprocess, os, sys, time

# Define the file name you want to execute
current_directory = os.getcwd()

# Goes back 1 directory to our AI (main.py)
split_path = current_directory.split(os.path.sep)
new_directory = os.path.sep.join(split_path[:-1])

# Dictionary that stores wins for Player 1 (Black) and Player 2 (White)
wins = {}
wins["Player_1_Black"] = 0
wins["Player_2_White"] = 0
wins["Ties"] = 0

# CHANGE THIS VALUE TO HOW MANY GAMES WILL BE RUN
TOTAL_GAMES = 50
games_played = 0

try:
    # Run the simulations
    for i in range(TOTAL_GAMES):
        print("Game ", end = "")
        print(i + 1, "of", TOTAL_GAMES, end = ": ")

        # Runs against "RandomAI.py"
        start_time = time.time()

        result = subprocess.run(['python3', os.path.join(current_directory, "AI_Runner.py"), "8", "8", "2", "l", os.path.join(new_directory, "src", "checkers-python", "main.py"), os.path.join(current_directory, "Sample_AIs", "Average_AI", "main.py")], stdout=subprocess.PIPE)

        end_time = time.time()
        execution_time = end_time - start_time
    
        # Get output from original AI code (the code prints out which player wins).
        console_output = str(result.stdout)
        # print(console_output)

        # Fix formatting for the original AI code output by removing symbols.
        output_search = console_output.strip("b'\\n")

        # Check which player won and incremenet it in the "wins" dictionary
        if "player 1 wins" in output_search:
            print("Player 1 (Black) Wins")
            wins["Player_1_Black"] += 1

        elif "player 2 wins" in output_search:
            print("Player 2 (White) Wins")
            wins["Player_2_White"] += 1

        elif "Tie" in output_search:
            print("Tie")
            wins["Ties"] += 1
        
        games_played += 1

        print("Time =", execution_time)

        print()

except KeyboardInterrupt:
    pass
    # print("\n---Total Wins---")
    # for i in wins:
    #     print(i, end = ": ")
    #     print(wins[i])

    # print("---Percentage Wins---")
    # print(((wins["Player_1_Black"] + wins["Ties"]) / games_played )* 100, end ='%\n')
    # print()
    # sys.exit()

finally:
    print("\n---Total Wins---")
    for i in wins:
        print(i, end = ": ")
        print(wins[i])

    print("---Percentage Wins---")
    print(((wins["Player_1_Black"] + wins["Ties"]) / games_played )* 100, end ='%\n')
    print()

