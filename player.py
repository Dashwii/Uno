import pygame

"""
A player/ai moveset might work better being kept in the class as a statemachine.
It would cut down on the if elses and hopefully make the code for a player/ai move clearer to follow.
"""


class Player:
    def __init__(self, name):
        self.camera_pov = True
        self.name = name
        self.deck = []
        self.threat_level = 0
        self.current_hovered_card_index = 0
        self.move_ticker = 0
        self.status = None
        self.state = None
        self.decision = None

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
 