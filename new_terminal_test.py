import subprocess
import time
import os
names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
port = 14666

# Get the absolute path of the chat_client.py file
script_path = os.path.abspath('poker_game_app/chat_client.py')

# Create a new terminal window for the server for each player and connect to the server
for name in names:
    subprocess.Popen(['gnome-terminal', '--', 'python3', script_path, '--port', str(port), '--name', name])
    
input('Press Enter to continue...')