import pygame
import Files.scripts.assets as assets
import Files.scripts.draw as Draw
import Files.scripts.pygameEventCycles as Cycles

assets.SHOP = True

with open("Files/stats.stt", 'r') as file:
    lines = [line.rstrip('\n') for line in file.readlines()]
assets.score = int(lines[0])

with open("Files/modific.stt", 'r') as file:
    lines = [line.rstrip('\n') for line in file.readlines()]
StatX = lines[0].split(",")
for i, X in enumerate(StatX):
    StatX[i] = float(X) 
assets.Stats = StatX

assets.costo = {1.0:10,1.1:20,1.2:30,1.3:50,1.4:65,1.5:80,1.6:95,1.7:110,1.8:130,1.9:150}

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
