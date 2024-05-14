import socket
import pickle
import argparse
import subprocess
from chat_client import chat_client


def send_data(client_socket, data):
    client_socket.send(pickle.dumps(data))

def decode_message(message):
    command, data = pickle.loads(message)
    return command, data

def cards_to_string(cards):
    # ANSI escape codes for text colors
    RED = '\033[91m'
    BLACK = '\033[30m'
    RESET = '\033[0m'

    # Define card suits
    suits = {
        'Hearts': RED + '♥' + RESET,
        'Diamonds': RED + '♦' + RESET,
        'Clubs': BLACK + '♣' + RESET,
        'Spades': BLACK + '♠' + RESET
    }
    #Converts the cards list to a colored symbol and number string separated by a space
    return " ".join([f"{card[0]}{suits[card[1]]}" for card in cards])

#Handle the user's input and choose an action given a list of options
def choose_action(options,client_socket,game_data):
    while True:
        print("Your possible actions are:")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")
        while True:
            choice = str(input("Choose an action: "))
            choice = choice.lower()
            print(f"Your choice is: {choice}")
            if choice.lower() in options:
                if choice.lower() == "call":
                    send_data(client_socket, choice)
                    return

                if choice.lower() == "fold":
                    send_data(client_socket, choice)
                    return
                
                if choice.lower() == "check":
                    send_data(client_socket, choice)
                    return
                
                if choice.lower() == "all_in":
                    print("You are going all in.")
                    send_data(client_socket, choice)
                    return
                
                if choice.lower() == "raise" or choice.lower() == "bet":
                    send_data(client_socket, choice)
                    raise_bet(client_socket,game_data)
                    return  
        
            else:
                print("Invalid action. Please choose one of the available options.")
                continue
                
        
def raise_bet(client_socket,game_data): 
    while True:
        amount = input("Enter the amount you want to raise: ")
        
        #Check if the amount is a number
        if amount.isdigit() == False:
            print("Invalid amount. Please enter a number.")
            continue
        
        #Convert the amount to an integer
        amount = int(amount)
        #Check that the player has enough money to raise
        if game_data['money'] >= amount:
            #Check if the raise is higher than the current bet
            if (amount + game_data['bet']) < game_data['current_bet']:
                print("The raise must be higher than the current bet.")
                continue
            else:
                send_data(client_socket, amount)
                break
        else:
            print("You don't have enough money to raise.")
            continue

       

            
    


def connect_to_server(server_ip, port, name):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect((server_ip, port))
    #send the client name to the server
    client_socket.send(name.encode())

    #Receive response from server
    message = client_socket.recv(1024)
    # Decode message
    command, data = decode_message(message)

     #END THE PRGRAM IF THE NAME IS TAKEN
    if command == "name_taken":
        print(data)
        exit()
    elif command == "connected":
        message, chat_port = data
        print(message)
        return client_socket , chat_port
    

def handle_game(client_socket):
    game_data = {
        "money": 0,
        "bet": 0,
        "all_in": False,
        "folded": False,
        "hand": [],
        "current_bet": 0,
        "community_cards": []

    }

    while True:
        message = client_socket.recv(1024)
        command, data = decode_message(message)
        if command == "print":
            print(data)
        elif command == "players_list":
            print(f"The current list of players is:\n")
            for player in data:
                print(player)
        
        elif command == "sync_data":
            game_data = data

        elif command == "get_options":
            print("-------------------")    
            print("It's your turn.")
            print(f"Your hand: {cards_to_string(game_data['hand'])}")
            if game_data['community_cards'] != []:
                print(f"Community cards: {cards_to_string(game_data['community_cards'])}")
            print(f"Your money: {game_data['money']}, Your bet: {game_data['bet']}, Current bet: {game_data['current_bet']}")
            print("-------------------\n")

            choose_action(data,client_socket,game_data)
            
        elif command == "cant_raise":
            raise_bet(client_socket,game_data)

        elif command == "cant_call":
            print("You can't call. Please choose another action.")
            options= ["fold", "all_in"]
            choose_action(options,client_socket,game_data)

        elif command == "invalid_action":
            print(data)

        elif command == "community_cards":
            print(f"Community cards are : {cards_to_string(data)}")
        
        elif command == "ENDGAME":
            print(data)
            return
  







if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", '-p', type=int, help="Enter the server IP address", required=True)
    parser.add_argument("--name" , '-n' ,type=str , help="Enter the player's name", required=True)
    #If the server IP is not specified, it will default to localhost
    parser.add_argument("--server_ip", '-s',type=str, help="Enter the server IP address", default="localhost" , required=False)

    args = parser.parse_args()

    server_socket,chat_port = connect_to_server(args.server_ip, args.port, args.name)

    #Launch the chat client in a separate process in another terminal to avoid cluttering the current terminal
    
    chat = subprocess.Popen(['gnome-terminal', '--', 'python3', 'chat_client.py', '--port', str(chat_port), '--name', args.name])
    

    handle_game(server_socket)

    server_socket.close()
    chat.kill()