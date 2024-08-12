import pygame
import sys
import ctypes
import Files.scripts.assets as assets
import Files.scripts.buttons as buttons
import Files.scripts.setting as setting
import Files.scripts.BattlersDatabase as data
import Files.scripts.Data.Moves as MovesData
import Files.scripts.Data.world as World

def BaseCicle(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            setting.open_settings_window()

def InShopBaseCicle(event):
    if event.type == pygame.QUIT:
        with open("Files/stats.stt", 'w') as file:
            file.write(str(assets.score))
        with open("Files/modific.stt", 'w') as file:
            file.write(','.join(map(str, assets.Stats)))
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
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
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
            action = data.CurrentBattleAction[assets.BattleMenuSelectedY][assets.BattleMenuSelectedX]
            if action == "lotta":
                data.CurrentBattleAction = data.Gino1.MakeMoveList()
            elif action == "-":
                pass
            elif action in MovesData.MOVES and data.Gino1.PP[action] > 0:
                data.Turn(assets.screen, action)
            elif action == "negozio":
                assets.mode = "shop"
            elif action == "Battlers":
                data.ViewTeam(assets.screen)
        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
            data.CurrentBattleAction = data.battleAction

def Stats(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, rect in enumerate(assets.ArrowRects):
                if assets.Stats[i] in assets.costo and rect.collidepoint(mouse_x, mouse_y):
                    input = ctypes.windll.user32.MessageBoxW(None, f"Vuoi spedere {assets.costo[assets.Stats[i]]} punti per Upgredare {data.Stats[i]}", "Game", 0x00000004)
                    if input == 6:
                        if assets.score >= assets.costo[assets.Stats[i]]:
                            assets.score -= assets.costo[assets.Stats[i]]
                            assets.Stats[i] += 0.1
                            assets.Stats[i] = round(assets.Stats[i], 2)
                        else:
                            ctypes.windll.user32.MessageBoxW(0, 'SEI POVERO', 'Lolo', 0x10)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            assets.mode = "statshop"
                        
cicles = {"menu":MenuCicles, "game": GameCicles, "shop": ShopCicles, "statshop":MenuCicles,"Stats":Stats}

def pygameEventCicles():
    for event in pygame.event.get():
        if assets.SHOP:
            InShopBaseCicle(event)
        else:
            BaseCicle(event)
        cicles[assets.mode](event)
        assets.back = World.image[assets.World]
                    