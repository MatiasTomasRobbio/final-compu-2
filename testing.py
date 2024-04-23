from poker_game_app.server.classes import *

deck = Deck()

player1 = Player("Alice", 100)
player2 = Player("Bob", 100)
players = [player1, player2]

deck.shuffle()
deck.deal_to_players(players, 2)



