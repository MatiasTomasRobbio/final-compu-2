import itertools

ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']


def determine_best_hand(player_hand, community_cards):
    all_cards = player_hand + community_cards

    possible_hands = []

    # Generate all possible combinations of 5 cards
    combinations = itertools.combinations(all_cards, 5)

    # Evaluate each combination to determine the hand
    for combination in combinations:
        
        hand_rank = evaluate_hand(combination)
        possible_hands.append((combination, hand_rank))

    # Sort the possible hands by rank in descending order
    possible_hands.sort(key=lambda x: x[1], reverse=True)

    # Return the best hand rank and highest card
    best_hand_rank = possible_hands[0][1]
    highest_card = max(player_hand, key=lambda x: ranks.index(x[0]))  # Find the highest card in the player's hand
    
    return best_hand_rank, highest_card

def evaluate_hand(hand):
    ranks = [card[0] for card in hand]

    # Count occurrences of each rank
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}


    # Sort ranks in descending order of occurrences
    sorted_ranks = sorted(rank_counts.keys(), key=lambda x: (rank_counts[x], ranks.index(x)), reverse=True)

    # Check for royal flush and straight flush
    if is_straight(hand) and is_flush(hand):
        if sorted_ranks[0] == '10':
            return 9
        else:
            return 8

    # Check for four of a kind
    for count in rank_counts.items():
        if count == 4:
            return 7

    # Check for full house
    if len(rank_counts) == 2 and 3 in rank_counts.values():
        return 6

    # Check for flush
    if is_flush(hand):
        return 5

    # Check for straight
    if is_straight(hand):
        return 4

    # Check for three of a kind
    for count in rank_counts.items():
        if count == 3:
            return 3

    # Check for two pairs
    if list(rank_counts.values()).count(2) == 2:
        return 2

    # Check for one pair
    if 2 in rank_counts.values():
        return 1

    # If none of the above, return the highest card
    return 0


def is_straight(hand):
    ranks = [card[0] for card in hand]
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    sorted_ranks = sorted(ranks, key=lambda x: rank_values[x])
    for i in range(len(sorted_ranks) - 1):
        if rank_values[sorted_ranks[i]] != rank_values[sorted_ranks[i + 1]] - 1:
            return False
    return True


def is_flush(hand):
    suits = [card[1] for card in hand]
    return len(set(suits)) == 1





# Test the function
player_hand = [('K', 'Clubs'), ('3', 'Clubs')]
community_cards = [('J', 'Hearts'), ('J', 'Clubs'), ('9', 'Diamonds'), ('9', 'Clubs'), ('2', 'Diamonds')]
hand_to_text = {9: 'Royal Flush', 8: 'Straight Flush', 7: 'Four of a Kind', 6: 'Full House', 5: 'Flush', 4: 'Straight', 3: 'Three of a Kind', 2: 'Two Pair', 1: 'One Pair', 0: 'High Card'}

best_hand_rank, highest_card = determine_best_hand(player_hand, community_cards)
print(f'Best Hand: {hand_to_text[best_hand_rank]}', f'Highest Card: {highest_card}')  

