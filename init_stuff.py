import pygame

WIDTH = 1920
HEIGHT = 1080

DESIGN_WIDTH = 1920
DESIGN_HEIGHT = 1080


SCALING_RATIO = DESIGN_WIDTH / WIDTH

FPS = 60

CARD_WIDTH = 150 / SCALING_RATIO
CARD_HEIGHT = 200 / SCALING_RATIO


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.mixer.init()
pygame.mixer.music.load("assets/music/music flip theme.mp3")
pygame.mixer.music.set_volume(0.05)

display = pygame.display.set_mode((WIDTH, HEIGHT))

BOARD_DIRECTION = pygame.transform.scale(pygame.image.load("assets/Uno Game Assets/board_direction.png").convert_alpha(), (DESIGN_WIDTH / SCALING_RATIO, DESIGN_HEIGHT / SCALING_RATIO))
BOARD_DIRECTION_REVERSE = pygame.transform.scale(pygame.image.load("assets/Uno Game Assets/board_direction_reverse.png").convert_alpha(), (DESIGN_WIDTH / SCALING_RATIO, DESIGN_HEIGHT / SCALING_RATIO))
SKIPPED_ICON = pygame.transform.scale(pygame.image.load("assets/Uno Game Assets/Skipped.png").convert_alpha(), (DESIGN_WIDTH / SCALING_RATIO, DESIGN_HEIGHT / SCALING_RATIO))

BACKGROUND = pygame.transform.scale(pygame.image.load("assets/Uno Game Assets/Table_0.png"), (WIDTH, HEIGHT)).convert_alpha()
BACKGROUND_ALT = pygame.transform.scale(pygame.image.load("assets/Uno Game Assets/Table_1.png"), (WIDTH, HEIGHT)).convert_alpha()

Blue_0 = pygame.transform.scale(pygame.image.load('assets/cards/Blue_0.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_1 = pygame.transform.scale(pygame.image.load('assets/cards/Blue_1.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_2 = pygame.transform.scale(pygame.image.load('assets/cards/Blue_2.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_3 = pygame.transform.scale(pygame.image.load('assets/cards/Blue_3.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_4 = pygame.transform.scale(pygame.image.load('assets/cards/Blue_4.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_5 = pygame.transform.scale(pygame.image.load('assets/cards/Blue_5.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_6 = pygame.transform.scale(pygame.image.load('assets/cards/Blue_6.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_7 = pygame.transform.scale(pygame.image.load('assets/cards/Blue_7.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_8 = pygame.transform.scale(pygame.image.load('assets/cards/Blue_8.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_9 = pygame.transform.scale(pygame.image.load('assets/cards/Blue_9.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_Draw = pygame.transform.scale(pygame.image.load('assets/cards/Blue_Draw.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_Reverse = pygame.transform.scale(pygame.image.load('assets/cards/Blue_Reverse.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_Skip = pygame.transform.scale(pygame.image.load('assets/cards/Blue_Skip.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_0 = pygame.transform.scale(pygame.image.load('assets/cards/Green_0.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_1 = pygame.transform.scale(pygame.image.load('assets/cards/Green_1.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_2 = pygame.transform.scale(pygame.image.load('assets/cards/Green_2.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_3 = pygame.transform.scale(pygame.image.load('assets/cards/Green_3.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_4 = pygame.transform.scale(pygame.image.load('assets/cards/Green_4.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_5 = pygame.transform.scale(pygame.image.load('assets/cards/Green_5.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_6 = pygame.transform.scale(pygame.image.load('assets/cards/Green_6.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_7 = pygame.transform.scale(pygame.image.load('assets/cards/Green_7.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_8 = pygame.transform.scale(pygame.image.load('assets/cards/Green_8.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_9 = pygame.transform.scale(pygame.image.load('assets/cards/Green_9.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_Draw = pygame.transform.scale(pygame.image.load('assets/cards/Green_Draw.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_Reverse = pygame.transform.scale(pygame.image.load('assets/cards/Green_Reverse.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_Skip = pygame.transform.scale(pygame.image.load('assets/cards/Green_Skip.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_0 = pygame.transform.scale(pygame.image.load('assets/cards/Red_0.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_1 = pygame.transform.scale(pygame.image.load('assets/cards/Red_1.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_2 = pygame.transform.scale(pygame.image.load('assets/cards/Red_2.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_3 = pygame.transform.scale(pygame.image.load('assets/cards/Red_3.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_4 = pygame.transform.scale(pygame.image.load('assets/cards/Red_4.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_5 = pygame.transform.scale(pygame.image.load('assets/cards/Red_5.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_6 = pygame.transform.scale(pygame.image.load('assets/cards/Red_6.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_7 = pygame.transform.scale(pygame.image.load('assets/cards/Red_7.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_8 = pygame.transform.scale(pygame.image.load('assets/cards/Red_8.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_9 = pygame.transform.scale(pygame.image.load('assets/cards/Red_9.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_Draw = pygame.transform.scale(pygame.image.load('assets/cards/Red_Draw.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_Reverse = pygame.transform.scale(pygame.image.load('assets/cards/Red_Reverse.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_Skip = pygame.transform.scale(pygame.image.load('assets/cards/Red_Skip.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_0 = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_0.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_1 = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_1.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_2 = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_2.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_3 = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_3.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_4 = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_4.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_5 = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_5.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_6 = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_6.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_7 = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_7.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_8 = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_8.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_9 = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_9.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_Draw = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_Draw.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_Reverse = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_Reverse.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_Skip = pygame.transform.scale(pygame.image.load('assets/cards/Yellow_Skip.png'), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Black_Wild = pygame.transform.scale(pygame.image.load("assets/cards/Wild.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Black_Wild_Draw = pygame.transform.scale(pygame.image.load("assets/cards/Wild_Draw.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Uno_Back = pygame.transform.scale(pygame.image.load("assets/cards/Deck.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()

Red_Wild = pygame.transform.scale(pygame.image.load("assets/cards/Wild_Red.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_Wild = pygame.transform.scale(pygame.image.load("assets/cards/Wild_Green.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_Wild = pygame.transform.scale(pygame.image.load("assets/cards/Wild_Blue.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_Wild = pygame.transform.scale(pygame.image.load("assets/cards/Wild_Yellow.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Red_Wild_Draw = pygame.transform.scale(pygame.image.load("assets/cards/Wild_Draw_Red.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Green_Wild_Draw = pygame.transform.scale(pygame.image.load("assets/cards/Wild_Draw_Green.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Blue_Wild_Draw = pygame.transform.scale(pygame.image.load("assets/cards/Wild_Draw_Blue.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()
Yellow_Wild_Draw = pygame.transform.scale(pygame.image.load("assets/cards/Wild_Draw_Yellow.png"), (CARD_WIDTH, CARD_HEIGHT)).convert_alpha()

card_image_map = {('Blue', '0'): Blue_0, ('Blue', '1'): Blue_1, ('Blue', '2'): Blue_2, ('Blue', '3'): Blue_3, ('Blue', '4'): Blue_4,
                  ('Blue', '5'): Blue_5, ('Blue', '6'): Blue_6, ('Blue', '7'): Blue_7, ('Blue', '8'): Blue_8, ('Blue', '9'): Blue_9,
                  ('Blue', 'draw'): Blue_Draw, ('Blue', 'reverse'): Blue_Reverse, ('Blue', 'skip'): Blue_Skip, ('Green', '0'): Green_0,
                  ('Green', '1'): Green_1, ('Green', '2'): Green_2, ('Green', '3'): Green_3, ('Green', '4'): Green_4, ('Green', '5'): Green_5,
                  ('Green', '6'): Green_6, ('Green', '7'): Green_7, ('Green', '8'): Green_8, ('Green', '9'): Green_9, ('Green', 'draw'): Green_Draw,
                  ('Green', 'reverse'): Green_Reverse, ('Green', 'skip'): Green_Skip, ('Red', '0'): Red_0, ('Red', '1'): Red_1, ('Red', '2'): Red_2,
                  ('Red', '3'): Red_3, ('Red', '4'): Red_4, ('Red', '5'): Red_5, ('Red', '6'): Red_6, ('Red', '7'): Red_7, ('Red', '8'): Red_8,
                  ('Red', '9'): Red_9, ('Red', 'draw'): Red_Draw, ('Red', 'reverse'): Red_Reverse, ('Red', 'skip'): Red_Skip, ('Yellow', '0'): Yellow_0,
                  ('Yellow', '1'): Yellow_1, ('Yellow', '2'): Yellow_2, ('Yellow', '3'): Yellow_3, ('Yellow', '4'): Yellow_4, ('Yellow', '5'): Yellow_5,
                  ('Yellow', '6'): Yellow_6, ('Yellow', '7'): Yellow_7, ('Yellow', '8'): Yellow_8, ('Yellow', '9'): Yellow_9, ('Yellow', 'draw'): Yellow_Draw,
                  ('Yellow', 'reverse'): Yellow_Reverse, ('Yellow', 'skip'): Yellow_Skip, ("Black", "wild"): Black_Wild, ("Black", "wild draw"): Black_Wild_Draw
                  }

asset_map = {"Uno Card Back": Uno_Back, "Board Direction": BOARD_DIRECTION, "Board Direction Reversed": BOARD_DIRECTION_REVERSE,
             "Skipped Icon": SKIPPED_ICON, "Background": BACKGROUND, "Background Alt": BACKGROUND_ALT}

wild_image_color_map = {"red": Red_Wild, "green": Green_Wild, "blue": Blue_Wild, "yellow": Yellow_Wild}
wild_draw_image_color_map = {"red": Red_Wild_Draw, "green": Green_Wild_Draw, "blue": Blue_Wild_Draw, "yellow": Yellow_Wild_Draw}


def asset_scaler():
    global SCALING_RATIO
    SCALING_RATIO = DESIGN_WIDTH / pygame.display.get_surface().get_width()
    for key, image in card_image_map.items():
        image = pygame.transform.scale(image, (image.get_width() / SCALING_RATIO, image.get_height() / SCALING_RATIO))
        card_image_map[key] = image
    for key, asset in asset_map.items():
        asset = pygame.transform.scale(asset, (asset.get_width() / SCALING_RATIO, asset.get_height() / SCALING_RATIO))
        asset_map[key] = asset
    for key, asset in wild_image_color_map.items():
        asset = pygame.transform.scale(asset, (asset.get_width() / SCALING_RATIO, asset.get_height() / SCALING_RATIO))
        wild_image_color_map[key] = asset
    for key, asset in wild_draw_image_color_map.items():
        asset = pygame.transform.scale(asset, (asset.get_width() / SCALING_RATIO, asset.get_height() / SCALING_RATIO))
        wild_draw_image_color_map[key] = asset

"""
Instead of using variables I'm calling my assets from dictionaries because it allows me to change their image scales easily. 
I can't rescale a pygame surface in place so I have to edit the variable itself. Calling from dictionaries make life easier for this."""

