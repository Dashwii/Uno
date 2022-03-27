from init_stuff import *
from render_helper import *


color_map = {"red": RED, "green": GREEN, "blue": BLUE, "yellow": YELLOW, "black": WHITE}


class CardRendering:
    def __init__(self, board):
        self.board = board
        self.rotation_list = self.board.rotation_list
        self.display = pygame.display.get_surface()
        self.camera_pov_index = self.board.camera_pov_index
        self.name_renders = create_ai_render_names(self.rotation_list, self.camera_pov_index)

        self.moving_cards_leaving = []  # <--- Make this also a list for future jump in mechanic. Will have multiple cards leaving their deck and animated
        self.moving_cards = []  # <--- This is only used in game not during the card dealing state (Gonna try and use this during card dealing state)

    def card_leaving_deck_animation(self, card):
        self.moving_cards_leaving.append(card)
        card_leaving_deck_spawn_location(card, self.board.game_flow.current_player_index, self.camera_pov_index)

    def check_moving_cards_leaving_done(self):
        for i, card in enumerate(self.moving_cards_leaving):
            if card.rect.x == card.destination_x and card.rect.y == card.destination_y:
                self.moving_cards_leaving.pop(i)
                self.board.game_flow.used_deck.append(card)
        if len(self.moving_cards_leaving) == 0:
            return True

    def card_pickup_animation(self, card, index):
        self.moving_cards.append(card)
        card_pickup_spawn_location(card, self.rotation_list[index], index, self.camera_pov_index)

    def check_moving_cards_done(self):
        for i, card in enumerate(self.moving_cards):
            if card.rect.x == card.destination_x and card.rect.y == card.destination_y:
                self.moving_cards.pop(i)
        if len(self.moving_cards) == 0:
            return True

    def render_cards(self):
        # Deck renders
        for i, player in enumerate(self.rotation_list):
            for card in player.deck:
                if i == self.camera_pov_index:
                    self.display.blit(card_image_map[(card.card_color.title(), str(card.card_type))], card.rect)
                else:
                    self.display.blit(pygame.transform.rotate(asset_map["Uno Card Back"], card.rotation), card.rect)
        # Render leaving cards
        for i, card in enumerate(self.moving_cards_leaving):
            self.display.blit(pygame.transform.rotate(card_image_map[(card.card_color.title(), str(card.card_type))], card.rotation), card.rect)
        # Render Unused Deck
        self.display.blit(pygame.transform.rotate(asset_map["Uno Card Back"], 20), (250 * SCALING_RATIO, 0, CARD_WIDTH, CARD_HEIGHT))

    def render_ai_names(self):
        for name in self.name_renders:
            name.render()

    def render_used_deck(self, used_deck):
        last_card = used_deck[-1]
        if last_card.card_type == "wild":
            self.display.blit(wild_image_color_map[last_card.wild_color], (WIDTH // 2 - last_card.rect.width // 2, HEIGHT // 2 - last_card.rect.height // 2))
        elif last_card.card_type == "wild draw":
            self.display.blit(wild_draw_image_color_map[last_card.wild_color], (WIDTH // 2 - last_card.rect.width // 2, HEIGHT // 2 - last_card.rect.height // 2))
        else:
            self.display.blit(card_image_map[(last_card.card_color.title(), str(last_card.card_type))], (WIDTH // 2 - last_card.rect.width // 2, HEIGHT // 2 - last_card.rect.height // 2))
