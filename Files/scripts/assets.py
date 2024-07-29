import pygame
import Files.scripts.BattlersSpawnChance as E

#image
bacck = pygame.image.load("Files/image/back.webp")
arrow = pygame.image.load("Files/image/arrow.png")

BattleMenuSelectedX = 0
BattleMenuSelectedY = 0
score = 0
delta_time = 0
mode = "menu"
spawn_list = E.spawn_list
SHOP = False