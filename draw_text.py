from init_stuff import *
pygame.font.init()


class DrawText:
    def __init__(self, text, pos, font_size=35, color="white"):
        self.display = pygame.display.get_surface()
        self.text = str(text)
        self.position = pos
        self.color = color
        self.font = pygame.font.SysFont("arial", int(font_size * SCALING_RATIO))
        self.text_surface = self.font.render(self.text, True, self.color)

    def render(self):
        self.display.blit(self.text_surface, (self.position[0], self.position[1]))

    def update_color(self, color):
        self.color = color
        self.text_surface = self.font.render(self.text, True, self.color)

    def update_text(self, text):
        self.text = str(text)
        self.text_surface = self.font.render(self.text, True, self.color)
