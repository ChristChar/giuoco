import pygame
import Files.scripts.assets as assets

assets.SHOP = True

import Files.scripts.draw as Draw
import Files.scripts.pygameEventCycles as Cycles


with open("Files/stats.stt", 'r') as file:
    lines = [line.rstrip('\n') for line in file.readlines()]
assets.score = int(lines[0])

with open("Files/modific.stt", 'r') as file:
    lines = [line.rstrip('\n') for line in file.readlines()]
StatX = lines[0].split(",")
for i, X in enumerate(StatX):
    StatX[i] = float(X) 
assets.Stats = StatX

assets.costo = {1.0:20,1.1:40,1.2:60,1.3:100,1.4:130,1.5:160,1.6:200,1.7:250,1.8:280,1.9:300}

pygame.init()

screen = pygame.display.set_mode((800,600), pygame.RESIZABLE)

assets.screen = screen

clock = pygame.time.Clock()

assets.mode = "statshop"

while True:
    clock.tick()
    assets.delta_time = clock.get_time() / 1000.0
    assets.ScreenDimension = screen.get_size()
    Cycles.pygameEventCicles()
    Draw.Draw(screen)
    pygame.display.update()
