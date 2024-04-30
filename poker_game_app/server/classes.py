#Player Class
import random

class Player:
    def __init__(self, name, money)-> None:
        self.name = name
        self.money = money
        self.hand = []
        self.bet = 0
        self.folded = False
        self.all_in = False

    def reset(self)-> None:
        self.hand = []
        self.bet = 0
        self.folded = False
        self.all_in = False

#Deck 

class Deck:
    def __init__(self)-> None:
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = self.create_new_deck()

    def create_new_deck(self):
        deck = [(rank, suit) for rank in self.ranks for suit in self.suits]
        return deck

    def reset(self)-> None:
        self.cards = self.create_new_deck()

    def shuffle(self)-> None:
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
    
    def deal_cards(self,cards_list,num_cards)-> None:
        for _ in range(num_cards):
            cards_list.append(self.draw())

    def __str__(self):
        return f"Deck with {len(self.cards)} cards."
    

class Game:
    def __init__(self,players_list) -> None:
        #Initialize the game when all players have connected
        self.players = players_list

    def rotate_players(self):
        #Rotate players list so that the first player becomes the second player and so on
        self.players = self.players[1:] + self.players[:1]


                

        

class Round:
    def __init__(self,players_list) -> None:
        self.participating_players = players_list
        self.pot = 0
        self.current_bet = 0
        self.community_cards = []

    def betting_round(self):
    
        for player in self.participating_players:
            if player.folded or player.all_in:
                continue
            print(f"It's {player} turn")
            while True:
                player_action = input(f"What would you like to do? (Call, Raise, Fold, Check) ")
                if player_action.lower() == "call":
                    self.call(player)
                elif player_action.lower() == "raise":
                    self.raise_bet(player)
                elif player_action.lower() == "fold":
                    self.fold(player)
                elif player_action.lower() == "check":
                    self.check(player)
                else:
                    print("Invalid action. Please try again.")
                    continue
        
    

    def check_if_everyone_folded(self):
        #Checks if all players have folded except one and gives the win to the player
        count = 0
        for player in self.participating_players:
            if player.folded:
                count += 1
            if count == len(self.participating_players) - 1:
                return True
        return False
    
    def determine_possible_actions(player,current_bet):
        #Selects the actions that a player can perform in their turn
        options = []
        #Fold is always available
        options.append("Fold")

        if player.bet == 0 : 
            options.append("Bet")
        elif not player.all_in :
            options.append("Raise")
        
        if player.bet < current_bet:
            options.append("Call")
        
        if player.bet <= current_bet:
            options.append("Check")

        return options    
        
        