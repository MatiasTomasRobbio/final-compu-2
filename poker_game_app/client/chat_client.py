import socket
import threading
import argparse



# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            # Receive message from server
            message = client_socket.recv(1024).decode()
            print(message)
        except Exception as e:
            print("Error receiving message:", e)
            break

# Function to send messages to the server
def send_messages(client_socket, client_name):
    while True:
        try:
            # Input message from the user
            message = input()
            # Send message to server with client name
            client_socket.send(f'{client_name}: {message}'.encode())
        except Exception as e:
            print("Error sending message:", e)
            break


def chat_client(host, port, name):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))

        # Send the client name to the server
        client_socket.send(name.encode())   

        # Receive the welcome message from the server
        welcome_message = client_socket.recv(1024).decode()
        print(welcome_message)

        # Start two threads for receiving and sending messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket, args.name))
        
        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()
       

    except Exception as e:
        print("Error:", e)


    finally:
        # Close the client socket
        client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chat client for the chat room server.")
    parser.add_argument('--port', '-p' ,type=int, help='The port to connect to.')
    parser.add_argument('--name', '-n', type=str, help='Your name in the chat room.')
    parser.add_argument('--host', help='The host to connect to.', default='localhost', required=False)

    # Parse the arguments
    args = parser.parse_args()



    # Define the host and port
    host = args.host    
    port = args.port

    # Start the chat client
    chat_client(host, port, args.name)

