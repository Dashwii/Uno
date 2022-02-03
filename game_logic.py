from player import Player
from ai import AI
from cards import return_deck
import random

def game():
    playing = True
    if playing:
        current_board_color = None
        current_board_number = None 
        #player_name = input("Enter your name! >")
        ai_name_list = ["Bot2", "Bot3", "Bot", "Bot4"]
        deck = return_deck()
        player = Player("Player", [deck.pop() for _ in range(7)])
        bots = [AI(ai_name_list.pop(random.randint(0, len(ai_name_list) - 1)), [deck.pop() for _ in range(7)]) for _ in range(4)]
        player_list = [player] + bots
        random.shuffle(player_list)
        print(player_list)
        current_player_rotation = 0 
        while True:
            play_move(player_list, current_player_rotation, current_board_color, current_board_number)
            current_player_rotation = player_rotation(player_list, current_player_rotation)  # Will handle soon if last played card as a skip 
            next_move_input = input("Go to next turn")
            if not next_move_input:
                continue 

def player_rotation(player_list, current_player_rotation, skipped=False):  # Move player turns into own function for handling skips and reverses 
    if skipped:
        current_player_rotation += 2
        if current_player_rotation > len(player_list) - 1:
            current_player_rotation = 0
    else:
        current_player_rotation += 1
        if current_player_rotation > len(player_list) - 1:
            current_player_rotation = 0
    return current_player_rotation 

def play_move(player_list, current_player_rotation, current_board_color, current_board_number):
    current_player = player_list[current_player_rotation]
    response = current_player.play(current_board_color, current_board_number)
    if response is not None:
        card_index, played_card = response 
        current_player.deck.pop(card_index)
        current_board_color = played_card[0]
        current_board_number = played_card[1]
    return current_board_color, current_board_number 

if __name__ == "__main__":
    game()
        