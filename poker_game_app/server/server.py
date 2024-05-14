import socket
import argparse
import multiprocessing
from chat_server import chat_server
from player_class import Player
from game_server import poker_game,send_command, broadcast




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Poker game server with chat.")
    #Add the host argument (if not defined, default to localhost)
    parser.add_argument('--host', help='The host to listen on.', default='localhost', required=False)
    parser.add_argument('--game_port', '-g' ,type=int, help='The port the poker game process will listen on.')
    #Add the chat port argument (if not define , it should default to the port next to the game port)
    parser.add_argument('--chat_port', '-c' ,type=int, help='The port the chat process will listen on.',default=None, required=False)    
    #Game settings 
    parser.add_argument('--starting_stack', type=int, help='The starting stack for each player.', default=1000)
    parser.add_argument('--num_players' ,'-n', type=int, help='The number of players to start the game.', default=3)    
    #Parse the arguments    
    args = parser.parse_args()

     #Check if the number of players is less than 2 and money is different than 0
    if args.num_players < 2:
        print("The number of players must be at least 2.")
        exit()
    
    if args.starting_stack == 0:
        print("The starting money must be different than 0.")
        exit()

    #If the chat port is not defined, it should default to the port next to the game port   
    if args.chat_port is None:
        chat_port = args.game_port + 1
    else:
        chat_port = args.chat_port
    game_port = args.game_port
    players_num = args.num_players  
    host = args.host    
    starting_stack = args.starting_stack   


    #Launch the chat server in a separate process  
    chat_process = multiprocessing.Process(target=chat_server, args=(host, chat_port)) 
    chat_process.start()

   # Listen for incoming connections until the number of players is reached and then start the game
    #A player connects with a name but if that name is already taken, the player will be asked to choose another name
    #If the player chooses a name that is not taken, the player will be added to the list of players and a welcome message will be sent
    #All other players will be notified that a new player has joined the game with the current number of players and list of players

    # Create a socket object
    game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the host and port
    game_socket.bind((host, game_port))

    # Listen for incoming connections
    game_socket.listen(players_num)
    print(f"[GAME SERVER] listening on {host}:{game_port}")
    print(f"[GAME SERVER] Waiting for {players_num} players to join the game.")
    players = []

    while len(players) < players_num:
        #Accept client connection
        client_socket, addr = game_socket.accept()
        #Receive client name
        client_name = client_socket.recv(1024).decode()
        #Create the player object
        player = Player(client_name, starting_stack, client_socket)

        if client_name in [player.name for player in players]:
            print(f"{addr} has tried to join the game with the name {client_name} that is already taken. Connection refused.")
            send_command(player, 'name_taken', f"Name {client_name} is already taken. Please choose another name.")
            continue

        #Send welcome message to the client along with the chat port
        message = f'Welcome to the game, {client_name}! , The starting money is {starting_stack}.'
        data = (message, chat_port)
        send_command(player, 'connected',data)

        print(f"{addr} with  name: {client_name} has joined the game.")

        #Broadcast the new player's arrival to all connected clients
        broadcast(players, 'print', f'{client_name} has joined the game.')
        
        #Add the player to the list of players
        players.append(player)

        #Broadcast the current number of players and list of players to all connected clients
        broadcast(players, 'players_list', [player.name for player in players])

    
    #Start the poker game
    poker_game(players)
    

    #When the game is over, close the chat server
    chat_process.terminate()
    print("Game has ended.")
    game_socket.close()




