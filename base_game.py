import argparse
import random

# Define card ranks, suits, and values
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Function to create and shuffle a deck of cards
def create_deck():
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

# Function to deal community cards (flop, turn, river)
def deal_community_cards(deck):
    community_cards = []
    for _ in range(5):  # Flop, turn, river
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
        player_cards.append({"name": player["name"], "cards": player_hand})

    return player_cards


def create_player_list(num_players, starting_money):
    players = []
    for i in range(1, num_players + 1):
        player = {"name": f"Player {i}", "money": starting_money}
        players.append(player)
    return players

# This funtion will initialize the betting round
# Looping through each player in the players_in_hand list asking for their action being the actions:
    # Check (if it's allowed)
    # Bet (if there's no bet yet) or Raise (if there's a bet)
    # Fold (if the player wants to fold adding him to the players_that_folded list ))
    # Call (if the player hasn´t made the highest bet yet)
# If there's only one player that hasn't folded, he wins the pot and the hand ends
# After each loop all players in the players_that_folded list are removed from the players_in_hand list
# After the first loop the funtion ends if there's only one player in the players_in_hand list or if all the bets are equal

def betting_round(players_in_hand, pot):
    bets = {player['name']: 0 for player in players_in_hand}
    players_that_folded = []
    while True:
        for player in players_in_hand:
            options = ""
            action = input(f"Es el turno de : {player['name']}, que desea hacer? {options}")
            if action == "Check":
                pass
            elif action == "Bet":
                pass
            elif action == "Raise":
                pass
            elif action == "Fold":
                players_that_folded.append(player)
            elif action == "Call":
                pass
        for player in players_that_folded:
            players_in_hand.remove(player)

    #len(players_in_hand) > 1 and len(set(bets.values())) > 1:
    
 


# Main function to run a complete hand
def hand(player_list):
    # Create and shuffle the deck
    deck = create_deck()
    pass


   


 
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Texas Hold\'em game with specified settings.')
    parser.add_argument('--player_quantity', type=int, default=5, help='Number of players required to start game and maximum players')
    parser.add_argument('--starting_money', type=int, default=1000, help='Starting money for each player')
    args = parser.parse_args()
    player_list = create_player_list(args.player_quantity,args.starting_money)
    deck = create_deck()
    player_cards = deal_cards(deck, player_list)
    print(player_cards)
    
    
