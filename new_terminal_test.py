import subprocess
import time
import os
name = 'Alice'
port = 14500

# Get the absolute path of the chat_client.py file
script_path = os.path.abspath('poker_game_app/client/chat_client.py')

# Create a new terminal window for the server for each player and connect to the server

chat = subprocess.Popen(['gnome-terminal', '--', 'python3', script_path, '--port', str(port), '--name', name])
    
input('Press Enter to close...')

chat.terminate()
chat.wait()

#No se puede cerrar por ser un terminal de gnome