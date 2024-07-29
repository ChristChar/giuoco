import Files.scripts.assets as assets

with open("Files/modific.stt", 'r') as file:
    lines = [line.rstrip('\n') for line in file.readlines()]
StatX = lines[0].split(",")
for i, X in enumerate(StatX):
    StatX[i] = float(X) 
StatsX = {}
for i, stat in enumerate(["HP","ATT","MAGIC","DIF","FUN","VEL"]):
    StatsX[stat] = StatX[i]
assets.Stats = StatsX

import pygame
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
