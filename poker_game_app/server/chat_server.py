import socket
import threading
import argparse


# Function to handle client connections
def handle_client(client_socket):
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode()

            # Broadcast the message to all connected clients
            for client in clients:
                client.send(message.encode())
        except:
            # Remove the client from the list if there's an error
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            client_name = client_names[index]
            client_names.remove(client_name)
            broadcast(f'{client_name} has left the chat.')
            break

# Function to broadcast a message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message.encode())

# Function to start the server
def start_server(clients, client_names, server_socket):
    print('Server started.')

    while True:
        # Accept client connection
        client_socket, client_address = server_socket.accept()
        print(f'Connection from {client_address} has been established.')

        # Receive client name
        client_name = client_socket.recv(1024).decode()

        # Add client to the list
        clients.append(client_socket)
        client_names.append(client_name)

        # Send welcome message to the client
        client_socket.send(f'Welcome to the chat, {client_name}!'.encode())
        

        # Broadcast the new client's arrival to all connected clients
        print(f'{client_name} has joined the chat.')
        broadcast(f'{client_name} has joined the chat.')

        # Start a new thread to handle the client connection
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="The chat server that will rung along with the poker game server.")
    parser.add_argument('--port', type=int, help='The port to listen on( assigned by the poker game server)')

    # Parse the arguments
    args = parser.parse_args()
    
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # Define the host and port
    host = 'localhost'
    port = args.port

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen()

    # List to store connected clients
    clients = []
    client_names = []

    # Start the server
    start_server(clients=clients, client_names=client_names, server_socket=server_socket)
