import pygame
import Files.scripts.assets as assets
import Files.scripts.draw as Draw
import Files.scripts.pygameEventCycles as Cycles

pygame.init()

screen = pygame.display.set_mode((800,600), pygame.RESIZABLE)

assets.screen = screen

clock = pygame.time.Clock()

while True:
    clock.tick()
    assets.delta_time = clock.get_time() / 1000.0
    assets.ScreenDimension = screen.get_size()
    Cycles.pygameEventCicles()
    Draw.Draw(screen)
    pygame.display.update()
