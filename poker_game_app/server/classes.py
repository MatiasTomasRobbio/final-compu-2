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

    def __str__(self) -> str:
        #Prints all the attributes of the player
        return f"Name: {self.name}, Money: {self.money}, Hand:{self.hand}, Bet:{self.bet}, Folded:{self.folded}, All in: {self.all_in}."
    

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

    def betting_round(self):
        #Loops until every player has folded or all the bets are equal
        while True:
            for player in self.participating_players:
                #If the player has gone all in they will not participate in any more bets till the end of the hand
                if player.folded or player.all_in:
                    continue

                print(f"It's {player} turn\n")
                options = self.determine_possible_actions(player,self.current_bet)
                while True:
                    player_action = input(f"What would you like to do? {[option.capitalize() for option in options]} ")
                    if player_action.lower() == "call" and player_action.lower() in options:
                        self.call(player)
                        break
                    if (player_action.lower() == "raise" or player_action.lower() == "bet") and player_action.lower() in options:
                        self.raise_bet(player)
                        break
                    elif player_action.lower() == "fold" and player_action.lower() in options:
                        self.fold(player)
                        break
                    elif player_action.lower() == "check"and player_action.lower() in options:
                        print(f"{player.name} checks.")
                        break
                    else:
                        print("Invalid action. Please try again.")
                        continue
            #Check if all the bets are equal
            if all(player.bet == self.current_bet for player in self.participating_players if not player.folded):
                return False, None
            #If all the players have folded except one, that player wins the pot
            if len([player for player in self.participating_players if not player.folded]) == 1:
                winning_player = [player for player in self.participating_players if not player.folded][0]
                return True, winning_player
                
        
    
    #Selects the actions that a player can perform in their turn
    def determine_possible_actions(self,player,current_bet):
        
        options = []
        #Fold is always available
        options.append("fold")

        if player.bet == 0 : 
            options.append("bet")
        elif not player.all_in :
            options.append("raise")
        
        if player.bet < current_bet:
            options.append("call")
        
        if player.bet <= current_bet:
            options.append("check")
        
        if player.money != 0 and player.all_in == False:
            options.append("all in")

        return options    
        
    ######## Call option ########
    def call (self,player):
      #Check if the player has enough money to call
        if player.money >= self.current_bet - player.bet:
            player.money -= self.current_bet - player.bet
            player.bet = self.current_bet
            print(f"{player.name} calls.")
        else:
            print("Not enough money to call.")
            while True:
                player_action = input(" Would you like to ['Fold', 'All in'].")
                if player_action.lower() == "fold":
                    self.fold(player)
                    break
                elif player_action.lower() == "all in":
                    self.all_in(player)
                    break
                else:
                    print("Invalid action. Please try again.")
                    continue

    ######## Fold option ########
    def fold (self,player):
        player.folded = True
        print(f"{player.name} folds.")


    ######## Raise / Bet Option ########
    def raise_bet(self,player,current_bet):

        if player.bet == 0:
            string = "bet"
        else:
            string = "raise to"
        while True:
            bet_amount = int(input(f"How much would you like to {string}? "))

            #Check if the player has enough money to raise
            if player.money > bet_amount:
                if bet_amount < current_bet:
                    print(f"Raise must be at least {current_bet}.")
                    continue
                else:
                    player.money -= bet_amount
                    player.bet += bet_amount
                    self.current_bet += bet_amount
                    print(f"{player.name} raises by {bet_amount}.")
                    break
            elif player.money == bet_amount:
                self.all_in(player)
                break
            else:
                print(f"Not enough money to {string}. ")
                self.all_in(player)
    
    ######## All in option ########
    def all_in(self,player):
        player.bet += player.money
        player.all_in = True
        print(f"{player.name} goes all in.")