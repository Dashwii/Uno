from player import *
from ai import AI, AI_NAMES
from deck import return_deck
from random import shuffle
from render import *
import time

update_card_positions_event = pygame.USEREVENT + 1
pygame.time.set_timer(update_card_positions_event, 1)

shuffle(AI_NAMES)


class Board:
    def __init__(self, game):
        self.game = game
        self.display = pygame.display.get_surface()
        self.playing = True
        self.current_state = "dealing_cards"
        self.all_states = {"dealing_cards": self.deal_cards_state, "in game": self.game_flow_state, "game over": self.end_game_state}
        self.deck = return_deck()
        self.player = Player("Player")
        self.bots = [AI(AI_NAMES.pop(_ - 2), [], self) for _ in range(3)]
        self.rotation_list = [self.player] + self.bots
        self.AI_prevent_win = False  # Debugging code
        shuffle(self.rotation_list)
        for i, player in enumerate(self.rotation_list):
            player.index = i
        self.camera_pov_index = get_camera_pov_index(self.rotation_list)

        self.state_switched = False
        self.winning_player = None

        self.board_rendering = BoardRendering(self)
        self.game_flow = GameFlowState(self)
        self.end_game = EndGame(self)
        self.card_dealer = DealingCardState(self, self.board_rendering)

        self.new_round = False

        pygame.mixer.music.play(-1)
        pygame.event.wait()

    def play(self):
        self.all_states[self.current_state]()
        if self.current_state != "game over":
            self.update_board_render()

    def deal_cards_state(self):
        self.card_dealer.deal_cards()
        if self.card_dealer.end_dealing_state and self.board_rendering.check_moving_cards_done():
            self.switch_states("in game")

    def game_flow_state(self):
        self.game_flow.game_loop()
        if not self.game_flow.playing:
            self.current_state = "game over"
            self.state_switched = True

    def end_game_state(self):
        self.end_game.game_loop()
        if self.state_switched:
            self.state_switched = False
        if self.new_round:
            self.reset_to_new_round()

    def reset_to_new_round(self):
        for player in self.rotation_list:
            player.deck = []
        if self.rotation_list[self.winning_player].score >= 500:
            for player in self.rotation_list:
                player.score = 0
        self.deck = return_deck()
        self.game_flow = GameFlowState(self)
        self.card_dealer = DealingCardState(self, self.board_rendering)
        self.board_rendering.used_deck_render = []
        self.current_state = "dealing_cards"
        self.new_round = False
        self.winning_player = None

    def update_board_render(self):
        for i, player in enumerate(self.rotation_list):
            if self.current_state == "in game" and self.game_flow.allow_render_raised_card:
                calculate_card_destination_position(self.rotation_list, i, self.camera_pov_index, True)
            else:
                calculate_card_destination_position(self.rotation_list, i, self.camera_pov_index, False)

        for event in self.game.events:
            if event.type == update_card_positions_event:
                update_card_positions(self.game_flow.rotation_list, self.board_rendering.moving_cards_leaving)

        if not self.game_flow.iteration_reversed:
            self.display.blit(asset_map["Board Direction"], (0, 50 * SCALING_RATIO))
        else:
            self.display.blit(asset_map["Board Direction Reversed"], (0, 50 * SCALING_RATIO))

        if self.game_flow.skipped:
            render_skipped(self.game_flow.current_player_index, self.camera_pov_index)

        if self.game_flow.current_stack > 0:
            self.game_flow.current_stack_text.render()
            self.display.blit(STACK_PORTAL, (WIDTH // 2 - STACK_PORTAL.get_width() // 2, HEIGHT // 2 - STACK_PORTAL.get_height() // 2))

        self.board_rendering.render_ai_names()
        self.board_rendering.render_cards()

    def switch_states(self, switch):
        self.current_state = switch
        self.state_switched = True


class GameFlowState:
    def __init__(self, board):
        self.board = board
        self.rotation_list = self.board.rotation_list
        self.board_rendering = self.board.board_rendering

        self.camera_pov_index = self.board.camera_pov_index

        self.current_player_index = 0
        self.last_player_index = 0
        self.board_rendering.update_rotation_interface_color(self.current_player_index, None)
        self.current_stack = 0
        self.current_stack_text = DrawText(self.current_stack, (WIDTH // 2 + (150 * SCALING_RATIO), HEIGHT // 2 - (200 * SCALING_RATIO)), font_size=60, color="purple")
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

        self.next_round_skip = False

    def game_loop(self):
        self.play_move()
        self.iteration()

    def iteration(self):
        # This will not iterate until iteration_rotation is true. It'll be true when the current player is done with their turn and cards moving on the board are in place.
        if self.iterate_rotation:
            self.check_win()
            self.reset_players_status()
            self.last_player_index = self.current_player_index
            self.player_rotation()
            self.board_rendering.update_rotation_interface_color(self.current_player_index, self.last_player_index)
            self.iterate_rotation = False
            if self.current_player_index == self.camera_pov_index:
                self.rotation_list[self.current_player_index].auto_highlight(self.current_board_color, self.current_board_type, self.current_stack)
            if self.next_round_skip:
                self.skipped = True
                self.next_round_skip = False
            else:
                self.skipped = False

    def check_win(self):
        if len(self.rotation_list[self.current_player_index].deck) == 0:
            self.board.winning_player = self.current_player_index
            self.playing = False

    def update_rotation_interface_color(self, color, game_start=False):
        if game_start:
            if not hasattr(self.rotation_list[self.current_player_index], "camera_pov"):
                self.board_rendering.name_renders[self.current_player_index].update_color(color)
            return
        if not hasattr(self.rotation_list[self.current_player_index], "camera_pov"):
            if self.current_player_index + 1 > 2:  # Account for player having a turn, prevents IndexError
                self.board_rendering.name_renders[self.current_player_index - 1].update_color(color)
            else:
                self.board_rendering.name_renders[self.current_player_index].update_color(color)

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
            self.play_player_move()
        else:
            self.play_ai_move()

    def player_choosing_color(self):
        current_selected_color_index = 0
        colors_images = {0: Red_0, 1: Green_0, 2: Blue_0, 3: Yellow_0}
        colors_positions = {0: WIDTH // 2 - (400 * SCALING_RATIO), 1: WIDTH // 2 - (200 * SCALING_RATIO), 2: (WIDTH // 2 + (200 * SCALING_RATIO)) - CARD_WIDTH, 3: (WIDTH // 2 + (400 * SCALING_RATIO)) - CARD_WIDTH}
        colors = ["red", "green", "blue", "yellow"]
        display = pygame.display.get_surface()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == update_card_positions_event:
                    update_card_positions(self.rotation_list, self.board_rendering.moving_cards_leaving)
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
            self.board_rendering.render_cards(player_color_choosing_state=True)
            calculate_card_destination_position(self.rotation_list, self.camera_pov_index, self.camera_pov_index, False)
            for i, color in enumerate(colors_images):
                if current_selected_color_index == i:
                    display.blit(colors_images[i], (colors_positions[i], HEIGHT // 2 - (300 * SCALING_RATIO)))
                else:
                    display.blit(colors_images[i], (colors_positions[i], HEIGHT // 2 - CARD_HEIGHT // 2))
            pygame.display.update()

    def play_player_move(self):
        """
        PLAYER STATES:
        1. None (Choosing any card)
        2. NO PLAYABLE CARDS
        3. STACK PICKUP
        4. Making Play/Keep decision
        5. Waiting
        """
        player = self.rotation_list[self.current_player_index]

        # Some initial checks before the player is allowed to give input
        if self.skipped:
            if self.round_delay_switch():
                self.iterate_rotation = True
            return
        # Two checks for either STACK PICKUP or NO PLAYABLE CARDS. If STACK PICKUP, the player has to pickup the amount of cards in the stack, then the turn moves on.
        # If NO PLAYABLE CARDS, the player will continue to pickup cards until they pickup a playable card. They will then be given the choice to either play or keep that card.
        if self.current_stack > 0 and player.status is None:
            player.stack_threat = True
            any_playable_cards = self.check_any_playable_cards(player)
            if not any_playable_cards:
                player.status = "STACK PICKUP"
        elif not self.check_any_playable_cards(player) and player.status is None:
            player.status = "NO PLAYABLE CARDS"

        if player.status is None:
            self.allow_render_raised_card = True

            # Allow input, will do more work if player.decision has a card
            player.input(self.board.game.events, self.current_board_color, self.current_board_type)
            # Future code to allow pressing the unused uno cards to pickup 1 card.
            pickup_request = pickup_card(self.board.game.events)
            if pickup_request:
                self.allow_render_raised_card = False
                card = self.pickup_cards()
                player.last_added_card = card
                if self.check_card_is_playable(card):
                    player.status = "PLAY/KEEP DECISION"
                else:
                    player.status = "WAITING"

            if player.decision is not None:
                player.status = "WAITING"
                card = player.deck.pop(player.current_hovered_card_index)
                self.allow_render_raised_card = False
                self.selected_card_logic(card)

        elif player.status in ("NO PLAYABLE CARDS", "STACK PICKUP"):
            card = self.pickup_cards()
            if card:  # In case a card wasn't added on iteration due to animation delay.
                player.last_added_card = card
            if player.status == "STACK PICKUP" and self.current_stack == 0:
                player.status = "WAITING"
            elif player.status == "NO PLAYABLE CARDS":
                any_playable_cards = self.check_any_playable_cards(player)
                if any_playable_cards:
                    player.status = "PLAY/KEEP DECISION"

        elif player.status == "PLAY/KEEP DECISION":
            decision = update_choice_buttons(self.board.game.events)
            if decision == "PLAY":
                card = player.deck.pop(player.deck.index(player.last_added_card))
                self.selected_card_logic(card)
                player.last_added_card = None
                player.status = "WAITING"
            elif decision == "KEEP":
                player.status = "WAITING"

        elif player.status == "WAITING":
            if self.board_rendering.check_moving_cards_leaving_done():
                if self.round_delay_switch():
                    self.iterate_rotation = True

    def play_ai_move(self):
        player_ai = self.rotation_list[self.current_player_index]
        if self.skipped:
            if self.round_delay_switch():
                self.iterate_rotation = True
            return
        if len(player_ai.deck) == 1 and self.board.AI_prevent_win:
            self.current_stack = 2
            player_ai.status = "STACK PICKUP"
            print("AI WIN PREVENTION")

        if self.current_stack > 0 and player_ai.status is None:
            player_ai.stack_threat = True
            any_playable_cards = self.check_any_playable_cards(player_ai)
            if not any_playable_cards:
                player_ai.status = "STACK PICKUP"
        elif not self.check_any_playable_cards(player_ai) and player_ai.status is None:
            player_ai.status = "NO PLAYABLE CARDS"

        if player_ai.status is None:
            player_ai.play(self.current_board_color, self.current_board_type)
            if player_ai.decision is not None:
                player_ai.status = "WAITING"
                card = player_ai.deck.pop(player_ai.chosen_card_index)
                self.selected_card_logic(card)

        elif player_ai.status in ("NO PLAYABLE CARDS", "STACK PICKUP"):
            card = self.pickup_cards()
            if card:  # In case a card wasn't added on iteration due to animation delay.
                player_ai.last_added_card = card
            if player_ai.status == "STACK PICKUP" and self.current_stack == 0:
                player_ai.status = "WAITING"
            elif player_ai.status == "NO PLAYABLE CARDS":
                any_playable_cards = self.check_any_playable_cards(player_ai)
                if any_playable_cards and self.board_rendering.check_moving_cards_done():
                    player_ai.status = None

        elif player_ai.status == "WAITING":
            if self.board_rendering.check_moving_cards_leaving_done():
                if self.round_delay_switch():
                    self.iterate_rotation = True

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
        self.board_rendering.card_leaving_deck_animation(card)
        if self.current_player_index != self.camera_pov_index:
            self.board_rendering.update_number_of_cards_in_deck_render(self.current_player_index)

    def special_cards(self, special_type):
        if special_type == "wild draw":
            self.current_stack += 4
            self.current_stack_text.update_text(f"+{self.current_stack}")
        elif special_type == "draw":
            self.current_stack += 2
            self.current_stack_text.update_text(f"+{self.current_stack}")
        elif special_type == "skip":
            self.next_round_skip = True
        elif special_type == "reverse":
            self.iteration_reversed = not self.iteration_reversed

    def check_any_playable_cards(self, player):
        if self.current_board_color is None:
            return True
        if self.current_stack:
            if self.current_board_type == "draw":
                for card in player.deck:
                    if card.card_type == "draw":
                        return card  # Should really be true instead of returning the card.
                else:
                    return False
            elif self.current_board_type == "wild draw":
                for card in player.deck:
                    if card.card_type == "wild draw":
                        return card
                else:
                    return False
        else:
            for card in player.deck:
                if card.card_color == self.current_board_color or card.card_type in (self.current_board_type, "wild", "wild draw"):
                    return card  # Should really be true instead of returning the card.
            else:
                return False

    def check_card_is_playable(self, card):
        if self.current_board_color is None:
            return True
        if self.current_stack:
            if card.card_type == "wild draw" or card.card_type == "draw":
                return True
            else:
                return False
        else:
            if card.card_color == self.current_board_color or card.card_type in (self.current_board_type, "wild", "wild draw"):
                return True
            else:
                return False

    def round_delay_switch(self):
        round_switch_delay = .75
        if self.time_delay is None:
            self.time_delay = time.time()
        if time.time() - self.time_delay >= round_switch_delay:
            self.time_delay = None
            return True

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
            self.card_pickup_delay = time.time() - 1000
        if time.time() - self.card_pickup_delay > .5:
            self.card_pickup_delay = time.time()
            self.deck_rebuild_checker()
            card = self.board.deck.pop()
            set_card_rotation_for_player(card, self.current_player_index, self.camera_pov_index)
            self.rotation_list[self.current_player_index].deck.append(card)
            self.board_rendering.card_pickup_animation(card, self.current_player_index)
            if self.current_player_index == self.camera_pov_index:
                self.rotation_list[self.current_player_index].sort_cards_visual()
            else:
                self.board_rendering.update_number_of_cards_in_deck_render(self.current_player_index)
            if self.current_stack > 0:
                self.current_stack -= 1
                if self.current_stack == 0:
                    self.current_stack_text.update_text("+0")
            return card # Card will be returned if needed in case it's needed for checks.

    def deck_rebuild_checker(self):
        if len(self.board.deck) - 1 < 0:
            self.rebuild_deck()

    def rebuild_deck(self):
        self.board.deck = self.used_deck[:-1]
        self.used_deck = [self.used_deck[-1]]
        shuffle(self.board.deck)

    def reset_players_status(self):
        self.rotation_list[self.current_player_index].status = None
        self.rotation_list[self.current_player_index].decision = None
        self.rotation_list[self.current_player_index].stack_threat = False


class DealingCardState:
    def __init__(self, board, board_rendering):
        self.board = board
        self.current_index = 0
        self.timer = None
        self.dealing_done = False
        self.added_cards = 0
        self.board_rendering = board_rendering
        self.camera_pov_index = get_camera_pov_index(self.board.rotation_list)
        self.distributing_done = False
        self.end_dealing_state = False
        self.time_began = time.time()

    def deal_cards(self):
        if len(self.board.rotation_list[-1].deck) == 7:
            self.distributing_done = True
        if self.board_rendering.check_moving_cards_done() and self.distributing_done:
            self.end_dealing_state = True
            return
        if self.timer is None:
            self.timer = time.time()
            self.distribute()
        elif time.time() - self.timer > .075 and not self.distributing_done:  # Distribute cards if timer is ready and every player does not have 7 cards already.
            self.timer = time.time()
            self.distribute()

    def distribute(self):
        card = self.board.deck.pop()
        set_card_rotation_for_player(card, self.current_index, self.camera_pov_index)
        self.board_rendering.card_pickup_animation(card, self.current_index)
        self.board.rotation_list[self.current_index].deck.append(card)
        if self.current_index != self.camera_pov_index:
            self.board_rendering.update_number_of_cards_in_deck_render(self.current_index)
        if self.current_index == self.camera_pov_index:
            self.board.rotation_list[self.camera_pov_index].sort_cards_visual()
        if self.current_index + 1 > 3:
            self.current_index = 0
        else:
            self.current_index += 1


class EndGame:
    def __init__(self, board):
        self.board = board
        self.display = self.board.display
        self.rotation_list = self.board.rotation_list
        self.score_board = ScoreBoard(self.board)

    def game_loop(self):
        if self.board.state_switched:
            self.score_board.add_score()
            self.score_board.update_text(self.board.winning_player)
        self.score_board.draw_board()
        self.input()

    def input(self):
        for event in self.board.game.events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.board.new_round = True


class ScoreBoard:
    def __init__(self, board):
        self.display = pygame.display.get_surface()
        self.board = board
        self.rotation_list = self.board.rotation_list
        self.player_score_list = [[player, DrawText(player.name, [600 * SCALING_RATIO, 0]), DrawText(player.score, [0, 0])] for player in self.rotation_list]
        self.score_board_rect = pygame.Rect((0, 0), (1000 * SCALING_RATIO, 500 * SCALING_RATIO))
        self.score_board_rect.x, self.score_board_rect.y = (WIDTH // 2 - self.score_board_rect.width // 2), (HEIGHT // 2 - self.score_board_rect.height // 2)
        self.winning_player_text = DrawText("", [0, self.score_board_rect.y + (15 * SCALING_RATIO)])

    def update_text(self, winning_player_index):
        self.player_score_list.sort(key=lambda x: x[0].score, reverse=True)
        for index, player in enumerate(self.player_score_list):
            self.player_score_list[index][1].position[1] = self.score_board_rect.y + ((100 + (index * 100)) * SCALING_RATIO)  # Name Positioning
            # Score positioning
            self.player_score_list[index][2].position[0] = self.score_board_rect.x + (self.score_board_rect.width - (200 * SCALING_RATIO))
            self.player_score_list[index][2].position[1] = self.score_board_rect.y + ((100 + (index * 100)) * SCALING_RATIO)
        if self.board.rotation_list[self.board.winning_player].score >= 500:
            self.winning_player_text.update_text(f"{self.player_score_list[0][0].name} won the game!")
        else:
            self.winning_player_text.update_text(f"{self.rotation_list[winning_player_index].name} won the round! Goal: 500 points.")
        self.winning_player_text.position[0] = (self.score_board_rect.x + self.score_board_rect.width // 2) - self.winning_player_text.text_surface.get_width() // 2

    def add_score(self):
        sorted_players = sorted(self.player_score_list, key=lambda x: len(x[0].deck))
        winning_player = sorted_players[0]
        for index, player in enumerate(sorted_players[1:]):
            for card in player[0].deck:
                if card.card_type in ("wild", "wild draw"):
                    winning_player[0].score += 50
                elif card.card_type in ("reverse", "skip", "draw"):
                    winning_player[0].score += 25
                else:
                    winning_player[0].score += card.card_type  # Add scores for card_types between 0-9
        winning_player[2].update_text(winning_player[0].score)

    def draw_board(self):
        pygame.draw.rect(self.display, "black", self.score_board_rect)
        self.winning_player_text.render()
        for player in self.player_score_list:
            player[1].render()
            player[2].render()


def get_camera_pov_index(rotation_list):
    for i, player in enumerate(rotation_list):
        if hasattr(player, "camera_pov"):
            return i