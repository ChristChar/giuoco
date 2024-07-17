import pygame
import sys
import Files.scripts.assets as assets
import Files.scripts.buttons as buttons
import Files.scripts.BattlersDatabase as data
import Files.scripts.Data.Moves as MovesData

def BaseCicle(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

def MenuCicles(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            buttons.ControllButtons(event)

def ShopCicles(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            buttons.ControllButtons(event)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            assets.mode = "game"

def GameCicles(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            buttons.ControllButtons(event)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            if assets.BattleMenuSelectedY == 1:
                assets.BattleMenuSelectedY = 0
        elif event.key == pygame.K_DOWN:
            if assets.BattleMenuSelectedY == 0:
                assets.BattleMenuSelectedY = 1
        elif event.key == pygame.K_LEFT:
            if assets.BattleMenuSelectedX == 1:
                assets.BattleMenuSelectedX = 0
        elif event.key == pygame.K_RIGHT:
            if assets.BattleMenuSelectedX == 0:
                assets.BattleMenuSelectedX = 1
        elif event.key == pygame.K_RETURN:
            if data.CurrentBattleAction[assets.BattleMenuSelectedY][assets.BattleMenuSelectedX] == "lotta":
                data.CurrentBattleAction = data.Gino1.MakeMoveList()
            elif data.CurrentBattleAction[assets.BattleMenuSelectedY][assets.BattleMenuSelectedX] == "-":
                pass
            elif data.CurrentBattleAction[assets.BattleMenuSelectedY][assets.BattleMenuSelectedX] in MovesData.MOVES:
                data.Turn(assets.screen, data.CurrentBattleAction[assets.BattleMenuSelectedY][assets.BattleMenuSelectedX] )
            elif data.CurrentBattleAction[assets.BattleMenuSelectedY][assets.BattleMenuSelectedX] == "negozio":
                assets.mode = "shop"
            elif data.CurrentBattleAction[assets.BattleMenuSelectedY][assets.BattleMenuSelectedX] == "Battlers":
                data.ViewTeam(assets.screen)
        elif event.key == pygame.K_BACKSPACE:
            data.CurrentBattleAction = data.battleAction

cicles = {"menu":MenuCicles, "game": GameCicles, "shop": ShopCicles}

def pygameEventCicles():
    for event in pygame.event.get():
        BaseCicle(event)
        cicles[assets.mode](event)
                    