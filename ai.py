"""
Determine what card is best to play during turn 
Determine hatred for other players (Use Wild 4's and Draw 2's on hated player. Change color to give hated player a disadvantage)
Determine if any wild cards or special cards are on hand
Determine if the AI hates the player more than it wants to win
Maybe give certain random traits? (Wants to win, vengeful, etc)
AI should also determine what is the best move to stop a player from winning:
    Guessing another Bots deck (Memory of previous moves)
    Automatically using a draw 2 on a player with only 1 card

Example:
Bot 1 has 2 yellow cards and 1 red draw 2 card
It would be best for Bot 1 to use his yellow cards however Bot 1 really hates Bot 2
Should Bot 1 target Bot 2 instead of using their yellow cards?


Plan:
-- Point system --
Create point system for every card in AI's deck 
Cards that are usable have higher points than rest of deck

Cases:
If player after bot is about to win:
    Wild draw 4 cards are rated highest
    Draw 2 Cards are rated second highest
    Wild change color cards rated 3rd highest (Potential to change board color to something the winning Player may not have)
If ANY enemy player is about to win:
    Wild draw 4 cards are rated highest (Potential to stack and force extra cards on winning player)
    Draw 2 cards are rated highest (Potential to stack and force extra cards on winning player)
    
-- Guessing Other Decks --
AI will track what cards other players played.
If they have a streak of cards of a certain color. The AI will guess that the majority of their deck is full of that colored cards.
AI will determine that using a Wild 4 would be a good decision (Wild 4's rated highest on next move if general case) to give winning player a disadvantage
If the same color is advantageous for the AI. Determine who is closer to winning. If AI is closer to winning. Do not change color. If enemy is closer to winning. Change color.
"""

# AI functions should be split into two. Class AI, responsible for returning cards and determining best card.
# Class AI advanced decisions, a helper class that will give function for specific sceneraios the AI should switch state to.
# E.g. trying to reverse the board. Waiting for a chance to stack against a player.

AI_NAMES = [
    "Bot 1",
    "Bot 2",
    "Bot 3",
]


class AI:
    def __init__(self, name, deck, board):
        self.board = board
        self.name = name 
        self.deck = deck
        self.hatred = None  # < -- Dictionary of hate for players
        self.stack_threat = False
        self.previous_deck_length = len(self.deck)

        self.chosen_card_index = None
        self.decision = None
        self.last_added_card = None

        self.status = None

        self.index = False
        self.ai_functs = AIFuncts(self)
        self.score = 0

    def play(self, current_board_color, current_board_type):
        """
            The status is a new flag check to determine whether an AI has already chosen a card.
            Will allow for delaying in iterating turns without the AI freaking out.
        """
        self.get_playable_card(current_board_color, current_board_type)

    def get_playable_card(self, current_board_color, current_board_type):
        self.ai_functs.update_state(current_board_color, current_board_type)
        self.decision = self.ai_functs.decision_path()
        self.chosen_card_index = self.deck.index(self.decision)

    # This function is used for the specific states in order to not waste time.
    # If the AI is hoping for a specific type of card but there aren't any new cards in it's deck it won't waste time to check.
    def manage_draw_card_flag(self):  # Wtf is this?
        response = check_if_new_cards_added(self.deck, self.previous_deck_length)  # Check if new cards have been added. If true reset flags
        if response:
            self.no_draw_cards = False 
        self.previous_deck_length = len(self.deck)
    
    def set_hatred(self, player_list):
        for player in player_list:
            if player.name != self.name:
                self.hatred[player.name] = 0

    def check_any_playable_cards(self, current_board_color, current_board_type):
        if current_board_color is None:
            return True
        if self.stack_threat:
            for card in self.deck:
                if card.card_type == "wild draw" or card.card_type == "draw":
                    return True
            else:
                return False
        else:
            for card in self.deck:
                if card.card_color == current_board_color or card.card_type in (current_board_type, "wild", "wild draw"):
                    return True
            else:
                return False


    def __repr__(self):
        return self.name


class AIFuncts:
    """
    Class for offloading some functionality off the main AI class.
    """

    def __init__(self, ai):
        self.ai = ai
        self.board = self.ai.board
        self.deck = self.ai.deck
        self.stack_threat = self.ai.stack_threat
        self.hatred = None
        self.prevent_win = False
        self.no_draw_cards = False
        self.skip = False
        self.reverse = False
        self.future_move = None
        self.previous_deck_length = len(self.deck)

        self.game_card_color = None
        self.game_card_type = None

    def update_state(self, game_card_color, game_card_type):
        self.game_card_color = game_card_color
        self.game_card_type = game_card_type
        self.deck = self.ai.deck
        self.stack_threat = self.ai.stack_threat

        # Prevent win
        if self.ai.index + 1 > len(self.board.rotation_list) - 1:
            player_after = 0
        else:
            player_after = self.ai.index + 1
        if self.ai.index - 1 < 0:
            player_before = len(self.board.rotation_list) - 1
        else:
            player_before = self.ai.index - 1

        if len(self.board.rotation_list[player_after].deck) < 3 and not self.board.game_flow.iteration_reversed:
            self.prevent_win = True
        elif len(self.board.rotation_list[player_before].deck) < 3 and self.board.game_flow.iteration_reversed:
            self.prevent_win = True
        else:
            self.prevent_win = False

        if len(self.board.rotation_list[player_after].deck) < 5 and not self.board.game_flow.iteration_reversed:
            self.skip = True
        elif len(self.board.rotation_list[player_before].deck) < 5 and self.board.game_flow.iteration_reversed:
            self.skip = True
        else:
            self.skip = False

        if len(self.board.rotation_list[player_after].deck) < 5 and not self.board.game_flow.iteration_reversed:
            self.reverse = True
        elif len(self.board.rotation_list[player_before].deck) < 5 and self.board.game_flow.iteration_reversed:
            self.reverse = True
        else:
            self.reverse = False

    def decision_path(self):
        """
        Main decision path for AIFuncts. This method will decide which method should be used for retrieving the best card for the current move and states of the AI.
        """
        if self.stack_threat or self.prevent_win:
            chosen_card = self.draw_card_case()
        elif self.reverse:
            chosen_card = self.reverse_priority()
        elif self.skip:
            chosen_card = self.skip_priority()
        else:
            chosen_card = self.no_priority()
        return chosen_card

    def no_priority(self):
        """
        Filter out cards that are not same color or number as current board color/number.
        Special cards rated lowest (e.g. draw, reverse, skip)
        Regular colored cards (0-9) rated highest.
        Play highest rated card (If multiple have same rating, pick any card out of the group of highest)
        If no available card launch color change.
        """
        card_ratings = []
        for card in self.deck:
            # Special card ratings (Draw, Skip, Reverse)  # -1 Used to be "None" I changed it for some reason
            if (card.card_color == self.game_card_color or self.game_card_color is None) and card.card_type not in range(0, 10):
                card_ratings.append((card, 5))
            # Regular card ratings
            elif (card.card_color == self.game_card_color or self.game_card_color is None) and card.card_type in range(0, 10):
                card_ratings.append((card, 10))
            # Cards with same number as game
            elif card.card_type == self.game_card_type:
                card_ratings.append((card, 7))
            # Wild card ratings
            elif card.card_type == "wild":
                card_ratings.append((card, 3))
            # Wild draw ratings
            elif card.card_type == "wild draw":
                card_ratings.append((card, 1))
        card = sort_highest_rated(card_ratings)
        if card.card_color == "black":
            highest_color_amount = get_highest_color_amount(self.deck)
            new_color = color_change(highest_color_amount, self.game_card_color)
            card.wild_color = new_color
        return card

    def draw_card_case(self):
        """
        Depending on thereat level, cards will be rated differently.
        If threat level is 1:
            If regular draw cards are available. (Same color as board). Regular draw cards rated highest.
            Wild draw rated lower.
        If threat level is 2:
            Wild draws rated highest, regular draw cards rated lower.
            If no draw cards availble. Target flag set to false.
            Remember_target variable set to true.
            Targeting set to false will prevent waste of resources.
            If a card is picked up and it's a draw card OR the game board color has changed and a draw card is now available.
            Remember_target will be set to false and targeting set to true.
            Launch base case if no card available."""
        card_ratings = []
        color_stats = get_highest_color_amount(self.deck)
        if self.ai.stack_threat:
            if self.game_card_type == "draw":
                for card in self.deck:
                    if card.card_type == "draw" and card.card_color == get_highest_color_amount(self.deck):
                        card_ratings.append((card, 10))
                    elif card.card_type == "draw":
                        card_ratings.append((card, 5))
            elif self.game_card_type == "wild draw":
                for card in self.deck:
                    if card.card_color == "black" and card.card_type == "wild draw":
                        new_color = color_change(color_stats, self.game_card_color)
                        card.wild_color = new_color
                        return card
        elif self.prevent_win:
            for card in self.deck:
                if card.card_color == self.game_card_color and card.card_type == "draw":
                    card_ratings.append((card, 5))
                elif card.card_color == "black" and card.card_type == "wild draw":
                    card_ratings.append((card, 10))
        if card_ratings:
            card = sort_highest_rated(card_ratings)
            if card.card_color == "black":
                new_color = color_change(color_stats, self.game_card_color)
                card.wild_color = new_color
            return card
        else:
            return self.no_priority() # Will only return no priority if were in a prevent_win state and have no draw cards.

    def reverse_priority(self):
        """
        If reverse cards are in deck and have same color as game board. The card is automatically played.
        If no card available, launch base case. Same memory system used in draw_card_case
        """
        for card in self.deck:
            if card.card_color == self.game_card_color and card.card_type == "reverse":
                return card
        else:
            return self.no_priority()

    def skip_priority(self):
        """
        If skip cards are in deck and have same color as game board. The card is auttomatically played. If no card available launch base case. Same memory system used in draw_card_case
        """
        for card in self.deck:
            if card.card_color == self.game_card_color and card.card_type == "skip":
                return card
        else:
            return self.no_priority()

    @staticmethod
    def sort_highest_ranked(card_ratings):
        sorted_cards = sorted(card_ratings, key=lambda tup: tup[1], reverse=True)
        return sorted_cards[0][0]

    def check_if_new_cards_added(self):
        if len(self.deck) > self.previous_deck_length:
            return True
        else:
            return False

    # AI specific state functions (Targeting player, trying to reverse board, trying to stack against a player)
    def target_player(self, game_board_color, target_player, player_rotation, current_player_index):
        hatred = self.hatred[target_player]
        before_or_after = self.is_target_before_or_after(target_player, player_rotation, current_player_index)
        draw_cards_available = self.check_if_draw_cards_available(game_board_color)
        if hatred > 8:  # High level hatred move
            if before_or_after == "before" and draw_cards_available:  # If player is before me and I have a draw card should I should reverse so I can stack cards on them.
                reverse_card_available = self.check_if_draw_cards_available(game_board_color)
                pass

    def check_if_reverse_cards_available(self, current_color):
        for card_index, card in enumerate(self.deck):
            if card[0] == current_color and card[1] == "reverse":
                return card_index, card
        return None

    def check_if_draw_cards_available(self, current_color):
        for card_index, card in enumerate(self.deck):
            if (card[0] == current_color and card[1] == "draw") or card[1] == "wild draw":
                return card_index, card
        return None

    def is_target_before_or_after(self, target_player, player_rotation, current_player_index):
        if target_player == player_rotation[current_player_index - 1]:
            return "before"
        elif current_player_index == len(player_rotation) - 1:
            if target_player == player_rotation[0]:
                return "after"
        elif target_player == player_rotation[current_player_index + 1]:
            return "after"
        else:
            return None


def check_if_new_cards_added(deck, previous_deck_length):
    if len(deck) > previous_deck_length:
        return True
    else:
        return False


def color_change(highest_number_color, current_color):
    if highest_number_color == current_color:  # This will be used in case the draw 4 is used to target another player. But AI still wants same color. OR AI is using draw to prevent taking a stack.
        new_color = current_color
        return new_color 
    else:
        new_color = highest_number_color
        return new_color


def sort_highest_rated(card_ratings):
    sorted_cards = sorted(card_ratings, key=lambda tup: tup[1], reverse=True)
    return sorted_cards[0][0]


def get_highest_color_amount(card_deck):
    color_amounts = {"red": 0, "green": 0, "blue": 0, "yellow": 0}
    for card in card_deck:
        if card.card_color != "black":
            color_amounts[card.card_color] += 1
    highest_color_amount = max(color_amounts, key=color_amounts.get)
    return highest_color_amount
