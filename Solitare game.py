import random

# Initialize deck of cards
suits = ['♠', '♣', '♦', '♥']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
deck = [(rank, suit) for suit in suits for rank in ranks]
random.shuffle(deck)

# Initialize game board
tableau = [[] for _ in range(7)]
foundation = {suit: [] for suit in suits}
stock = deck[:24]
waste = []

# Deal cards onto the tableau
for i, row in enumerate(tableau):
    row.extend(stock[:i+1])
    del stock[:i+1]

# Function to display the current game state
def display_board():
    print("Tableau:")
    for row in tableau:
        print("  ".join(card[0] + card[1] for card in row))
    print("\nFoundation:")
    for suit, cards in foundation.items():
        print(f"{suit}: " + " ".join(card[0] + card[1] for card in cards))
    print("\nStock: " + str(len(stock)) + " cards")
    print("Waste: " + " ".join(card[0] + card[1] for card in waste))

# Function to check if a move is valid
def is_valid_move(card, dest):
    if not dest:
        return card[0] == 'K'
    dest_rank, dest_suit = dest[-1]
    rank_idx = ranks.index(card[0])
    dest_rank_idx = ranks.index(dest_rank)
    return (rank_idx + 1 == dest_rank_idx and card[1] != dest_suit)

# Function to move a card
def move_card(card, src, dest):
    src.remove(card)
    dest.append(card)

# Main game loop
while True:
    display_board()

    # Check for game over
    if all(len(cards) == 13 for cards in foundation.values()):
        print("Congratulations! You won!")
        break

    # Prompt for player's move
    move_from = input("Enter the source pile (1-7 for tableau, S for stock, or W for waste): ")
    move_to = input("Enter the destination pile (F for foundation or 1-7 for tableau): ")

    # Process player's move
    if move_from == 'S':
        if stock:
            waste.append(stock.pop())
        else:
            stock = waste[::-1]
            waste.clear()
    elif move_from == 'W':
        if waste:
            move_card(waste[-1], waste, tableau[int(move_to)-1])
    else:
        move_from_pile = tableau[int(move_from)-1]
        if move_from_pile:
            if move_to == 'F':
                if is_valid_move(move_from_pile[-1], foundation):
                    move_card(move_from_pile[-1], move_from_pile, foundation[move_from_pile[-1][1]])
            else:
                move_to_pile = tableau[int(move_to)-1]
                if move_to_pile and is_valid_move(move_from_pile[-1], move_to_pile):
                    move_card(move_from_pile[-1], move_from_pile, move_to_pile)

    # Clear the console window (works on most systems)
    print("\033c")