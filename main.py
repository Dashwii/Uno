from init_stuff import *
from game_logic import Board


class Game:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.events = []
        self.board = Board(self)

    def run(self):
        while True:
            self.handle_events()
            self.display.blit(BACKGROUND, (0, 0))
            self.board.play()
            pygame.display.update()
            self.clock.tick(FPS)
            self.event_clear()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            self.events.append(event)

    def event_clear(self):
        self.events = []


if __name__ == "__main__":
    game = Game()
    game.run()
