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
    back = pygame.transform.scale(assets.bacck, (Width, Height))
    screen.blit(back, (0,0))
    data.Gino1.Draw(screen, False)
    data.Gino2.Draw(screen, True)
    Battle_text.draw(screen)
    data.DrawBattleSelection(screen)

def Shop(screen):
    screen.fill((0,255,255))
    butt.updateButtons(screen)


DrawForMode = {"menu":Menu, "game":Game, "shop":Shop}

def Draw(screen):
    DrawForMode[assets.mode](screen)