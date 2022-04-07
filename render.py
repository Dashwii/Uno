from init_stuff import *
from render_helper import *
from random import randrange


color_map = {"red": RED, "green": GREEN, "blue": BLUE, "yellow": YELLOW, "black": WHITE}


class BoardRendering:
    def __init__(self, board):
        self.board = board
        self.used_deck_render = []
        self.rotation_list = self.board.rotation_list
        self.display = pygame.display.get_surface()
        self.camera_pov_index = self.board.camera_pov_index
        self.name_renders = create_render_names(self.rotation_list, self.camera_pov_index)
        self.show_enemy_cards = False  # For debugging only

        self.moving_cards_leaving = []  # <--- Make this also a list for future jump in mechanic. Will have multiple cards leaving their deck and animated
        self.moving_cards = []  # <--- This is only used in game not during the card dealing state (Gonna try and use this during card dealing state)


    def update_number_of_cards_in_deck_render(self, player_index):
        self.name_renders[player_index][1].update_text(len(self.rotation_list[player_index].deck))

    def update_rotation_interface_color(self, current_player_index, last_player_index=None):
        if current_player_index == self.camera_pov_index:
            if last_player_index is not None:
                self.name_renders[last_player_index][0].update_color("white")
                self.name_renders[last_player_index][1].update_color("white")
        else:
            self.name_renders[current_player_index][0].update_color("green")
            self.name_renders[current_player_index][1].update_color("green")
            if last_player_index != self.camera_pov_index:
                if last_player_index is not None:
                    self.name_renders[last_player_index][0].update_color("white")
                    self.name_renders[last_player_index][1].update_color("white")

    def card_leaving_deck_animation(self, card):
        self.moving_cards_leaving.append(card)
        card_leaving_deck_spawn_location(card, self.board.game_flow.current_player_index, self.camera_pov_index)

    def check_moving_cards_leaving_done(self):
        for i, card in enumerate(self.moving_cards_leaving):
            if card.rect.x == card.destination_x and card.rect.y == card.destination_y:
                card.rotation = randrange(card.rotation - 35, card.rotation + 35)
                self.moving_cards_leaving.pop(i)
                self.board.game_flow.used_deck.append(card)
                self.used_deck_render.append(card)
                if len(self.used_deck_render) > 25:
                    del self.used_deck_render[0]
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

    def render_cards(self, player_color_choosing_state=None):
        # Deck renders
        for i, player in enumerate(self.rotation_list):
            if i == self.camera_pov_index:
                for card in player.deck:
                    self.display.blit(card_image_map[(card.card_color.title(), str(card.card_type))], card.rect)
            elif not player_color_choosing_state:
                for card in player.deck:
                    if not self.show_enemy_cards:
                        self.display.blit(pygame.transform.rotate(asset_map["Uno Card Back"], card.rotation), card.rect)
                    else:
                        self.display.blit(pygame.transform.rotate(card_image_map[(card.card_color.title(), str(card.card_type))], card.rotation), card.rect)

        if player_color_choosing_state:
            return
        else:
            # Render Leaving Cards
            for i, card in enumerate(self.moving_cards_leaving):
                self.display.blit(pygame.transform.rotate(card_image_map[(card.card_color.title(), str(card.card_type))], card.rotation), card.rect)
            # Render Unused Deck
            self.display.blit(pygame.transform.rotate(asset_map["Uno Card Back"], 20), (UNUSED_DECK_POSITION[0], UNUSED_DECK_POSITION[1], CARD_WIDTH, CARD_HEIGHT))
            # Render Used Deck
            self.render_used_deck()

    def render_ai_names(self):
        for name in self.name_renders:
            if name is not None:
                name[0].render()
                name[1].render()

    def render_used_deck(self):
        for card in self.used_deck_render:
            if card.card_type == "wild":
                self.display.blit(pygame.transform.rotate(wild_image_color_map[card.wild_color], card.rotation), (WIDTH // 2 - card.rect.width // 2, HEIGHT // 2 - card.rect.height // 2))
            elif card.card_type == "wild draw":
                self.display.blit(pygame.transform.rotate(wild_draw_image_color_map[card.wild_color], card.rotation), (WIDTH // 2 - card.rect.width // 2, HEIGHT // 2 - card.rect.height // 2))
            else:
                self.display.blit(pygame.transform.rotate(card_image_map[(card.card_color.title(), str(card.card_type))], card.rotation), (WIDTH // 2 - card.rect.width // 2, HEIGHT // 2 - card.rect.height // 2))
