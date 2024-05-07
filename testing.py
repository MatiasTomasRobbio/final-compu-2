from poker_game_app.server.classes import *


player1 = Player("Alice", 100)
player2 = Player("Bob", 100)
player3 = Player("Charlie", 100)

players = [player1, player2, player3]

game = Game(players)


continue_game = True



    


#Game loop
while continue_game:
    
    #Betting Rounds loop


    
    while True:

        #Deal hands to players
        game.deal_hands()
        participating_players = game.get_participating_players()
        #Create the round object with the players that still have money
        round = Round(participating_players)
        
        #Pre-flop round
        print("Starting Pre-flop round \n")
        got_winner, winner = round.start_betting_round()
        if got_winner:
            print(f"\n$$$$$$$$$ All players folded, {winner.name} wins the pot $$$$$$\n")
            break

        
        #Flop
        print("Starting Flop round \n")
        game.deal_community_cards(3)
        game.print_community_cards()
        
        got_winner, winner = round.start_betting_round()
        if got_winner:
            print(f"All players folded, {winner.name} wins the pot")
            break

        
        #Turn
        print("Starting Turn round \n")
        game.deal_community_cards(1)
        game.print_community_cards()
        
        got_winner, winner = round.start_betting_round()
        if got_winner:
            print(f"All players folded, {winner.name} wins the pot")
            break

        
        #River
        print("Starting River round \n")
        game.deal_community_cards(1)
        game.print_community_cards()
        
        got_winner, winner = round.start_betting_round()
        if got_winner:
            print(f"All players folded, {winner.name} wins the pot")
            break
        
        
        
    game.give_pot(winner, round.pot)
    game.reset()

    











