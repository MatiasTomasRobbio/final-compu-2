import multiprocessing

# Define card ranks, suits, and values
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Function to evaluate the hand of each player
def evaluate_hand(hand):
    # Extract ranks and suits from the hand
    ranks = [card[0] for card in hand]
    suits = [card[1] for card in hand]

    # Count occurrences of each rank
    rank_counts = {rank: ranks.count(rank) for rank in ranks}

    # Check for flush
    is_flush = len(set(suits)) == 1

    # Check for straight
    is_straight = len(set(ranks)) == 5 and (max(ranks) - min(ranks) == 4 or set(ranks) == {'A', '2', '3', '4', '5'})

    # Check for straight flush or royal flush
    if is_straight and is_flush:
        if set(ranks) == {'10', 'J', 'Q', 'K', 'A'}:
            return "Royal Flush", max(ranks)
        else:
            return "Straight Flush", max(ranks)

    # Check for four of a kind
    if 4 in rank_counts.values():
        return "Four of a Kind", max(rank_counts, key=rank_counts.get)

    # Check for full house
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return "Full House", max(rank_counts, key=rank_counts.get)

    # Check for flush
    if is_flush:
        return "Flush", max(ranks)

    # Check for straight
    if is_straight:
        return "Straight", max(ranks)

    # Check for three of a kind
    if 3 in rank_counts.values():
        return "Three of a Kind", max(rank_counts, key=rank_counts.get)

    # Check for two pairs
    if list(rank_counts.values()).count(2) == 4:
        return "Two Pair", max(rank_counts, key=rank_counts.get)

    # Check for one pair
    if 2 in rank_counts.values():
        return "One Pair", max(rank_counts, key=rank_counts.get)

    # High card
    return "High Card", max(ranks)

# Function to evaluate hands in parallel
def evaluate_hands_parallel(hands):
    with multiprocessing.Pool() as pool:
        results = pool.map(evaluate_hand, hands)
    return results

if __name__ == "__main__":

    # Example community cards (the board)
    community_cards = [('Q', 'Hearts'), ('J', 'Hearts'), ('10', 'Hearts'), ('9', 'Hearts'), ('8', 'Hearts')]

    # Example hands
    hands = [
        [('2', 'Hearts'), ('3', 'Hearts'), ('4', 'Hearts'), ('5', 'Hearts'), ('6', 'Hearts')],
        [('10', 'Clubs'), ('J', 'Clubs'), ('Q', 'Clubs'), ('K', 'Clubs'), ('A', 'Clubs')],
        [('5', 'Spades'), ('5', 'Diamonds'), ('5', 'Clubs'), ('5', 'Hearts'), ('A', 'Spades')]
    ]

    # Evaluate hands in parallel
    results = evaluate_hands_parallel(hands)

    print(results)
