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

for suit, symbol in suits.items():
    print(f"{suit} {symbol}")