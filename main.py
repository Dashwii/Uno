from init_stuff import *
from game_logic import Board
from fps_counter import fps_counter


class Game:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.events = []
        self.board = Board(self)
        self.show_frames = False

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.display.blit(BACKGROUND, (0, 0))
            self.board.play()
            if self.show_frames:
                fps_counter(self.clock.get_fps())

            pygame.display.update()
            self.event_clear()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_frames = not self.show_frames
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
            self.events.append(event)

    def event_clear(self):
        self.events = []

    def debug_code(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                for player in self.board.rotation_list:
                    print(player.name, player.deck)
            if event.key == pygame.K_u:
                print(self.board.game_flow.used_deck)
                print(len(self.board.game_flow.used_deck))
            if event.key == pygame.K_d:
                print(self.board.deck)
                print(len(self.board.deck))
            if event.key == pygame.K_f:
                print(self.board.board_rendering.used_deck_render)
                print(len(self.board.board_rendering.used_deck_render))
            if event.key == pygame.K_s:
                self.board.board_rendering.show_enemy_cards = not self.board.board_rendering.show_enemy_cards
                if self.board.board_rendering.show_enemy_cards:
                    print("Showing enemy cards on")
                else:
                    print("Showing enemy cards off")
            if event.key == pygame.K_t:
                self.board.AI_prevent_win = not self.board.AI_prevent_win
                if self.board.AI_prevent_win:
                    print("AI win prevention on")
                else:
                    print("AI win prevention off")


if __name__ == "__main__":
    game = Game()
    game.run()
