import argparse
import random
import itertools

# Define card ranks, suits, and values
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Function to create and shuffle a deck of cards
def create_deck():
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

# Function to deal community cards (flop, turn, river)
def deal_community_cards(deck,community_cards,number):
    for _ in range(number):  # Flop, turn, river
        card = deck.pop()
        community_cards.append(card)
    return community_cards

# Function to deal cards to players

def deal_cards(deck, players):
    # Shuffle the deck
    random.shuffle(deck)

    # Initialize a list to hold player cards
    player_cards = []

    # Deal two cards to each player
    for player in players:
        # Remove two cards from the deck and add them to the player's hand
        player_hand = [deck.pop(), deck.pop()]
        player_cards.append({"name": player["name"], "cards": player_hand ,"all_in": False})

    return player_cards


def create_player_list(num_players, starting_money):
    players = []
    for i in range(1, num_players + 1):
        player = {"name": f"Player {i}", "money": starting_money}
        players.append(player)
    return players


# This part will initialize the betting round
# Looping through each player in the players_in_hand list asking for their action being the actions:
    # Check (if it's allowed)
    # Bet (if there's no bet yet) or Raise (if there's a bet)
    # Fold (if the player wants to fold adding him to the players_that_folded list ))
    # Call (if the player hasn´t made the highest bet yet)
# If there's only one player that hasn't folded, the function ends and returns everyone_folds = True and the pot ending the hand subsequentely
# After each loop all players in the players_that_folded list are removed from the players_in_hand list
# After the first loop the funtion ends if there's only one player in the players_in_hand list or if all the bets are equal

################
#auxiliary funtions for the betting round

def get_player_money(player_list,player_name):
    for player in player_list:
        if player['name'] == player_name:
            return player['money']

def check_if_enough_money(player_list,bet,player_name):
    for player in player_list:
        if player['name'] == player_name:
            if player['money'] > bet:
                return True
            else:
                return False
            
def go_all_in(player_money,players_in_hand,player_name):
    #Extracts the money value for a ceratin player_name form player_list and asigns returing the bet value and setting  the all_in value in the players_in_hand list to True
    for player in players_in_hand:
        if player['name'] == player_name:
            player['all_in'] = True
            bet = player_money
            print(f"{player['name']} goes all-in ({bet})")
            return bet

#Ask the player if he wants to go all in yes then go_all_in() no then return False
def ask_all_in(players_in_hand,player_name,player_money):
    action = input(f"Desea ir all-in ? (Y/N)")
    if action.lower() == "y":
        return go_all_in(player_money,players_in_hand,player_name)
    else:
        return False
    

def subtract_bets(player_list,bets):
    for player in player_list:
        if player['name'] in bets:
            player['money'] -= bets[player['name']]
        
            if player['money'] < 0:
                return(ValueError("El dinero del jugador no puede ser negativo"))
    return

def delete_folded_players(players_in_hand, players_that_folded):
    new_players_in_hand = [player for player in players_in_hand if player not in players_that_folded]
    return new_players_in_hand


###################

#Main function to run a betting round
def betting_round(players_in_hand,player_list, pot):
    everyone_folds = False
    bets = {player['name']: 0 for player in players_in_hand}
    players_that_folded = []


    while True:
        for player in players_in_hand:
            #If the player has gone all in they will not participate in any more bets till the end of the hand
            if player["all_in"] == True:
                continue

            #If not they will be shown the options they have 

            options = [] 
            max_bet = max(bets.values())

           

            if bets[player['name']] == 0:
                options.append("Bet")
            elif player["all_in"] == False:
                options.append("Raise")
            if player["all_in"] == False:
                options.append("Fold")
            if bets[player['name']] < max_bet:
                options.append("Call")
            if bets[player['name']] == max_bet or player["all_in"] == True:
                options.append("Check")
           
     
           
      


            #extracts how much money the player has available to bet
            player_money = get_player_money(player_list,player['name'])

            print(f"Es el turno de : {player['name']}, su dinero disponible es: {player_money} ")
            
            #Loops until the user enters a valid action
            while True:

                
                action = input(f"Que desea hacer? {options}").lower() #Converts the input to lower case to avoid case sensitive errors
                options = [x.lower() for x in options] #Converts the options to lower case to avoid case sensitive errors

        
           

                if action == "check" and action in options:
                    print(f"{player['name']} Checks")
                    break

                elif (action == "bet" or action == "raise") and action in options:
                    if action == "bet":
                        bet = int(input(f"Place your bet (minimum {max_bet}):"))
                    elif action == "raise":
                        bet = int(input(f"Amount to raise (minimum {max_bet}):"))
                    
                    #check if player has enough money to bet
                    if bet >= max_bet :
                        if bet > player_money:
                            print("No tienes suficiente dinero para realizar esta apuesta")
                            bet = ask_all_in(players_in_hand,player['name'],player_money)
                            if bet == False:
                                print("Accion invalida, intenta de nuevo")
                                continue
                            else:
                                break

                        elif bet == player_money:
                            bet = go_all_in(player_money,players_in_hand,player['name'])

                            break

                        elif bet < player_money:
                            print(f"{player['name']} apuesta {bet}")
                            bets[player['name']] = bet
                            break


                       
                    else:
                        print("La apuesta debe ser mayor o igual a la apuesta mas alta")

                elif action == "call":
                    if max_bet > player_money:
                        print("No tienes suficiente dinero para igualar la apuesta")
                        bet = ask_all_in(players_in_hand,player['name'],player_money)
                        if bet == False:
                            print("Accion invalida, intenta de nuevo")
                            continue
                        else:
                            break
                    else:
                        bet = max_bet
                        print(f"{player['name']} iguala la apuesta ({bet})")
                        break

                elif action == "fold":
                    print(f"{player['name']} folds")
                    players_that_folded.append(player)
                    break

                else:
                    print("Accion invalida, intenta de nuevo")
                    continue

            if len(players_that_folded) == len(players_in_hand) - 1:
                everyone_folds = True
                break

        players_in_hand = delete_folded_players(players_in_hand, players_that_folded)

        if everyone_folds == True or len(set(bets.values())) == 1:
            pot += sum(bets.values())
            subtract_bets(player_list,bets)
       
            return pot, players_in_hand,everyone_folds

###############################################################################################################3
#Funtions to determine the best hand       
                
def determine_best_hand(player_hand, community_cards):
    all_cards = player_hand + community_cards

    possible_hands = []

    # Generate all possible combinations of 5 cards
    combinations = itertools.combinations(all_cards, 5)

    # Evaluate each combination to determine the hand
    for combination in combinations:
        
        hand_rank = evaluate_hand(combination)
        possible_hands.append((combination, hand_rank))

    # Sort the possible hands by rank in descending order
    possible_hands.sort(key=lambda x: x[1], reverse=True)

    # Return the best hand rank and highest card
    best_hand_rank = possible_hands[0][1]
    highest_card = max(player_hand, key=lambda x: ranks.index(x[0]))  # Find the highest card in the player's hand
    
    return best_hand_rank, highest_card


def evaluate_hand(hand):
    ranks = [card[0] for card in hand]

    # Count occurrences of each rank
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}


    # Sort ranks in descending order of occurrences
    sorted_ranks = sorted(rank_counts.keys(), key=lambda x: (rank_counts[x], ranks.index(x)), reverse=True)

    # Check for royal flush and straight flush
    if is_straight(hand) and is_flush(hand):
        if sorted_ranks[0] == '10':
            return 9
        else:
            return 8

    # Check for four of a kind
    for count in rank_counts.items():
        if count == 4:
            return 7

    # Check for full house
    if len(rank_counts) == 2 and 3 in rank_counts.values():
        return 6

    # Check for flush
    if is_flush(hand):
        return 5

    # Check for straight
    if is_straight(hand):
        return 4

    # Check for three of a kind
    for count in rank_counts.items():
        if count == 3:
            return 3

    # Check for two pairs
    if list(rank_counts.values()).count(2) == 2:
        return 2

    # Check for one pair
    if 2 in rank_counts.values():
        return 1

    # If none of the above, return the highest card
    return 0


def is_straight(hand):
    ranks = [card[0] for card in hand]
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    sorted_ranks = sorted(ranks, key=lambda x: rank_values[x])
    for i in range(len(sorted_ranks) - 1):
        if rank_values[sorted_ranks[i]] != rank_values[sorted_ranks[i + 1]] - 1:
            return False
    return True


def is_flush(hand):
    suits = [card[1] for card in hand]
    return len(set(suits)) == 1

##########################################################################33



# Main function to run a complete hand
def hand(player_list):
    # Create and shuffle the deck
    deck = create_deck()
    # Deal two cards to each player
    players_in_hand = deal_cards(deck, player_list)
    #Initialize the community cards as empty for the preflop round
    community_cards = []
    # Initialize the pot
    pot = 0
   
    rounds = ["Preflop","Flop","Turn","River"]
    community_cards_numbers = [0,3,1,1]

    # Run the betting round for each round
    for round in rounds:
        print(f"Starting {round} round")
        
        community_cards = deal_community_cards(deck,community_cards,community_cards_numbers[rounds.index(round)])
        print(f"Community cards: {community_cards}")
        pot, players_in_hand,everyone_folds = betting_round(players_in_hand,player_list, pot)
        if everyone_folds == True:
            print("Todos los jugadores se retiraron")
            winner = players_in_hand[0]['name']
            print(f"El ganador es:{winner}")
            
            return pot, winner
        
    

            

    






   


 
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Texas Hold\'em game with specified settings.')
    parser.add_argument('--player_quantity', type=int, default=5, help='Number of players required to start game and maximum players')
    parser.add_argument('--starting_money', type=int, default=1000, help='Starting money for each player')
    args = parser.parse_args()
    player_list = create_player_list(args.player_quantity,args.starting_money)
    deck = create_deck()
    players_hands = deal_cards(deck, player_list)
    print(players_hands)
    pot, winner = hand(player_list)
    
    
