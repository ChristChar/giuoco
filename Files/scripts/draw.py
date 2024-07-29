import pygame
import Files.scripts.buttons as butt
import Files.scripts.assets as assets
import Files.scripts.BattlersDatabase as data
import Files.scripts.dialogue as dialog

Battle_text = dialog.dialoge("cosa devi fare?")

def Menu(screen):
    Width, Height = assets.ScreenDimension
    screen.fill((255,255,255))
    font = pygame.font.SysFont(None, round(Height/8))
    TITOLO = font.render("dgjkdjsjkdfs", True, (0,0,0))
    WW, HH = TITOLO.get_size()
    screen.blit(TITOLO, (Width/2-WW/2, Height/4- HH/2))
    butt.updateButtons(screen)

def Game(screen):
    Width, Height = assets.ScreenDimension
    back = pygame.transform.scale(assets.back, (Width, Height))
    screen.blit(back, (0,0))
    data.Gino1.Draw(screen, False)
    data.Gino2.Draw(screen, True)
    Battle_text.draw(screen)
    data.DrawBattleSelection(screen)

def Shop(screen):
    screen.fill((0,255,255))
    butt.updateButtons(screen)

def StatShop(screen):
    screen.fill((255,255,255))
    W, H = screen.get_size()
    Font = pygame.font.SysFont(None , round(H/10))
    Score = Font.render(f"Punti: {assets.score}", True, (0,0,0))
    screen.blit(Score, (10,10))
    butt.updateButtons(screen)

def Stat_Menu(screen):
    screen.fill((255,255,255))
    W, H = screen.get_size()
    Font = pygame.font.SysFont(None , round(H/10))
    Score = Font.render(f"Punti: {assets.score}", True, (0,0,0))
    screen.blit(Score, (10,10))
    Font = pygame.font.SysFont(None , round(H/12))
    He = Font.get_height()
    Arrow = pygame.transform.scale(assets.arrow, (He, He))
    assets.ArrowRects = []
    for i, stat in enumerate(data.Stats):
        StatText = Font.render(f"{stat}: {assets.Stats[i]}", True, (0,0,0))
        screen.blit(StatText, (W/2.5, H/2-He*(3-i)-(50-i*10)))
        screen.blit(Arrow, (W/1.7, H/2-He*(3-i)-(50-i*10)))
        assets.ArrowRects.append(pygame.rect.Rect((W/1.7, H/2-He*(3-i)-(50-i*10), He, He)))


DrawForMode = {"menu":Menu, "game":Game, "shop":Shop,"statshop":StatShop, "Stats":Stat_Menu}

def Draw(screen):
    DrawForMode[assets.mode](screen)