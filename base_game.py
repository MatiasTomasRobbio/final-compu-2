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

    # Initialize a hand for each player if it doesn't exist
    for player in players:
        if "hand" not in player:
            player["hand"] = []

    # Deal two cards to each player
    for _ in range(2):
        for player in players:
            # Remove the card from the deck and add it to the player's hand
            player["hand"].append(deck.pop())


def create_player_list(num_players, starting_money):
    players = []
    for i in range(1, num_players + 1):
        player = {"name": f"Player {i}", "money": starting_money}
        players.append(player)
    return players

# Main function to run a complete hand
def hand(player_list):
    # Create and shuffle the deck
    deck = create_deck()

    
    # Deal hole cards to players
    hole_cards = deal_cards(deck, len(player_list))

   


 
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Texas Hold\'em game with specified settings.')
    parser.add_argument('--player_quantity', type=int, default=5, help='Number of players required to start game and maximum players')
    parser.add_argument('--starting_money', type=int, default=1000, help='Starting money for each player')
    args = parser.parse_args()
    player_list = create_player_list(args.player_quantity,args.starting_money)
    deck = create_deck()
    print(len(deck))
    deal_cards(deck,player_list)
    print(len(deck))
    print(player_list)
    
