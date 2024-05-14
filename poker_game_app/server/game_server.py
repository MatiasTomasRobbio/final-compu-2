from game_class import *
from player_class import *
import socket
import argparse
import pickle


def poker_game(players):
    # Initialize the game with the players
    game = Game(players)

    # Start the game
    continue_game = True
    winner = None

    while continue_game:

        game.reset()

        #Commencing a new hand 
        game.broadcast(f"print", f"Starting a new hand.")
        game.deal_hands()
        

        while True:
            game.broadcast(f"print", f"Starting pre-flop round.")
            got_winner , winner = game.start_betting_round()

            if got_winner:
                game.broadcast(f"print", f"All players folded, {winner.name} has won the hand.")
                break
                
            game.broadcast(f"print", f"Starting flop round.")
            game.deal_community_cards(3)
            game.broadcast(f"community_cards", game.community_cards)

            got_winner , winner = game.start_betting_round()

            if got_winner:
                game.broadcast(f"print", f"All players folded, {winner.name} has won the hand.")
                break

            game.broadcast(f"print", f"Starting turn round.")
            game.deal_community_cards(1)
            game.broadcast(f"community_cards",game.community_cards)

            got_winner , winner = game.start_betting_round()    

            if got_winner:
                game.broadcast(f"print", f"All players folded, {winner.name} has won the hand.")
                break

            game.broadcast(f"print", f"Starting river round.")
            game.deal_community_cards(1)
            game.broadcast(f"community_cards",game.community_cards)

            got_winner , winner = game.start_betting_round()

            if got_winner:

                game.broadcast(f"print", f"All players folded, {winner.name} has won the hand.")
                break

            break

        
        #Determine the winner of the hand
        if got_winner:
            game.give_pot(winner)

        else:
            game.broadcast(f"print", f"Showdown time!")
            winner , hand_rank  = game.get_showdown_winner()
            game.broadcast(f"print", f"{winner.name} has won the hand with a {hand_rank}.")
            game.give_pot(winner)
        



        #Check if the game has ended
        continue_game, game_winner = game.determine_game_status()

    game.broadcast(f"ENDGAME", f"{game_winner.name} has won the game!")
    print(f"{game_winner.name} has won the game!")


def broadcast(players, command, data):
    # Broadcast the message to all connected clients
    for player in players:
        send_command(player, command, data)    

def send_command(player, command, data):
        # Send a message to a specific player
        socket = player.conn
        message = (command, data)
        socket.send(pickle.dumps(message))


    
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Poker game server.")
    parser.add_argument('--port', '-p' ,type=int, help='The port to listen on.')
    #If the host is not specified, it will default to localhost
    parser.add_argument('--host', help='The host to listen on.', default='localhost', required=False)
    #The number of players in the game can´t be less than 2
    parser.add_argument('--num_players','-n', type=int, help='The number of players in the game.', default=3)
    #The starting money of the players(if not specified it will default to 1000)
    parser.add_argument('--money','-m', type=int, help='The starting money of the players.', default=1000)

     # Parse the arguments
    args = parser.parse_args()

    #Check if the number of players is less than 2 and money is different than 0
    if args.num_players < 2:
        print("The number of players must be at least 2.")
        exit()
    
    if args.money == 0:
        print("The starting money must be different than 0.")
        exit()

    players_num = args.num_players

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the host and port
    host = args.host
    port = args.port

     # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections until the number of players is reached and then start the game
    #A player connects with a name but if that name is already taken, the player will be asked to choose another name
    #If the player chooses a name that is not taken, the player will be added to the list of players and a welcome message will be sent
    #All other players will be notified that a new player has joined the game with the current number of players and list of players
    server_socket.listen(players_num)
    print(f"Server is listening on {host}:{port}")
    print(f"Waiting for {players_num} players to join the game.")
    players = []

    while len(players) < players_num:
        #Accept client connection
        client_socket, addr = server_socket.accept()
        #Receive client name
        client_name = client_socket.recv(1024).decode()
        #Create the player object
        player = Player(client_name, args.money, client_socket)

        if client_name in [player.name for player in players]:
            print(f"{addr} has tried to join the game with the name {client_name} that is already taken. Connection refused.")
            send_command(player, 'name_taken', f"Name {client_name} is already taken. Please choose another name.")
            continue
        
      

        #Send welcome message to the client
        send_command(player, 'connected', f'Welcome to the game, {client_name}! , The starting money is {args.money}.')
        
        #Broadcast the new player's arrival to all connected clients
        print(f'{client_name} has joined the game.')
        broadcast(players, 'print', f'{client_name} has joined the game.')        

        #Add the player to the list of players
        players.append(player)
       
        #Broadcast the current number of players and list of players to all connected clients
        broadcast(players, 'players_list', [player.name for player in players])


    #Start the game
    poker_game(players)
    print("Game has ended.")
    server_socket.close()


        