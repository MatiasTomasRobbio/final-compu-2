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
    