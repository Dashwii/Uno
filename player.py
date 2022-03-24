import pygame
import time

"""
Gonna rework the player class to look at it's current situation and send 'commands' to the game class
on specific moves it needs to do. Like in an interation we'll send a 'pickup' command and the game class
will respond by appending cards to the players deck when it's ready. This should make edge cases simpler
to squash as the if chain in the game loop is getting messy. 
"""


class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.current_hovered_card_index = 0
        self.command = None

        self.board_color, self.board_type = None, None

        self.stack_threat = None

        self.input_delay = 0

    def get_input(self):
        time_since_delay = time.time() - self.input_delay
        if not time_since_delay > 10:
            return
        else:
            self.input_delay = time.time()
        self.handle_input()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.current_hovered_card_index - 1 < 0:
                self.current_hovered_card_index = len(self.deck) - 1
            else:
                self.current_hovered_card_index -= 1
        elif keys[pygame.K_RIGHT]:
            if self.current_hovered_card_index + 1 > len(self.deck) - 1:
                self.current_hovered_card_index = 0
        elif keys[pygame.K_SPACE]:
            self.verify_play()

    def verify_play(self):
        card = self.deck[self.current_hovered_card_index]

        if self.board_color is None:
            self.command = "PLAY"
        elif card.card_type == "wild draw":
            self.command = "PLAY"
        elif card.card_type == "wild" and not self.stack_threat:
            self.command = "PLAY"
        else:
            if self.stack_threat:
                if card.card_color == self.board_color and card.card_type == "draw":
                    self.command = "PLAY"
            else:
                if card.card_color == self.board_color or card.card_type == self.board_type:
                    self.command = "PLAY"


    def retrieve_played_card(self):
        return_card = self.deck.pop(self.current_hovered_card_index)
        return return_card

    def input(self, current_board_color, current_board_type):
        if self.decision is not None:
            return
        self.move_ticker += 1
        keys = pygame.key.get_pressed()
        if self.move_ticker > 10:
            if keys[pygame.K_LEFT]:
                if self.current_hovered_card_index - 1 < 0:
                    self.current_hovered_card_index = len(self.deck) - 1
                else:
                    self.current_hovered_card_index -= 1
            if keys[pygame.K_RIGHT]:
                if self.current_hovered_card_index + 1 > len(self.deck):
                    self.current_hovered_card_index = 0
                else:
                    self.current_hovered_card_index += 1
            if keys[pygame.K_p]:
                self.decision = "pickup"
            if keys[pygame.K_SPACE]:
                if self.deck[self.current_hovered_card_index].card_type == "wild draw":
                    self.decision = self.deck[self.current_hovered_card_index]
                elif self.deck[self.current_hovered_card_index].card_type == "wild" and not self.threat_level:
                    self.decision = self.deck[self.current_hovered_card_index]
                elif current_board_color is None:
                    self.decision = self.deck[self.current_hovered_card_index]
                else:
                    if self.threat_level:
                        if self.deck[self.current_hovered_card_index].card_type == "draw":
                            self.decision = self.deck[self.current_hovered_card_index]
                    else:
                        if self.deck[self.current_hovered_card_index].card_color == current_board_color or self.deck[self.current_hovered_card_index].card_type == current_board_type:
                            self.decision = self.deck[self.current_hovered_card_index]

            self.move_ticker = 0

    def sort_cards_visual(self):
        red_cards = []
        green_cards = []
        blue_cards = []
        yellow_cards = []
        black_cards = []
        for card in self.deck:
            if card.card_color == "red":
                red_cards.append(card)
            if card.card_color == "green":
                green_cards.append(card)
            if card.card_color == "blue":
                blue_cards.append(card)
            if card.card_color == "yellow":
                yellow_cards.append(card)
            if card.card_color == "black":
                black_cards.append(card)
        red_cards.sort(key=lambda card: card.sort_num)
        green_cards.sort(key=lambda card: card.sort_num)
        blue_cards.sort(key=lambda card: card.sort_num)
        yellow_cards.sort(key=lambda card: card.sort_num)
        black_cards.sort(key=lambda card: card.sort_num)
        self.deck = red_cards + green_cards + blue_cards + yellow_cards + black_cards

    def choose_new_color_wild(self, card_index, chosen_card):
        pass

    def __repr__(self):
        return self.name 
 