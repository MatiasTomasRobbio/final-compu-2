import socket
import pickle
import argparse

def game_client(server_ip, server_port, player_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Send player name to server
    client_socket.send(pickle.dumps(player_name))

    while True:
        # Wait for a message from the server
        message = pickle.loads(client_socket.recv(1024))
        print(message)

        if message == "It's your turn!":
            # It's the player's turn, send a response
            response = input("Enter your action: ")
            client_socket.send(pickle.dumps(response))

        if message == "Name already taken.": # If the name is already taken, close the client
            client_socket.close()
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("player_name", help="Enter the player's name")
    parser.add_argument("port",type=int, help="Enter the server IP address")
    args = parser.parse_args()

    game_client('localhost',args.port , args.player_name)