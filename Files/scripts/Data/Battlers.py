import pygame
import json

with open('Files/JSON/BattlersData.json', encoding='utf-8') as f:
    BattlersType = json.load(f)

for i in BattlersType:
    BattlersType[i]["sprite"] = pygame.image.load("Files/image/Battlers/"+i+".png")