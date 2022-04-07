from draw_text import *

fps_text = DrawText(0, (0, 0))


def fps_counter(fps_count):
    global fps_text
    fps_count = round(fps_count, 1)
    p_display = pygame.display.get_surface()

    fps_text.update_text(f"FPS: {fps_count}")
    fps_text_rect = fps_text.text_surface.get_rect()
    pygame.draw.rect(p_display, "black", fps_text_rect)
    fps_text.render()


