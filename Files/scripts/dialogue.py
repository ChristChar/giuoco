import pygame
from sys import exit
import Files.scripts.assets as assets

def draw_text_within(surface, text, shape, font, color):
    words = text.split(" ")
    line = ""
    y = shape.top
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] <= shape.width:
            line = test_line
        else:
            text_surface = font.render(line, True, color)
            surface.blit(text_surface, (shape.left, y))
            line = word + " "
            y += font.get_height()
    text_surface = font.render(line, True, color)
    surface.blit(text_surface, (shape.left, y))

class dialoge:
    def __init__(self, text):
        self.text = text
    
    def draw(self, screen):
        Width, Height = assets.ScreenDimension
        pygame.draw.rect(screen, (200,200,200), (10, Height - Height/3, Width-20, Height/3))
        pygame.draw.rect(screen, (255,255,255), (20, Height - Height/3 + 20, Width-40, Height/3 - 40))
        TextRect = pygame.rect.Rect(25, Height - Height/3 + 45, Width-50, Height/3 - 50)
        font = pygame.font.SysFont(None, round(Height/15))
        draw_text_within(screen, self.text, TextRect, font, (0,0,0))
        font = pygame.font.SysFont(None, round(Height/14))
    
    def update(self, screen):
        self.draw(screen)
        pygame.display.flip()
        Waiting = True
        while Waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Waiting = False