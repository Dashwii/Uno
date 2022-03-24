from init_stuff import *
from draw_text import RenderText


"""
Clean up and generalise the functions.
They're convoluted AF right now:

What I need:
    - Function to map render positions for a deck: Check
    - Function to set rotation orientation for deck of cards: Check
    - Function to set spawn location of a card picked up: Check
    - Function to set spawn location of a card leaving: Check
    - Function to calculate a cards final destination position: Check
    - Function to update a cards current position to its destination: Check
    - Function to create renders for ai names: Check
"""


def render_skipped(player_index, camera_pov_index):
    display = pygame.display.get_surface()
    position = camera_pov_mapping(camera_pov_index, player_index)
    if position == -1:
        display.blit(SKIPPED_ICON, (WIDTH // 2 - SKIPPED_ICON.get_width() // 2, 800 - SKIPPED_ICON.get_height() // 2))
    elif position == 0:
        display.blit(SKIPPED_ICON, (100 - SKIPPED_ICON.get_width() // 2, HEIGHT // 2 - SKIPPED_ICON.get_height() // 2))
    elif position == 1:
        display.blit(SKIPPED_ICON, (WIDTH - 100 - SKIPPED_ICON.get_width() // 2, HEIGHT // 2 - SKIPPED_ICON.get_height() // 2))
    elif position == 2:
        display.blit(SKIPPED_ICON, (WIDTH // 2 - SKIPPED_ICON.get_width() // 2, 150 - SKIPPED_ICON.get_height() // 2))


def create_ai_render_names(rotation_list, camera_pov_index):
    name_renders = []
    for i, player in enumerate(rotation_list):
        if i == camera_pov_index:  # Skip of player's camera_pov
            continue
        position = camera_pov_mapping(camera_pov_index, i)
        if position == 0:  # left deck render
            ai_name = RenderText(player.name, (50, 170 // SCALING_RATIO))
            name_renders.append(ai_name)
        elif position == 1:  # right deck render
            ai_name = RenderText(player.name, (WIDTH - 50, 170 // SCALING_RATIO))
            name_renders.append(ai_name)
        elif position == 2:  # opposite deck render
            ai_name = RenderText(player.name, (WIDTH // 2 + (400 // SCALING_RATIO), 30))
            name_renders.append(ai_name)
    return name_renders


def update_card_positions(rotation_list, moving_cards_leaving):
    for player in rotation_list:
        update_card_positions_helper(player.deck)
    update_card_positions_helper(moving_cards_leaving)


def update_card_positions_helper(cards_to_move):
    change_speed = 3
    for card in cards_to_move:
        if card.rect.x > card.destination_x and not (card.destination_x - change_speed) < card.rect.x < (
                card.destination_x + change_speed):  # <--- Huge check is to see if the x value is between the two values. It prevents the card from constantly spazzing out due to in-precise float values.
            card.rect.x -= change_speed
        if card.rect.x < card.destination_x and not (card.destination_x - change_speed) < card.rect.x < (
                card.destination_x + change_speed):  # <-- Why isn't this condition working
            card.rect.x += change_speed
        elif min(card.destination_x - change_speed, card.destination_x + change_speed) < card.rect.x < max(
                card.destination_x - change_speed,
                card.destination_x + change_speed) and card.rect.x != card.destination_x:
            card.rect.x = card.destination_x
        if card.rect.y > card.destination_y and not min(card.destination_y - change_speed,
                                                        card.destination_y + change_speed) < card.rect.y < max(
                card.destination_y - change_speed, card.destination_y + change_speed):
            card.rect.y -= change_speed
        elif card.rect.y < card.destination_y and not min(card.destination_y - change_speed,
                                                          card.destination_y + change_speed) < card.rect.y < max(
                card.destination_y - change_speed, card.destination_y + change_speed):
            card.rect.y += change_speed
        elif card.rect.y != card.destination_y and min(card.destination_y - change_speed,
                                                       card.destination_y + change_speed) < card.rect.y < max(
                card.destination_y - change_speed, card.destination_y + change_speed):
            card.rect.y = card.destination_y


def calculate_card_destination_position(rotation_list, player_index, camera_pov_index, allowed_to_raise_card):
    """
    Will determine where each card should be positioned in their deck.
    The equation is ((screen_mid - card.rect.(width or height) // 2) - pixel_card_overlap * index) + (pixel_card_overlap * (deck_len - 1)) // 2
        - (screen_mid - card.rect.(width or height) // 2) - pixel_card_overlap * index): Screen mid will be either MID_W, or MID_H. Depends on if the deck is on the side.
            We take the screen_mid and subtract it by width|height of the card divided by 2.
            We then subtract the pixel_card_overlap * the cards index. This is to keep the whole deck in the middle of the screen
            and account for the offset of overlapped space.
        - + (pixel_card_overlap * (deck_len - 1)) // 2: We then add pixel_card_overlap * (deck_len - 1) which will prevent a deck of
            only 1 card from having a negative offset. We then divide this by 2 also. Which tbh I don't know what that does, but it keeps it aligned lmao.
    """
    max_ai_card_renders = 20
    player = rotation_list[player_index]
    position = camera_pov_mapping(camera_pov_index, player_index)
    screen_mid_w = WIDTH // 2
    screen_mid_h = HEIGHT // 2
    player_deck_len = len(player.deck)
    if position == -1:  # camera_pov rendering
        overlap = 65 - player_deck_len
        pixel_card_overlap = percentage(overlap, CARD_WIDTH)
        for index, card in enumerate(player.deck):
            if index == player.current_hovered_card_index and allowed_to_raise_card:
                card.destination_x = int((((screen_mid_w - card.rect.width // 2) + pixel_card_overlap * index) - (
                                        pixel_card_overlap * (player_deck_len - 1)) // 2))
                card.destination_y = HEIGHT - (325 // SCALING_RATIO)
            else:
                card.destination_x = int((((screen_mid_w - card.rect.width // 2) + pixel_card_overlap * index) - (
                            pixel_card_overlap * (player_deck_len - 1)) // 2))
                card.destination_y = HEIGHT - (175 // SCALING_RATIO)

    # Ai deck renders
    if player_deck_len > max_ai_card_renders:
        player_deck_len = max_ai_card_renders
    overlap = 35 - player_deck_len
    if position == 0:  # left deck rendering
        pixel_card_overlap = percentage(overlap, CARD_WIDTH)
        for index, card in enumerate(player.deck[:max_ai_card_renders]):
            card.destination_x = -50 // SCALING_RATIO
            card.destination_y = int(((screen_mid_h - card.rect.width // 2) + pixel_card_overlap * index) - (
                        pixel_card_overlap * (player_deck_len - 1)) // 2)
    elif position == 1:  # right deck rendering
        overlap = 35 - player_deck_len
        pixel_card_overlap = percentage(overlap, CARD_WIDTH)
        for index, card in enumerate(player.deck[:max_ai_card_renders]):
            card.destination_x = WIDTH - (150 // SCALING_RATIO)
            card.destination_y = int(((screen_mid_h - card.rect.width // 2) - pixel_card_overlap * index) + (
                        pixel_card_overlap * (player_deck_len - 1)) // 2)
    elif position == 2:  # opposite deck rendering
        pixel_card_overlap = percentage(overlap, CARD_WIDTH)
        for index, card in enumerate(player.deck[:max_ai_card_renders]):
            card.destination_x = int(((screen_mid_w - card.rect.width // 2) - pixel_card_overlap * index) + (
                        pixel_card_overlap * (player_deck_len - 1)) // 2)
            card.destination_y = -50 // SCALING_RATIO


def get_deck_width(player, position):
    player_pixel_overlap = 65
    ai_pixel_overlap = 35

    if position == -1:  # For some reason the pixel overlap doesn't seem to have an effect. Still keeping it because it makes sense though.
        deck_width = CARD_WIDTH * len(player.deck)
        deck_width = deck_width - (percentage(player_pixel_overlap, CARD_WIDTH) - len(player.deck) - 1)
    elif position == 0:
        deck_width = CARD_HEIGHT * len(player.deck)
        deck_width = deck_width - (percentage(ai_pixel_overlap, CARD_HEIGHT) * (len(player.deck) - 1))
    elif position == 1:
        deck_width = CARD_HEIGHT * len(player.deck)
        deck_width = deck_width - (percentage(ai_pixel_overlap, CARD_HEIGHT) * (len(player.deck) - 1))
    else:
        deck_width = CARD_WIDTH * len(player.deck)
        deck_width = deck_width - (percentage(ai_pixel_overlap, CARD_WIDTH) - len(player.deck) - 1)
    return deck_width


def card_pickup_spawn_location(card, player, player_index, camera_pov_index):
    """
    Based on where the position of the deck the card is being added to will determine its spawn location.
    If the position is in (0, 1) it is a sideways deck. So the cards width and height are swapped to make it sideways.
    Position -1 = camera_pov_index
    Position 0 = left deck
    Position 1 = right deck
    Position 2 = opposite deck
    """
    position = camera_pov_mapping(camera_pov_index, player_index)
    player_deck_width = get_deck_width(player, position)

    if position == -1:
        card.rect.x = (WIDTH // 2 + player_deck_width // 2) + 200
        card.rect.y = HEIGHT - (175 / SCALING_RATIO)
    elif position == 0:
        card.rect.x = -50
        card.rect.y = 700
        card.rect.width = 200
        card.rect.height = 150
    elif position == 1:
        card.rect.x = WIDTH - 150
        card.rect.y = 100
        card.rect.width = 200
        card.rect.height = 150
    elif position == 2:
        card.rect.x = 700
        card.rect.y = -50


def card_leaving_deck_spawn_location(card, player_index, camera_pov_index):
    """
        Based on where the position of the deck the card is being added to will determine its spawn location.
        Position -1 = camera_pov_index
        Position 0 = left deck
        Position 1 = right deck
        Position 2 = opposite deck
    """
    position = camera_pov_mapping(camera_pov_index, player_index)
    if position == -1:
        card.rect.x = WIDTH // 2 - card.rect.width // 2
        card.rect.y = 700
    elif position == 0:
        card.rect.x = 150
        card.rect.y = HEIGHT // 2 - card.rect.height // 2
    elif position == 1:
        card.rect.x = WIDTH - 300
        card.rect.y = HEIGHT // 2 - card.rect.height // 2
    elif position == 2:
        card.rect.x = WIDTH // 2 - card.rect.width // 2
        card.rect.y = 150
    card.destination_x = WIDTH // 2
    card.destination_y = HEIGHT // 2


def set_card_rotation_for_deck(rotation_list, player_index, camera_pov_index):
    player = rotation_list[player_index]
    if player_index == camera_pov_index:
        rotation = 0
        set_card_rotation(player.deck, rotation)
        return
    position = camera_pov_mapping(camera_pov_index, player_index)
    if position == 0:
        rotation = 270
        set_card_rotation(player.deck, rotation)
    elif position == 1:
        rotation = 90
        set_card_rotation(player.deck, rotation)
    elif position == 2:
        rotation = 180
        set_card_rotation(player.deck, rotation)


def set_card_rotation(deck, rotation):
    for card in deck:
        card.rotation = rotation


def camera_pov_mapping(camera_pov_index, player_index):
    """
        Determine positions on the screen for each opposing player based off the camera_pov_index.
        camera_pov_index is the index where Player 1 is at in their turn.

        Positions:
                        POV_INDEX + 2



        POV_INDEX - 1                   POV_INDEX + 1




                         YOUR POV

        POV_INDEX - 1 and POV_INDEX + 1 will have to render their cards sideways. Shifting their card positions on the y index
        POV_INDEX + 2 will render cards upside down. It will be almost identical to rendering camera_pov_deck. The calculations for POV_INDEX + 2
        will be inverted because they are opposite of the POV.
    """
    camera_pov_index_maps = {
        0: [3, 1, 2],
        1: [0, 2, 3],
        2: [1, 3, 0],
        3: [2, 0, 1],
    }
    """
    index 0 = Render left
    index 1 = Render right
    index 2 = Render across
    """
    if player_index == camera_pov_index:
        return -1
    for index, position in enumerate(camera_pov_index_maps[camera_pov_index]):
        if position == player_index:
            return index


def percentage(percent, whole):
    return (percent * whole) / 100.0
