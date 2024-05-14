import socket
import threading
import argparse


# Function to handle client connections
def handle_client(client_socket,clients):
    while True:
        try:
            # Receive message from client
            data = client_socket.recv(1024).decode()
            name , message = data.split(':', 1)
            # Send confirmation message to client
            client_socket.send(f'You Sent :{message}'.encode())
            # Broadcast the message to all connected clients
            print(f'[CHAT SERVER]{name} says:{message}')
            broadcast(f'{name} says:{message}',clients,client_socket)
        except:
            # Remove the client from the list if there's an error
            clients.remove(client_socket)
            client_socket.close()
            break

# Function to broadcast a message to all other clients but the sender
def broadcast(message,all_clients,client_socket):
    for client_conn in all_clients:
        # Check if isn't the connection of who's send
        if client_conn != client_socket:
            try:
                # Sending message to client connection
                client_conn.send(message.encode())

            # if it fails, there is a chance of socket has died
            except Exception as e:
                print('Error broadcasting message: {e}')
                client_conn.close()


# Function to start the server
def chat_server(host, port):
     # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen()
    print('Chat Server started.\n ')

    clients = []

    while True:

        # Accept client connection
        client_socket, client_address = server_socket.accept()
        print(f'[CHAT SERVER] Connection from {client_address} has been established.')

        # Receive client name
        client_name = client_socket.recv(1024).decode()

        # Send welcome message to the client
        client_socket.send(f'Welcome to the chat, {client_name}!'.encode())
        
        # Add the client to the list of clients
        clients.append(client_socket)

        # Broadcast the new client's arrival to all connected clients
        print(f'[CHAT SERVER]{client_name} has joined the chat.')
        broadcast(f'{client_name} has joined the chat.',clients,client_socket)

        # Start a new thread to handle the client connection
        thread = threading.Thread(target=handle_client, args=(client_socket,clients))
        thread.start()



#################Function if you want to start the chat server standalone########################3

if __name__ == '__main__':



    parser = argparse.ArgumentParser(description="Chat server for a chat room.")
    parser.add_argument('--port' ,'-p ', type=int, help='The port to listen on.')
    parser.add_argument('--host', help='The host to listen on.', default='localhost', required=False)   

    # Parse the arguments
    args = parser.parse_args()

   

    # Define the host and port
    host = args.host
    port = args.port



    try:
        # Start the server
        chat_server(host,port)
    except OSError as e:
        if e.errno == 98:
            print("Error: The specified port is already in use. Please choose a different port.")
        else:
            print("OS error:", e)
    except Exception as e:
        print("Error:", e)
