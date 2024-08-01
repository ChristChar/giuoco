import pygame
from Files.scripts import functions
import Files.scripts.assets as assets
import Files.scripts.dialogue as dialog
from Files.scripts.Data.Battlers import BattlersType


def Death(screen, Attacker, Defender, IsEnemy):
    Width, Height = screen.get_size()
    speed = 500
    Sound = functions.create_sound("Files/sound/death.mp3")
    Sound.play()
    Text = dialog.dialoge(Attacker.type + " non ha più energie")
    AttackerImage = BattlersType[Attacker.type]["sprite"]
    DefenderImage = BattlersType[Defender.type]["sprite"]
    if IsEnemy:
        scale = round(Height / 3)
        Ax, Ay = ((Width / 4) * 3) - scale / 2, (Height / 4) - scale / 2
        scale = round(Height / 1.6)
        Dx, Dy = (Width / 4) - scale / 2, (Height - Height / 3) - scale / 1.7
    else:
        scale = round(Height / 1.6)
        Ax, Ay = (Width / 4) - scale / 2, (Height - Height / 3) - scale / 1.7
        scale = round(Height / 3)
        Dx, Dy = ((Width / 4) * 3) - scale / 2, (Height / 4) - scale / 2
    Move = 0
    while True:
        screen.fill((0, 0, 0))  # Riempie lo schermo con il colore nero
        back = pygame.transform.scale(assets.back, (Width, Height))
        screen.blit(back, (0, 0))
        if IsEnemy:
            scale = round(Height / 3)
            sprite = pygame.transform.scale(AttackerImage, (scale, scale))
            EnemySurface = pygame.Surface((scale,scale), pygame.SRCALPHA)
            EnemySurface.blit(sprite, (0, Move))
            screen.blit(EnemySurface, (Ax, Ay))
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(DefenderImage, (scale, scale)), True, False)
            screen.blit(sprite, (Dx, Dy))
        else:
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(AttackerImage, (scale, scale)), True, False)
            EnemySurface = pygame.Surface((scale,scale), pygame.SRCALPHA)
            EnemySurface.blit(sprite, (0, Move))
            screen.blit(EnemySurface, (Ax, Ay))
            scale = round(Height / 3)
            sprite = pygame.transform.scale(DefenderImage, (scale, scale))
            screen.blit(sprite, (Dx, Dy))
        Move += speed * assets.delta_time
        if Move >= scale:
            break
        Text.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    back = pygame.transform.scale(assets.back, (Width, Height))
    screen.blit(back, (0,0))
    if IsEnemy:
        Defender.Draw(screen, False)
        Attacker.drawStateBar(screen, True)
    else:
        Defender.Draw(screen, True)
        Attacker.drawStateBar(screen, False)
    Text.update(screen)