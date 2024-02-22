def modify_list(my_list):
    # Pop an item from the list
    if my_list:
        my_list.pop()
    else:
        print("List is empty")

# Original deck of cards
deck = ['A', 'K', 'Q', 'J', '10']

# Passing the deck to the function
modify_list(deck)

# Printing the modified deck
print("Modified deck:", deck)
