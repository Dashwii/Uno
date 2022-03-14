import pygame
pygame.font.init()


class RenderText:
    def __init__(self, text, pos, color="white", font_size=35, background_color=None):
        self.text = text
        self.background = False
        self.screen = pygame.display.get_surface()
        self.font_size = font_size
        self.font = pygame.font.SysFont("arial", self.font_size)
        self.color = color
        self.text_surface = self.font.render(text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.x, self.text_rect.y = pos[0] - self.text_rect.width // 2, pos[1] - self.text_rect.height // 2
        if background_color is not None:
            self.background = True
            self.temp_surface = pygame.Surface(self.text_surface.get_size())
            self.temp_surface.fill(background_color)

    def render(self):
        if self.background:
            self.screen.blit(self.temp_surface, (self.text_rect.x, self.text_rect.y))
        self.screen.blit(self.text_surface, (self.text_rect.x, self.text_rect.y))

    def update_color(self, color):
        self.color = color
        self.text_surface = self.font.render(self.text, True, self.color)

    def update_text(self, text):
        self.text = text
        self.text_surface = self.font.render(text, True, self.color)




