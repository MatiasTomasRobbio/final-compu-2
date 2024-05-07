from deck_class import Deck
import pickle

        

class Game:
    def __init__(self,players_list) -> None:
        #Initialize the game when all players have connected
        self.players = players_list #ALL PLAYERS IN THE GAME
        self.participating_players = None #PLAYERS THAT STILL HAVE MONEY TO PLAY A ROUND
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0


    def broadcast(self, command, data):
        # Broadcast the message to all connected clients
        for player in self.players:
            player.conn.send(f"{command}:{pickle.dumps(data)}".encode())

    def send_command(self, player, command, data):
        # Send a message to a specific player
        player.conn.send(f"{command}:{pickle.dumps(data)}".encode())

    

    def rotate_players(self):
        #Rotate players list so that the first player becomes the second player and so on
        self.players = self.players[1:] + self.players[:1]

    def deal_hands(self):
        #Deal two cards to each player that can still play
        for player in self.players:
            if player.money > 0:
                self.deck.deal_cards(player.hand,2)

    def give_pot(self,player,pot):
        #Give the pot to the winning player
        player.money += pot
        

    def get_participating_players(self):
        #Return players that still have money to play
        return [player for player in self.players if player.money > 0]

    def deal_community_cards(self,num_cards):
        #Deal community cards
        self.deck.deal_cards(self.community_cards,num_cards)


    def reset(self):
        #Reset the game
        for player in self.players:
            player.reset()
        self.deck.reset()
        self.deck.shuffle()
    
    def print_community_cards(self):
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
        
        print(f"Community cards: ")
        for card in self.community_cards:
            print(f"{card[0]}{suits[card[1]]}", end="")
        print("\n")

        

    def determine_game_status(self):
        #Determine the winner of the game if all but one player has run out of money returning true and the player if there is a winner
        if len([player for player in self.players if player.money != 0]) == 1:
            winning_player = [player for player in self.players if player.money != 0][0]
            return False, winning_player
        return True, None
    
    def get_showdown_winner(self):
        pass


    def print_player_info(self):
        #Prints all the players info
        for player in self.players:
            print(player.__str__())


    def start_betting_round(self):
        #Loops until every player has folded or all the bets are equal
        self.participating_players = self.get_participating_players() #Get the players that can play the round

        while True:

            
            for player in self.participating_players:
                #Before giving the turn to the player check if all others have folded and give the win to him
                if len([player for player in self.participating_players if not player.folded]) == 1:
                    winner = [player for player in self.participating_players if not player.folded][0]
                    return True, winner

                
                #If the player has gone all in they will not participate in any more bets till the end of the hand
                if player.folded or player.all_in:
                    continue


                #Sends all players the name of the player whose turn it is and the current bet
                
                self.broadcast(f"print",f"It's {player.name}'s turn. Current bet: {self.current_bet}")
                #Creates a list with the players hand ,money , bet and current bet to send to the player
                player_data = [player.hand,player.money,player.bet,self.current_bet]

                self.send_command(player,"get_data", f"{player_data}")
                
                options = self.determine_possible_actions(player,self.current_bet)
                self.send_command(player,"get_options", f"{options}")


                while True:
                    player_action = player.conn.recv(1024).decode()
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
                        self.broadcast(f"print",f"{player.name} checks.")
                        break
                    else:
                        self.send_command(player,"invalid_action", "Invalid action. Please try again.")
                        continue


            #Check if all the bets are equal
            if all(player.bet == self.current_bet for player in self.participating_players if not player.folded):
                return False, None
            
                
        
    
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
        
        if player.bet >= current_bet:
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
            self.broadcast(f"print",f"{player.name} calls.")

        else:
            self.send_command(player,"cant_call", "Not enough money to call.")
            while True:
                player_action = player.conn.recv(1024).decode()
                if player_action.lower() == "fold":
                    self.fold(player)
                    break
                elif player_action.lower() == "all in":
                    self.all_in(player)
                    break
                else:
                    self.send_command(player,"invalid_action", "Invalid action. Please try again.")
                    continue

    ######## Fold option ########
    def fold (self,player):
        player.folded = True
        self.broadcast(f"print",f"{player.name} folds.")


    ######## Raise / Bet Option ########
    def raise_bet(self,player):

        while True:
            bet_amount = int(player.conn.recv(1024).decode())

            #Check if the player has enough money to raise
            if player.money > bet_amount:
                if (bet_amount+player.bet) < self.current_bet:
                    self.send_command(player,"cant_raise", f"Raise must be at least {self.current_bet-player.bet}.")
                    continue
                else:
                    player.money -= bet_amount
                    player.bet += bet_amount
                    self.current_bet += bet_amount
                    self.broadcast(f"print",f"{player.name} raises by {bet_amount}. Current bet: {self.current_bet}")
                    break
            elif player.money == bet_amount:
                self.all_in(player)
                break
            else:
                self.send_command(player,"cant_raise", "Not enough money to raise.")
    
    ######## All in option ########
    def all_in(self,player):
        player.bet += player.money
        player.all_in = True
        self.broadcast(f"print",f"{player.name} goes all in with {player.money}.")