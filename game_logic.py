from player import Player
from ai import AI
from deck import return_deck
from random import shuffle
from render import *
import time


AI_NAME_LIST = list(reversed(["Bot", "Bot2", "Bot3"]))

update_card_positions_event = pygame.USEREVENT + 1
pygame.time.set_timer(update_card_positions_event, 1)


class Board:
    def __init__(self, game):
        self.game = game
        self.display = pygame.display.get_surface()
        self.playing = True
        self.current_state = "dealing_cards"
        self.all_states = {"dealing_cards": self.deal_cards, "in game": self.game_flow, "game over": self.end_game}
        self.deck = return_deck()
        self.player = Player("Player", [])
        self.bots = [AI(AI_NAME_LIST[_], []) for _ in range(3)]
        self.rotation_list = [self.player] + self.bots
        shuffle(self.rotation_list)
        self.camera_pov_index = get_player_controller_index(self.rotation_list)

        self.state_switched = False
        self.winning_player = None

        self.card_rendering = CardRendering(self)
        self.game_flow = GameFlowState(self)
        self.end_game = EndGame(self)
        self.card_dealer = DealingCardState(self.rotation_list, self.deck, self.card_rendering)

        self.reset = False

        pygame.mixer.music.play()
        pygame.event.wait()

    def play(self):
        self.all_states[self.current_state]()
        if self.current_state != "game over":
            self.update_board_render()

    def deal_cards(self):
        self.card_dealer.deal_cards()
        if self.card_dealer.end_dealing_state:
            self.switch_states("in game")

    def game_flow(self):
        self.game_flow.game_loop()
        if not self.game_flow.playing:
            self.current_state = "game over"
            self.state_switched = True

    def end_game(self):
        self.end_game.game_loop()
        if self.state_switched:
            self.state_switched = False

    def update_board_render(self):
        for i, player in enumerate(self.rotation_list):
            if self.current_state == "in game" and self.game_flow.allow_render_raised_card:
                calculate_card_destination_position(self.rotation_list, i, self.camera_pov_index, True)
            else:
                calculate_card_destination_position(self.rotation_list, i, self.camera_pov_index, False)
            set_card_rotation_for_deck(self.rotation_list, i, self.camera_pov_index)
        for event in self.game.events:
            if event.type == update_card_positions_event:
                update_card_positions(self.game_flow.rotation_list, self.card_rendering.moving_cards_leaving)

        self.card_rendering.render_ai_names()
        self.card_rendering.render_cards()

        if not self.game_flow.iteration_reversed:
            self.display.blit(BOARD_DIRECTION, (0, 50))
        else:
            self.display.blit(BOARD_DIRECTION_REVERSE, (0, 50))

        if self.game_flow.skipped:
            render_skipped(self.game_flow.current_player_index, self.camera_pov_index)

    def switch_states(self, switch):
        self.current_state = switch
        self.state_switched = True


class GameFlowState:
    def __init__(self, board):
        self.board = board
        self.rotation_list = self.board.rotation_list
        self.deck = self.board.deck
        self.card_rendering = self.board.card_rendering
        self.camera_pov_index = self.board.camera_pov_index

        self.current_player_index = 0
        self.current_stack = 0
        self.current_board_color = None
        self.current_board_type = None
        self.playing = True
        self.iterate_rotation = False
        self.iteration_reversed = False
        self.skipped = False
        self.allow_render_raised_card = False
        self.time_delay = None

        self.card_pickup_delay = None

        self.used_deck = []

        self.update_rotation_interface_color("green")

        self.next_round_skip = False

    def game_loop(self):
        self.play_move()
        self.render_used_deck()

        if self.iterate_rotation:  # Player rotation must not iterate until ready (Player made their choice of card, animations being completed, simulating wait time for AI's)
            self.check_win()
            self.update_rotation_interface_color("white")
            self.reset_players_status()
            self.player_rotation()
            self.iterate_rotation = False
            self.update_rotation_interface_color("green")
            if self.next_round_skip:
                self.skipped = True
                self.next_round_skip = False
            else:
                self.skipped = False

    def check_win(self):
        for player in self.rotation_list:
            if len(player.deck) == 0:
                self.board.winning_player = player
                self.playing = False

    def update_rotation_interface_color(self, color, game_start=False):
        if game_start:
            if not hasattr(self.rotation_list[self.current_player_index], "controllable"):
                self.card_rendering.name_renders[self.current_player_index].update_color(color)
            return
        if not hasattr(self.rotation_list[self.current_player_index], "controllable"):
            if self.current_player_index + 1 > 2:  # Account for player having a turn, prevents IndexError
                self.card_rendering.name_renders[self.current_player_index - 1].update_color(color)
            else:
                self.card_rendering.name_renders[self.current_player_index].update_color(color)

    def player_rotation(self):
        if self.iteration_reversed:
            self.current_player_index -= 1
            if self.current_player_index == -1:
                self.current_player_index = len(self.rotation_list) - 1
        else:
            self.current_player_index += 1
            if self.current_player_index > len(self.rotation_list) - 1:
                self.current_player_index = 0

    def play_move(self):
        if self.camera_pov_index == self.current_player_index:
            self.play_player_move(self.board.game.events)
        else:
            self.play_ai_move()

    def player_choosing_color(self):
        current_selected_color_index = 0
        colors_images = {0: Red_0, 1: Green_0, 2: Blue_0, 3: Yellow_0}
        colors_positions = {0: WIDTH // 2 - 400, 1: WIDTH // 2 - 200, 2: (WIDTH // 2 + 200) - CARD_WIDTH, 3: (WIDTH // 2 + 400) - CARD_WIDTH}
        colors = ["red", "green", "blue", "yellow"]
        display = pygame.display.get_surface()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            if current_selected_color_index - 1 < 0:
                                current_selected_color_index = len(colors) - 1
                            else:
                                current_selected_color_index -= 1
                        if event.key == pygame.K_RIGHT:
                            if current_selected_color_index + 1 > len(colors):
                                current_selected_color_index = 0
                            else:
                                current_selected_color_index += 1
                        if event.key == pygame.K_SPACE:
                            return colors[current_selected_color_index]
            display.blit(BACKGROUND_ALT, (0, 0))
            for i, color in enumerate(colors_images):
                if current_selected_color_index == i:
                    display.blit(colors_images[i], (colors_positions[i], HEIGHT // 2 - 300))
                else:
                    display.blit(colors_images[i], (colors_positions[i], HEIGHT // 2 - CARD_HEIGHT // 2))
            pygame.display.update()


    def play_player_move(self, events):
        if self.skipped:
            if self.round_delay_switch():
                self.iterate_rotation = True
            return
        player = self.rotation_list[self.current_player_index]

        if self.current_stack > 0 and player.status != "waiting":
            player.threat_level = 1
            if not player.status == "pickup":
                response = self.check_any_playable_cards(player)
                if not response:
                    player.status = "pickup"
                else:
                    self.allow_render_raised_card = True
                    player.input(self.current_board_color, self.current_board_type)
                    if player.decision is not None:
                        card = player.deck.pop(player.current_hovered_card_index)
                        self.selected_card_logic(card)
                        player.status = "waiting"
                        self.allow_render_raised_card = False
            if player.status != "waiting":
                self.pickup_cards()
                player.sort_cards_visual()
            if self.current_stack == 0:
                player.status = "waiting"
        else:
            response = self.check_any_playable_cards(player)
            if not response and player.status != "waiting":
                player.status = "pickup"
            if player.status == "pickup":
                self.pickup_cards()
                player.sort_cards_visual()
                if self.check_any_playable_cards(player):
                    player.status = None
            elif player.status is None:
                self.allow_render_raised_card = True
                player.input(self.current_board_color, self.current_board_type, events)
                if player.decision is not None:
                    card = player.deck.pop(player.current_hovered_card_index)
                    self.selected_card_logic(card)
                    player.status = "waiting"
                    self.allow_render_raised_card = False
        if player.status == "waiting":
            if self.card_rendering.check_moving_cards_leaving_done():
                if self.round_delay_switch():
                    self.iterate_rotation = True

    def play_ai_move(self):
        if self.skipped:
            if self.round_delay_switch():
                self.iterate_rotation = True
            return
        player_ai = self.rotation_list[self.current_player_index]

        if self.current_stack > 0 and player_ai.status != "waiting":
            player_ai.threat_level = 1
            if not player_ai.status == "pickup":
                response = self.check_any_playable_cards(player_ai)
                if not response:
                    player_ai.status = "pickup"
                else:
                    # If playable draw card or wild draw. Play it, then move to next turn.
                    player_ai.play(self.current_board_color, self.current_board_type)
                    card = player_ai.deck.pop(player_ai.chosen_card_index)
                    self.selected_card_logic(card)
                    player_ai.status = "waiting"
            # Pick up cards until stack is done and then move to next turn.
            if player_ai.status != "waiting":
                self.pickup_cards()
            if self.current_stack == 0:
                player_ai.status = "waiting"
        else:
            response = self.check_any_playable_cards(player_ai)
            if not response and player_ai.status != "waiting":
                player_ai.status = "pickup"
            if player_ai.status == "pickup":
                self.pickup_cards()
                if self.check_any_playable_cards(player_ai):
                    player_ai.status = None
            elif player_ai.status is None:
                player_ai.play(self.current_board_color, self.current_board_type)
                card = player_ai.deck.pop(player_ai.chosen_card_index)
                self.selected_card_logic(card)
                player_ai.status = "waiting"

        if player_ai.status == "waiting":
            if self.card_rendering.check_moving_cards_leaving_done():
                if self.round_delay_switch():
                    self.iterate_rotation = True
        return

    def selected_card_logic(self, card):
        if card.card_color in ("red", "green", "blue", "yellow"):
            self.current_board_color = card.card_color
        elif card.card_color == "black":
            if self.current_player_index != self.camera_pov_index:
                self.current_board_color = card.wild_color
            else:
                card.wild_color = self.player_choosing_color()
                self.current_board_color = card.wild_color
        self.current_board_type = card.card_type
        if card.card_type not in range(0, 9) and card.card_type != "wild":  # <-- Handle special type cards
            self.special_cards(card.card_type)
        self.card_rendering.card_leaving_deck_animation(card)

    def special_cards(self, special_type):
        if special_type == "wild draw":
            self.current_stack += 4
        elif special_type == "draw":
            self.current_stack += 2
        elif special_type == "skip":
            self.next_round_skip = True
        elif special_type == "reverse":
          self.iteration_reversed = True

    def check_any_playable_cards(self, player):
        if self.current_board_color is None:
            return True
        if self.current_stack:
            for card in player.deck:
                if card.card_type == "wild draw" or card.card_type == "draw":
                    return True
            else:
                return False
        else:
            for card in player.deck:
                if card.card_color == self.current_board_color or card.card_type in (self.current_board_type, "wild", "wild draw"):
                    return True
            else:
                return False

    def round_delay_switch(self):
        if self.time_delay is None:
            self.time_delay = time.time()
        if time.time() - self.time_delay >= 1.5:
            self.time_delay = None
            return True

    def render_used_deck(self):
        if self.used_deck:
            self.card_rendering.render_used_deck(self.used_deck)

    def pickup_cards(self):
        """
            - Check if stack threat
            - If stack threat:
                - Card_Renderer.play_add_card_to_deck(current_player, self.deck[-1])
                - Once Card_Render.animation_complete == True
                - Add card to player/ai deck.
                - Card will be rendered normally.
                - Subtract -1 from current_stack
                - Repeat until current_stack = 0
            - No stack threat:
                - Card_renderer.play_add_card_to_deck(current_player, self.deck[-1])
                - Once card_render.animation_complete == True
                - Add card to player/ai deck.
                - Card renders normally.

            Add variable delay to give cards time to travel
        """
        if self.card_pickup_delay is None:
            self.card_pickup_delay = time.time()
        if time.time() - self.card_pickup_delay > 1:
            self.card_pickup_delay = time.time()
            self.deck_rebuild_checker()
            card = self.deck.pop()
            self.rotation_list[self.current_player_index].deck.append(card)
            self.card_rendering.card_pickup_animation(card, self.current_player_index)
            if self.current_stack > 0:
                self.current_stack -= 1
            return card # Card will be returned if needed in case it's needed to checks.

    def deck_rebuild_checker(self):
        if len(self.deck) - 1 < 0:
            self.rebuild_deck()

    def rebuild_deck(self):
        self.deck = self.used_deck[:-1]
        shuffle(self.deck)

    def reset_players_status(self):
        self.rotation_list[self.current_player_index].status = None
        self.rotation_list[self.current_player_index].decision = None
        self.rotation_list[self.current_player_index].threat_level = 0


class DealingCardState:
    def __init__(self, rotation_list, deck, card_rendering):
        self.deck = deck
        self.rotation_list = rotation_list
        self.current_index = 0
        self.timer = None
        self.dealing_done = False
        self.added_cards = 0
        self.card_rendering = card_rendering
        self.camera_pov_index = get_player_controller_index(self.rotation_list)
        self.distributing_done = False
        self.end_dealing_state = False

    def deal_cards(self):
        if len(self.rotation_list[-1].deck) == 7:
            self.distributing_done = True
        if self.card_rendering.check_moving_cards_done() and self.distributing_done:
            #self.rotation_list[0].deck = self.rotation_list[0].deck[:2]
            # self.rotation_list[0].deck[0].card_color, self.rotation_list[0].deck[0].card_type = "black", "wild draw"
            # self.rotation_list[0].deck[0].image = card_image_map[(self.rotation_list[0].deck[0].card_color.title(), str(self.rotation_list[0].deck[0].card_type))]
            self.end_dealing_state = True
        if self.timer is None:
            self.timer = time.time()
            self.distribute()
        elif time.time() - self.timer > .075 and self.card_rendering.check_moving_cards_done():  # Distribute cards if timer is ready and every player does not have 7 cards already.
            self.timer = time.time()
            self.distribute()

    def distribute(self):
        card = self.deck.pop()
        self.card_rendering.card_pickup_animation(card, self.current_index)
        self.rotation_list[self.current_index].deck.append(card)
        if self.current_index == self.camera_pov_index:
            self.rotation_list[self.camera_pov_index].sort_cards_visual()
        if self.current_index + 1 > 3:
            self.current_index = 0
        else:
            self.current_index += 1


class EndGame:
    def __init__(self, board):
        self.board = board
        self.display = self.board.display

    def game_loop(self):
        if self.board.state_switched:
            self.winner_text = RenderText(f"{self.board.winning_player.name} won the game", (WIDTH // 2, 400), font_size=80)
            self.play_again_text = RenderText("Play again?", (self.winner_text.text_rect.x + self.winner_text.text_rect.width - 100, 500))
            self.quit_text = RenderText("Quit", (self.winner_text.text_rect.x + 75, 500))
        self.display.fill("black")
        self.render_texts()
        self.input()

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in self.board.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_text.text_rect.collidepoint(mouse_pos):
                    pygame.display.quit()
                if self.play_again_text.text_rect.collidepoint(mouse_pos):
                    self.board.reset = True

    def render_texts(self):
        self.winner_text.render()
        self.play_again_text.render()
        self.quit_text.render()


def get_player_controller_index(rotation_list):
    for i, bot in enumerate(rotation_list):
        if hasattr(bot, "controllable"):
            return i


"""
Implement:
Jump in: If someone plays a card and you have the exact same card. You can place that card down. (Rotation resumes normally)
Memory: Bots will stay in a state even if requirements are not met. They can switch states if needed though.
Prevent Win: Bots will try to prevent a player from winning. If someone on the board has only 2 cards. The chances
of the AI playing draw cards skyrocket unless they have a priority that's more important. (Like determining they will win first so saving their draw cards is useful instead).
The chances of using cards like skip and reverse if the player that's about to win is after them also raise as well.
"""
