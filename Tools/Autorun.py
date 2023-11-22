import subprocess, os

# Define the file name you want to execute
current_directory = os.getcwd()
print(current_directory)

# Goes back 1 directory to our AI (main.py)
split_path = current_directory.split(os.path.sep)
new_directory = os.path.sep.join(split_path[:-1])

# Dictionary that stores wins for Player 1 (Black) and Player 2 (White)
wins = {}
wins["Player_1_Black"] = 0
wins["Player_2_White"] = 0
wins["Ties"] = 0



# Run the file 100 times
for i in range(100):
    result = subprocess.run(['python3', os.path.join(current_directory, "AI_Runner.py"), "8", "8", "3", "l", os.path.join(new_directory, "src", "checkers-python", "main.py"), os.path.join(current_directory, "Sample_AIs", "Random_AI", "main.py")], stdout=subprocess.PIPE)
    console_output = result.stdout

    print("THIS IS STDOUT", console_output)

    print(type(console_output))
    output_search = console_output.strip("b")
    print(output_search, "IS OUTPUT SEARCH")
    
    if "1" in output_search:
        print("Player 1 (Black) Wins")
        wins["Player_1_Black"] += 1

    elif "2" in output_search:
        print("Player 2 (White) Wins")
        wins["Player_2_White"] += 1

    elif "Tie" in output_search:
        print("Ties")
        wins["Ties"] += 1



        



    print("Game #", i + 1, end ="")
    print(".")
