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
class AI:
    def __init__(self, name, deck):
        self.name = name 
        self.deck = deck
        self.hatred = None
        self.prevent_win = None  # <--- Player name
        self.threat_level = 0
        self.no_draw_cards = False 
        self.skip = False 
        self.reverse = False
        self.previous_deck_length = len(self.deck)
        self.future_move = None 
    
    def play(self, current_board_color, current_board_number):
        if (self.threat_level or self.prevent_win is not None) and not self.no_draw_cards:
            # To prevent function from running without need. Only check when no_draw_cards is set to False. If no_draw_cards is set to true. Have a function that checks if the length of our card deck was greater than our last turns. If that is true then set no_draw_cards to False.
            # Prevent win should possibly contain the player name. With that the bot can determine hatred for that player. If hatred is above certain threshold the threat_level will be 2. (Prioritize wild draw) or threat_level 1 (Prioritize draw)
            # Depending on hate for the player the bot will try more cards in order to prevent them from winning. (If draw_card_case yields None. Go to reverse priority next, or skip priority)
            # If hatred is high enough. The bot will actively try to guess the flaws of the hated players deck (If the player is playing a lot of blue's the bot can try to change the color to something else.)
            if self.threat_level:  # If being threatened by a card stack
                card = draw_card_case(self.deck, current_board_color, self.threat_level)
            elif self.prevent_win: # If preventing a player win (Different threat levels)
                if self.hatred[self.prevent_win] >= 5:
                    card = draw_card_case(self.deck, current_board_color, 2)
                else:
                    card = draw_card_case(self.deck, current_board_color, 1)
            if card is None and self.threat_level:
                return "pickup"
            else:
                self.no_draw_cards = True 
                card = no_priority(self.deck, current_board_color, current_board_number)
        elif self.reverse:
            card = reverse_priority(self.deck, current_board_color, current_board_number)
        elif self.skip:
            card = skip_priority(self.deck, current_board_color, current_board_number)
        else:
            card = no_priority(self.deck, current_board_color, current_board_number)
        if card is None:  # If card is None then that means no card was available for play.
            return "pickup"
        print(f"{self.name} played {(card[0], card[1])}!")
        card_index = self.deck.index(card)
        self.manage_draw_card_flag()
        return card_index, card 
    
    def manage_draw_card_flag(self):
        response = check_if_new_cards_added(self.deck, self.previous_deck_length) # Check if new cards have been added. If true reset flags
        if response:
            self.no_draw_cards = False 
        self.previous_deck_length = len(self.deck)
    
    def set_hatred(self, player_list):
        for player in player_list:
            if player.name != self.name:
                self.hatred[player.name] = 0
    
    def target_player(self, game_color, target_player, player_rotation, current_player_index):
        hatred = self.hatred[target_player]
        before_or_after = self.is_target_before_or_after(target_player, player_rotation, current_player_index)
        draw_cards_available = self.check_if_draw_cards_available()
        if hatred > 8: # High level hatred move 
            if before_or_after == "before" and draw_cards_available:  # If player is before me and I have a draw card should I should reverse so I can stack cards on them.
                reverse_card_available = self.check_if_draw_cards_available(game_color)
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

    def __repr__(self):
        return self.name
    

def check_if_new_cards_added(deck, previous_deck_length):
    if len(deck) > previous_deck_length:
        return True
    else:
        return False 

def no_priority(deck, game_color, game_number):
    """
    Filter out cards that are not same color or number as current board color/number.
    Special cards rated lowest (e.g. draw, reverse, skip)
    Regular colored cards (0-9) rated highest. 
    Play highest rated card (If multiple have same rating, pick any card out of the group of highest)
    If no available card launch color change."""
    card_ratings = []
    color_stats = count_colored_amount(deck)
    for card in deck:
        # Special card ratings (Draw, Skip, Reverse)
        if (card[0] == game_color or game_color is None) and card[1] not in range(0, 10):
            card_ratings.append((card, 5))
        # Regular card ratings
        elif (card[0] == game_color or game_color is None) and card[1] in range(0, 10):
            card_ratings.append((card, 10))
        # Cards with same number as game
        elif card[1] == game_number:
            card_ratings.append((card, 7))
        # Wild card ratings
        elif card[1] == "wild":
            card_ratings.append((card, 3))
        # Wild draw ratings
        elif card[1] == "wild draw":
            card_ratings.append((card, 1))
    if card_ratings:
        card = sort_highest_rated(card_ratings)
        if card[0] == "black":
            new_color = color_change(color_stats, game_color)
            card[2] = new_color           
        return card
    else:
        return None
    

def draw_card_case(deck, game_color, threat_level):
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
    color_stats = count_colored_amount(deck)
    if threat_level == 1:
        for card in deck:
            if card[0] == game_color and card[1] == "draw":
                card_ratings.append((card, 10))
            elif card[0] == "black" and card[1] == "wild draw":
                card_ratings.append((card, 5))
    elif threat_level == 2:
        for card in deck:
            if card[0] == game_color and card[1] == "draw":
                card_ratings.append((card, 5))
            elif card[0] == "black" and card[1] == "wild draw":
                card_ratings.append((card, 10))
    if card_ratings:
        card = sort_highest_rated(card_ratings)
        if card[0] == "black":
            new_color = color_change(color_stats, game_color)
            card[2] = new_color
        return card
    else:
        return None 


def reverse_priority(deck, game_color, game_number):
    """
    If reverse cards are in deck and have same color as game board. The card is automatically played.
    If no card available, launch base case. Same memory system used in draw_card_case
    """
    for card in deck:
        if card[0] == game_color and card[1] == "reverse":
            return card 
    else:
        return no_priority(deck, game_color, game_number)
    
    
def skip_priority(deck, game_color, game_number):
    """
    If skip cards are in deck and have same color as game board. The card is auttomatically played. If no card available launch base case. Same memory system used in draw_card_case
    """
    for card in deck:
        if card[0] == game_color and card[1] == "skip":
            return card
    else:
        return no_priority(deck, game_color, game_number)


def pick_up_card(game_deck):
    return game_deck.pop()


def color_change(deck_color_stats, current_color):
    lowest_number_color = deck_color_stats[2]  # Might be used in future
    highest_number_color = deck_color_stats[1]
    amount_each_color = deck_color_stats[0]  # Might be used in future
    if highest_number_color == current_color:  # This will be used in case the draw 4 is used to target another player. But AI still wants same color. OR AI is using draw to prevent taking a stack.
        new_color = current_color
        return new_color 
    else:
        new_color = highest_number_color
        return new_color


def give_wild_color(card, color):
    card[2] = color
    return card


def sort_highest_rated(card_ratings):
    sorted_cards = sorted(card_ratings, key=lambda tup: tup[1], reverse=True)
    return sorted_cards[0][0]
    

def count_colored_amount(card_deck):
    color_amounts = {"red": 0, "green": 0, "blue": 0, "yellow": 0, "black": 0}
    for card in card_deck:
        color_amounts[card[0]] += 1 
    highest_color_amount = max(color_amounts, key=color_amounts.get)
    lowest_color_amount = min(color_amounts, key=color_amounts.get)
    return color_amounts, highest_color_amount, lowest_color_amount 
