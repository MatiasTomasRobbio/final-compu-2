import random

class Deck:
    def __init__(self)-> None:
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = self.create_new_deck()
        self.shuffle()

    def create_new_deck(self):
        deck = [(rank, suit) for rank in self.ranks for suit in self.suits]
        deck
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