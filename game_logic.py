from player import Player
from ai import AI
from cards import return_deck
import random

def game():
    playing = True
    if playing:
        current_board_color = None
        current_board_number = None 
        ai_name_list = ["Bot", "Bot2", "Bot3", "Bot4"]
        ai_name_list = list(reversed(ai_name_list))
        deck = return_deck()
        player = Player("Player", [deck.pop() for _ in range(7)])
        bots = [AI(ai_name_list.pop(), [deck.pop() for _ in range(7)]) for _ in range(4)]
        player_list = [player] + bots
        player_list[0].deck = [["black", "wild draw", None], ("blue", 5)]
        #player_list[1].deck = [["black", "wild", None], ("green", 5)]
        current_player_rotation = 0 
        current_stack = 0
        print(player_list)
        while True:
            print(f"{player_list[current_player_rotation].name} deck: {player_list[current_player_rotation].deck}")
            current_board_color, current_board_number, special_ability = play_move(player_list, current_player_rotation, current_board_color, current_board_number, deck)
            if special_ability != "skip":
                current_player_rotation = player_rotation(player_list, current_player_rotation)
            if special_ability is not None:
                if special_ability == "reverse":
                    reversed(player_list)
                    print("Player rotation has been reversed!")
                elif special_ability == "skip":
                    current_player_rotation = player_rotation(player_list, current_player_rotation, skipped=True)
                    print(f"{player_list[current_player_rotation - 1]} has been skipped!")
                elif special_ability[0] == "draw":
                    current_stack += special_ability[1]
                    print(f"The current stack is {current_stack} cards!")
                elif special_ability[0] == "wild draw":
                    current_stack += special_ability[1]
                    print(f"The current stack is {current_stack} and the board has been changed to {current_board_color}!")
            next_move_input = input("Go to next turn")
            winner = check_win(player_list)
            if winner:
                print(f"{winner} won the game!")
                return
            if not next_move_input:
                print(f"Current board color is {current_board_color}. Current board number is {current_board_number}")      
                continue 

def player_rotation(player_list, current_player_rotation, skipped=False):
    """
    Function will increment current_player_rotation by 1 by default. 
    If skipped is True provided to the function. current_player_rotation will increment by 2 to skip the next player.
    """
    if skipped:
        current_player_rotation += 2
        if current_player_rotation > len(player_list) - 1:
            current_player_rotation = 0
    else:
        current_player_rotation += 1
        if current_player_rotation > len(player_list) - 1:
            current_player_rotation = 0
    return current_player_rotation 

def play_move(player_list, current_player_rotation, current_board_color, current_board_number, game_deck):
    """
    Use current player's play method, whether they're an AI or Player class.
    The response can be either "picked up card" or a card_index and the played card
    If the response is picked up card. A card from the game deck has been popped and appended to the players deck.
    If the response is a card index and played card. The card will be popped from the players deck. The boards current color and number (If it has a number) will be the current cards.
    """
    current_player = player_list[current_player_rotation]
    response = current_player.play(game_deck, current_board_color, current_board_number)
    
    if response == "m": # <-- Testing Code 
        return current_board_color, current_board_number, None 
    if response == "pickup":
        card = game_deck.pop()
        player_list[current_player_rotation].deck.append(card)
        print(f"{player_list[current_player_rotation].name} picked up a card! {card}")
        return current_board_color, current_board_number, None  
    else:
        special_ability = None 
        card_index, played_card = response 
        if played_card[0] in ("red", "blue", "green", "yellow"):
            current_board_color = played_card[0]
        if played_card[1] in range(0, 10):
            current_board_number = played_card[1]
        else:
            special_ability = card_specials(played_card)
            if played_card[0] == "black":
                current_board_color = played_card[2]
                print(f"Board color has been changed to {current_board_color}!")
                played_card[2] = None
            current_board_number = None
        card = current_player.deck.pop(card_index)
        game_deck.append(card)  # <--- After done with card pop it from players deck and add it back to the game deck.
        return current_board_color, current_board_number, special_ability


def card_specials(card):
    if card[1] == "skip":
        return ("skip")
    elif card[1] == "reverse":
        return ("reverse")
    elif card[1] == "draw":
        return ("draw", 2)
    elif card[1] == "wild draw":
        return ("wild draw", 4, card[2])
    else:
        return None 

def check_win(player_list):
    for player in player_list:
        if len(player.deck) == 0:
            return player.name 
    else:
        return False 

if __name__ == "__main__":
    game()
    
    
# Remember when AI and Player takes card it pops it from main game deck.

"""
Implement:
Jump in: If someone plays a card and you have the exact same card. You can place that card down. (Rotation resumes normally)
Adding to the stack (AI's will automatically play a draw card if there is a stack threatening them.)
Remebering to target an enemy player. Even if function requirements are not met.
Targeting players that are about to win.
"""