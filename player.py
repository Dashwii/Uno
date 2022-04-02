from init_stuff import *
from draw_text import DrawText


class Player:
    def __init__(self, name):
        self.camera_pov = True
        self.name = name
        self.deck = []
        self.last_added_card = None
        self.stack_threat = False
        self.current_hovered_card_index = 0
        self.status = None
        self.decision = None
        self.index = False

    def input(self, events, current_board_color, current_board_type):
        if self.decision is not None:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.current_hovered_card_index - 1 < 0:
                        self.current_hovered_card_index = len(self.deck) - 1
                    else:
                        self.current_hovered_card_index -= 1
                if event.key == pygame.K_RIGHT:
                    if self.current_hovered_card_index + 1 > len(self.deck) - 1:
                        self.current_hovered_card_index = 0
                    else:
                        self.current_hovered_card_index += 1
                if event.key == pygame.K_SPACE:
                    self.check_valid(current_board_color, current_board_type)

    def check_valid(self, current_board_color, current_board_type):
        if self.deck[self.current_hovered_card_index].card_type == "wild draw":
            self.decision = self.deck[self.current_hovered_card_index]
        elif self.deck[self.current_hovered_card_index].card_type == "wild" and not self.stack_threat:
            self.decision = self.deck[self.current_hovered_card_index]
        elif current_board_color is None:
            self.decision = self.deck[self.current_hovered_card_index]
        else:
            if self.stack_threat:
                if self.deck[self.current_hovered_card_index].card_type == "draw":
                    self.decision = self.deck[self.current_hovered_card_index]
            else:
                if self.deck[self.current_hovered_card_index].card_color == current_board_color or self.deck[self.current_hovered_card_index].card_type == current_board_type:
                    self.decision = self.deck[self.current_hovered_card_index]

    def auto_highlight(self, current_board_color, current_board_type):
        for i, card in enumerate(self.deck):
            if card.card_color == current_board_color or card.card_type in (current_board_type, "wild", "wild draw"):
                self.current_hovered_card_index = i
                break

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

    def __repr__(self):
        return self.name


class Button:
    def __init__(self, position=None, dimensions=None, button_color=None, text=None, text_color="black"):
        self.display = display
        self.position_x = position[0]
        self.position_y = position[1]

        self.button_color = button_color
        self.dimension_w = dimensions[0]
        self.dimension_h = dimensions[1]

        self.button_rect = pygame.Rect((self.position_x, self.position_y), (self.dimension_w, self.dimension_h))

        self.text = text
        if self.text is not None:
            self.text_render = DrawText(self.text, [0, 0], font_size=35, color=text_color)
            self.text_render.position[0] = self.position_x + (self.text_render.text_surface.get_rect().x // 2)
            self.text_render.position[1] = self.position_y + (self.text_render.text_surface.get_rect().y // 2)
        if button_color is not None:
            self.button_color = button_color

    def update(self, events):
        if self.button_color is not None:
            pygame.draw.rect(self.display, self.button_color, self.button_rect)
        if self.text is not None:
            self.text_render.render()
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(mouse_pos):
                    return True
        else:
            return False


unused_deck_button = Button(position=UNUSED_DECK_POSITION, dimensions=(CARD_WIDTH, CARD_HEIGHT))
play_card_button = Button(position=(WIDTH // 2 + (200 * SCALING_RATIO), HEIGHT - (300 * SCALING_RATIO)), dimensions=(100, 50), button_color="green", text="Play")
keep_card_button = Button(position=(WIDTH // 2 - (300 * SCALING_RATIO), HEIGHT - (300 * SCALING_RATIO)), dimensions=(100, 50), button_color="orange", text="Keep")
CHOICE_CARD_DECISION_X = (WIDTH // 2 - CARD_WIDTH // 2) * SCALING_RATIO
CHOICE_CARD_DECISION_Y = (HEIGHT - (300 * SCALING_RATIO))


def update_choice_buttons(events):
    clicked_p = play_card_button.update(events)
    clicked_k = keep_card_button.update(events)

    if clicked_p:
        return "PLAY"
    elif clicked_k:
        return "KEEP"


def pickup_card(events):
    pickup = unused_deck_button.update(events)
    if pickup:
        return "PICKUP"
