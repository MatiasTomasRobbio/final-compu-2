from poker_game_app.server.classes import *

deck = Deck()

player1 = Player("Alice", 100)
player2 = Player("Bob", 100)
player3 = Player("Charlie", 100)
player4 = Player("David", 100)

player1.bet = 10
players = [player1, player2, player3, player4]

game = Game(players)
round = Round(players)

options = round.determine_possible_actions(player1, 10)
#Make the first letter uppercase for each option when printing

print(f"What would you like to do? {[option.capitalize() for option in options]}")





