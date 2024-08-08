import math
import pygame
import Files.scripts.assets as assets
import Files.scripts.dialogue as dialog
import json
import Files.scripts.functions as F
from Files.scripts.Data.Battlers import BattlersType

f = open('Files/JSON/MoveData.json')

MOVES = json.load(f)

def Defoult(screen, Move, Attacker, Defender, IsEnemy):
    Width, Height = screen.get_size()
    if "sound" in MOVES[Move]:
        roar = F.create_sound(f"Files/sound/{MOVES[Move]["sound"]}")
        roar.play()
    else:
        slap = F.create_sound("Files/sound/slap.mp3")
        slap.play()
    Text = dialog.dialoge(Attacker.type + " usa " + Move + "!!")
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

    speed = 1250 * assets.delta_time  # Velocità di movimento

    while True:
        screen.fill((0, 0, 0))  # Riempie lo schermo con il colore nero
        back = pygame.transform.scale(assets.back, (Width, Height))
        screen.blit(back, (0, 0))

        if IsEnemy:
            scale = round(Height / 3)
            sprite = pygame.transform.scale(AttackerImage, (scale, scale))
            screen.blit(sprite, (Ax, Ay))
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(DefenderImage, (scale, scale)), True, False)
            screen.blit(sprite, (Dx, Dy))
        else:
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(AttackerImage, (scale, scale)), True, False)
            screen.blit(sprite, (Ax, Ay))
            scale = round(Height / 3)
            sprite = pygame.transform.scale(DefenderImage, (scale, scale))
            screen.blit(sprite, (Dx, Dy))

        Text.draw(screen)

        dx = Dx - Ax
        dy = Dy - Ay
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < speed:  # Controlla se la distanza rimanente è minore della velocità
            break

        Ax += dx / distance * speed
        Ay += dy / distance * speed

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    back = pygame.transform.scale(assets.back, (Width, Height))
    screen.blit(back, (0,0))
    if IsEnemy:
        Defender.Draw(screen, False)
        Attacker.Draw(screen, True)
    else:
        Defender.Draw(screen, True)
        Attacker.Draw(screen, False)
    Text.draw(screen)
    pygame.display.update()

def State(screen, Move, Attacker, Defender, IsEnemy):
    Width, Height = screen.get_size()
    if "sound" in MOVES[Move]:
        roar = F.create_sound(f"Files/sound/{MOVES[Move]["sound"]}")
        roar.play()
        lenght = roar.get_length()
    else:
        lenght = 1.5
    speed = 300
    StaMuovendoADestra = True
    SuonoPartito = pygame.time.get_ticks()
    Text = dialog.dialoge(Attacker.type + " usa " + Move + "!!")
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
    AxOriginale = Ax
    while lenght > (pygame.time.get_ticks() - SuonoPartito) / 1000:
        MaxMove = Width/25
        screen.fill((0, 0, 0))  # Riempie lo schermo con il colore nero
        back = pygame.transform.scale(assets.back, (Width, Height))
        screen.blit(back, (0, 0))

        if IsEnemy:
            scale = round(Height / 3)
            sprite = pygame.transform.scale(AttackerImage, (scale, scale))
            screen.blit(sprite, (Ax, Ay))
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(DefenderImage, (scale, scale)), True, False)
            screen.blit(sprite, (Dx, Dy))
        else:
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(AttackerImage, (scale, scale)), True, False)
            screen.blit(sprite, (Ax, Ay))
            scale = round(Height / 3)
            sprite = pygame.transform.scale(DefenderImage, (scale, scale))
            screen.blit(sprite, (Dx, Dy))
        if StaMuovendoADestra:
            Ax += speed * assets.delta_time
            if Ax >= AxOriginale + MaxMove:
                StaMuovendoADestra = False
        else:
            Ax -= speed * assets.delta_time
            if Ax <= AxOriginale - MaxMove:
                StaMuovendoADestra = True
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
        Attacker.Draw(screen, True)
    else:
        Defender.Draw(screen, True)
        Attacker.Draw(screen, False)
    Text.draw(screen)
    pygame.display.update()


def LanciaPalle(screen, Move, Attacker, Defender, IsEnemy):
    Width, Height = screen.get_size()
    if "sound" in MOVES[Move]:
        roar = F.create_sound(f"Files/sound/{MOVES[Move]['sound']}")
        roar.play()
    Text = dialog.dialoge(Attacker.type + " usa " + Move + "!!")
    AttackerImage = BattlersType[Attacker.type]["sprite"]
    DefenderImage = BattlersType[Defender.type]["sprite"]

    if IsEnemy:
        scale = round(Height / 3)
        Ax, Ay = ((Width / 4) * 3) - scale / 2, (Height / 4) - scale / 2
        Bx, By = Ax + scale / 2, Ay + scale / 2
        scale = round(Height / 1.6)
        Dx, Dy = (Width / 4) - scale / 2, (Height - Height / 3) - scale / 1.7
        Arrx, Arry = Dx + scale / 2, Dy + scale / 2
    else:
        scale = round(Height / 1.6)
        Ax, Ay = (Width / 4) - scale / 2, (Height - Height / 3) - scale / 1.7
        Bx, By = Ax + scale / 2, Ay + scale / 2
        scale = round(Height / 3)
        Dx, Dy = ((Width / 4) * 3) - scale / 2, (Height / 4) - scale / 2
        Arrx, Arry = Dx + scale / 2, Dy + scale / 2

    speed = 1000 * assets.delta_time  # Velocità di movimento
    
    BALL_COLOR = MOVES[Move]["color"]
    DIMENSION = MOVES[Move]["dimension"]
    while True:
        screen.fill((0, 0, 0))  # Riempie lo schermo con il colore nero
        back = pygame.transform.scale(assets.back, (Width, Height))
        screen.blit(back, (0, 0))

        if IsEnemy:
            scale = round(Height / 3)
            sprite = pygame.transform.scale(AttackerImage, (scale, scale))
            screen.blit(sprite, (Ax, Ay))
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(DefenderImage, (scale, scale)), True, False)
            screen.blit(sprite, (Dx, Dy))
        else:
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(AttackerImage, (scale, scale)), True, False)
            screen.blit(sprite, (Ax, Ay))
            scale = round(Height / 3)
            sprite = pygame.transform.scale(DefenderImage, (scale, scale))
            screen.blit(sprite, (Dx, Dy))
        
        pygame.draw.circle(screen, BALL_COLOR, (Bx, By), round(DIMENSION / (Height / 1080)))

        Text.draw(screen)

        dx = Arrx - Bx
        dy = Arry - By
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < speed:  # Controlla se la distanza rimanente è minore della velocità
            break

        Bx += dx / distance * speed
        By += dy / distance * speed

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    back = pygame.transform.scale(assets.back, (Width, Height))
    screen.blit(back, (0, 0))
    if IsEnemy:
        Defender.Draw(screen, False)
        Attacker.Draw(screen, True)
    else:
        Defender.Draw(screen, True)
        Attacker.Draw(screen, False)
    Text.draw(screen)
    pygame.display.update()
        

def Brilla(screen, Move, Attacker, Defender, IsEnemy):
    Width, Height = screen.get_size()
    if "sound" in MOVES[Move]:
        roar = F.create_sound(f"Files/sound/{MOVES[Move]['sound']}")
        roar.play()
    Text = dialog.dialoge(Attacker.type + " usa " + Move + "!!")
    AttackerImage = BattlersType[Attacker.type]["sprite"]
    DefenderImage = BattlersType[Defender.type]["sprite"]

    if IsEnemy:
        scale = round(Height / 3)
        Ax, Ay = ((Width / 4) * 3) - scale / 2, (Height / 4) - scale / 2
        Bx, By = Ax + scale / 2, Ay + scale / 2
        scale = round(Height / 1.6)
        Dx, Dy = (Width / 4) - scale / 2, (Height - Height / 3) - scale / 1.7
    else:
        scale = round(Height / 1.6)
        Ax, Ay = (Width / 4) - scale / 2, (Height - Height / 3) - scale / 1.7
        Bx, By = Ax + scale / 2, Ay + scale / 2
        scale = round(Height / 3)
        Dx, Dy = ((Width / 4) * 3) - scale / 2, (Height / 4) - scale / 2

    speed = 1200 * assets.delta_time  # Velocità di movimento
    dimension = Height/10
    BALL_COLOR = MOVES[Move]["color"]
    while dimension < Height:
        screen.fill((0, 0, 0))  # Riempie lo schermo con il colore nero
        back = pygame.transform.scale(assets.back, (Width, Height))
        screen.blit(back, (0, 0))

        if IsEnemy:
            scale = round(Height / 3)
            sprite = pygame.transform.scale(AttackerImage, (scale, scale))
            screen.blit(sprite, (Ax, Ay))
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(DefenderImage, (scale, scale)), True, False)
            screen.blit(sprite, (Dx, Dy))
        else:
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(AttackerImage, (scale, scale)), True, False)
            screen.blit(sprite, (Ax, Ay))
            scale = round(Height / 3)
            sprite = pygame.transform.scale(DefenderImage, (scale, scale))
            screen.blit(sprite, (Dx, Dy))
        
        circle_surface = pygame.Surface((Height*2, Height*2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, BALL_COLOR, (Height, Height), round(dimension))
        screen.blit(circle_surface, (Bx-Height,By-Height))
        dimension += speed
        Text.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    back = pygame.transform.scale(assets.back, (Width, Height))
    screen.blit(back, (0, 0))
    if IsEnemy:
        Defender.Draw(screen, False)
        Attacker.Draw(screen, True)
    else:
        Defender.Draw(screen, True)
        Attacker.Draw(screen, False)
    Text.draw(screen)
    pygame.display.update()