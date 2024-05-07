class Player:
    def __init__(self, name, money,connection)-> None:
        self.name = name
        self.money = money
        self.hand = []
        self.bet = 0
        self.folded = False
        self.all_in = False
        self.conn = connection  # The socket connection to the player

    def reset(self)-> None:
        self.hand = []
        self.bet = 0
        self.folded = False
        self.all_in = False

    def __str__(self) -> str:
        #Prints all the attributes of the player
        return f"Name: {self.name}, Money: {self.money}, Hand:{self.hand}, Bet:{self.bet}, Folded:{self.folded}, All in: {self.all_in}."
    

    ##ONLY FOR TESTING PURPOSES### THIS WILL NOT BE USED IN THE SERVER SIDE
    def cards_string(self):
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
        #Converts the card tuple to a symbol and number string
        return str(f"{self.hand[0][0]}{suits[self.hand[0][1]]},{self.hand[1][0]}{suits[self.hand[1][1]]}")