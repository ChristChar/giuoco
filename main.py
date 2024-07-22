import pygame
import Files.scripts.assets as assets
import Files.scripts.pygameEventCycles as Cycles
import Files.scripts.buttons as butt
import Files.scripts.BattlersDatabase as data
import Files.scripts.dialogue as dialog

pygame.init()

screen = pygame.display.set_mode((800,600), pygame.RESIZABLE)


assets.screen = screen

clock = pygame.time.Clock()
Battle_text = dialog.dialoge("cosa devi fare?")

while True:
    clock.tick()
    assets.delta_time = clock.get_time() / 1000.0
    assets.ScreenDimension = screen.get_size()
    Width, Height = assets.ScreenDimension
    Cycles.pygameEventCicles()
    if assets.mode == "menu":
        screen.fill((255,255,255))
        font = pygame.font.SysFont(None, round(Height/8))
        TITOLO = font.render("dgjkdjsjkdfs", True, (0,0,0))
        WW, HH = TITOLO.get_size()
        screen.blit(TITOLO, (Width/2-WW/2, Height/4- HH/2))
        butt.updateButtons(screen)
    elif assets.mode == "game":
        back = pygame.transform.scale(assets.bacck, (Width, Height))
        screen.blit(back, (0,0))
        data.Gino1.Draw(screen, False)
        data.Gino2.Draw(screen, True)
        Battle_text.draw(screen)
        data.DrawBattleSelection(screen)
    elif assets.mode == "shop":
        screen.fill((0,255,255))
        butt.updateButtons(screen)
    pygame.display.update()