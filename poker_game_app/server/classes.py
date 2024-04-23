#Player Class
import random

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hand = []
        self.bet = 0
        self.folded = False
        self.all_in = False

    def reset(self):
        self.hand = []
        self.bet = 0
        self.folded = False
        self.all_in = False

    def get_cards(self, card):
        self.hand.append(card)



class Deck:
    def __init__(self):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = self.create_new_deck()

    def create_new_deck(self):
        deck = [(rank, suit) for rank in self.ranks for suit in self.suits]
        return deck
    
    def reset(self):
        self.cards = self.create_new_deck()
        

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
    
    def deal_to_players(self, players,num_cards):
        for _ in range(num_cards):
            for player in players:
                player.get_cards(self.draw())

    def __str__(self):
        return f"Deck with {len(self.cards)} cards."
    
