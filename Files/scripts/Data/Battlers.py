import pygame
import json

f = open('Files/JSON/BattlersData.json')

BattlersType = json.load(f)

for i in BattlersType:
    BattlersType[i]["sprite"] = pygame.image.load("Files/image/Battlers/"+i+".png")