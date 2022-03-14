import random 





def return_deck():
    colors = ["red", "blue", "green", "yellow"]
    specials = ["skip", "reverse", "draw"]
    deck = []
    for color in colors:  # Append 0-9 color cards
        for number in range(0, 10):
            deck.append((color, number))
    for color in colors:  # Append 1-9 color cards 
        for number in range(1, 10):
            deck.append((color, number))
    for color in colors:  # Append special cards
        for special in specials:
            deck.append((color, special))
            deck.append((color, special))
    for _ in range(4):    # Append black cards. None in third index is the possible color for the card to change into.
        deck.append(["black", "wild", None])
        deck.append(["black", "wild draw", None])
    random.shuffle(deck)
    return deck 
