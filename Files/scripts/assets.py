import pygame

#image
arrow = pygame.image.load("Files/image/arrow.png")

BattleMenuSelectedX = 0
BattleMenuSelectedY = 0
score = 0
delta_time = 0
mode = "menu"
World = None
SHOP = False
Stats = {"HP":1,"ATT":1,"MAGIC":1,"DIF":1,"FUN":1,"VEL":1}