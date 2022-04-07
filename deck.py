import random
from init_stuff import *


class Card:
    def __init__(self, card_color, card_type):
        self.card_color = card_color
        self.card_type = card_type
        self.rect = pygame.Rect((0, 0), (CARD_WIDTH, CARD_HEIGHT))
        self.rotation = 0
        # For wild cards
        self.wild_color = None
        self.image = card_image_map[(self.card_color.title(), str(self.card_type))]

        self.destination_x = 0
        self.destination_y = 0

        self.show_face_leaving = False

        self.sort_num = 0

    def switch_wild_color(self, selected_color):
        # If wild card switch game color
        self.wild_color = selected_color

    def reset_wild_color(self):
        self.wild_color = None

    def __repr__(self):
        return f"({self.card_color}, {self.card_type})"


def return_deck():
    colors = ["red", "blue", "green", "yellow"]
    specials = ["skip", "reverse", "draw"]
    deck = []
    for color in colors:  # Append 0-9 color cards
        for card_type in range(0, 10):
            card = Card(color, card_type)
            sort(card)
            deck.append(card)

    for color in colors:  # Append 1-9 color cards 
        for card_type in range(1, 10):
            card = Card(color, card_type)
            sort(card)
            deck.append(card)
    for color in colors:  # Append special cards
        for card_type in specials:
            for _ in range(2):
                card = Card(color, card_type)
                sort(card)
                deck.append(card)
    for _ in range(4):    # Append black cards. None in third index is the possible color for the card to change into.
        card_wild = Card("black", "wild")
        sort(card_wild)
        deck.append(card_wild)
        card_wild_draw = Card("black", "wild draw")
        sort(card_wild_draw)
        deck.append(card_wild_draw)
    random.shuffle(deck)
    return deck 


def sort(card):
    sort_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, "reverse": 10, "skip": 11, "draw": 12, "wild": 13, "wild draw": 14}
    card.sort_num = sort_map[card.card_type]