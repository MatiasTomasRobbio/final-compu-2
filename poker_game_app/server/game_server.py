import argparse
import socket
import pickle
import random



def wait_for_players(server_socket, num_players, starting_money):
    players_data = []
    names_used = []
    while len(players_data) < num_players:
        print(f"Waiting for players [{len(players_data)}/{num_players}]...")
        client_socket, client_address = server_socket.accept()
        player_name = pickle.loads(client_socket.recv(1024))

        # Receive the player's name from the client
        if player_name in names_used:
            client_socket.send(pickle.dumps('Name already taken.'))
            continue

        
        
        

        player_data = {
            'name': player_name,
            'socket': client_socket,
            'address': client_address,
            'money': starting_money
        }
        players_data.append(player_data)
        names_used.append(player_name)
        print(f"Player {player_name} connected.")

    return players_data

def game_loop(players_data):
    while True:
        for player_data in players_data:
            print(f"Player {player_data['name']}'s turn.")
            client_socket = player_data['socket']
            # Notify the current player that it's their turn
            client_socket.send(pickle.dumps("It's your turn!"))
            # Notify all other players that it's the current player's turn
            for other_player_data in players_data:
                if other_player_data is not player_data:
                    other_player_data['socket'].send(pickle.dumps(f"It's {player_data['name']}'s turn!"))
            # Wait for the current player's response
            try:
                print(f"Waiting for action from {player_data['name']}...")
                message = pickle.loads(client_socket.recv(1024))
                action =  str(f"{player_data['name']}: {message}")
                print(f"Received action from {action}")
                #Send the action to all players
                for player_data in players_data:
                    player_data['socket'].send(pickle.dumps(f"{action}"))
            except (BrokenPipeError, ConnectionResetError):
                print(f"Player {player_data['name']} disconnected.")
                players_data.remove(player_data)
   



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("server_port", type=int,help="Enter the server port")
    parser.add_argument("num_players", type=int, default=5, help="Enter the number of players")
    parser.add_argument("starting_money", type=int,default=1000, help="Enter the starting money for each player")
    args = parser.parse_args()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', args.server_port))
    server_socket.listen(args.num_players)

    print(f"Server started on port {args.server_port}. Waiting for players...")

    players_data = wait_for_players(server_socket, args.num_players, args.starting_money)
    print("All players connected. Starting game...")

    game_loop(players_data)
