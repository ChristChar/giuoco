import math
import pygame
import Files.scripts.assets as assets
import Files.scripts.dialogue as dialog
from Files.scripts.Data.Battlers import BattlersType

pygame.mixer.init()

#effetti
def AssorbiVita(screen, damage, self):
    Heal = damage/2
    self.HP = min(self.HP + Heal, self.maxHP)
    self.drawStateBar(screen, self.isEnemy)
    Text = dialog.dialoge(f"{self.type} si cura!")
    Text.update(screen)

def AfterSkipTurn(screen, self):
    self.riposo = True


#animazioni
def Defoult(screen, Move, Attacker, Defender, IsEnemy):
    Width, Height = screen.get_size()
    slap = pygame.mixer.Sound("Files/sound/slap.mp3")
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

    speed = 25  # Velocità di movimento

    while True:
        screen.fill((0, 0, 0))  # Riempie lo schermo con il colore nero
        back = pygame.transform.scale(assets.bacck, (Width, Height))
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
    back = pygame.transform.scale(assets.bacck, (Width, Height))
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
        roar = pygame.mixer.Sound(f"Files/sound/{MOVES[Move]["sound"]}")
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
        back = pygame.transform.scale(assets.bacck, (Width, Height))
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
    back = pygame.transform.scale(assets.bacck, (Width, Height))
    screen.blit(back, (0,0))
    if IsEnemy:
        Defender.Draw(screen, False)
        Attacker.Draw(screen, True)
    else:
        Defender.Draw(screen, True)
        Attacker.Draw(screen, False)
    Text.draw(screen)
    pygame.display.update()
        
        

MOVES = {
    "azione": {
        "type": "normale",
        "MoveType": "Fisica",
        "BasePower": 40,
        "precisione": 100,
        "target": "enemy"
    },
    "smog": {
        "type": "veleno",
        "MoveType": "Fisica",
        "BasePower": 35,
        "precisione": 100,
        "target": "enemy"
    },
    "Braciere": {
        "type": "fuoco",
        "MoveType": "Magic",
        "BasePower": 40,
        "precisione": 100,
        "target": "enemy"
    },
    "Sassata": {
        "type": "sasso",
        "MoveType": "Fisica",
        "BasePower": 55,
        "precisione": 95,
        "target": "enemy"
    },
    "Trhyhard": {
        "type": "gamer",
        "MoveType": "State",
        "precisione": 95,
        "Stat": [{"stats": ["ATT","MAGIC"], "Power": 0.2, "Target":"self"}],
        "target": "self",
        "animation":State
    },
    "vento": {
        "type": "gas",
        "MoveType": "Magic",
        "BasePower": 55,
        "precisione": 95,
        "target": "enemy"
    },
    "Tuonoshock": {
        "type": "elettro",
        "MoveType": "Magic",
        "BasePower": 40,
        "precisione": 100,
        "target": "enemy"
    },
    "Morso": {
        "type": "normale",
        "MoveType": "Fisica",
        "BasePower": 60,
        "precisione": 100,
        "target": "enemy"
    },
    "Lanciafiamme": {
        "type": "fuoco",
        "MoveType": "Magic",
        "BasePower": 90,
        "precisione": 95,
        "target": "enemy"
    },
    "Brilla": {
        "type": "luce",
        "MoveType": "Magic",
        "BasePower": 80,
        "precisione": 85,
        "Stat": [{"stats": ["PRECISIONE"], "Power": -0.3, "Target":"enemy", "probabilità":65}],
        "target": "enemy"
    },
    "IPER RAGGIO": {
        "type": "magia",
        "MoveType": "Magic",
        "BasePower": 200,
        "precisione": 100,
        "Scripts": [AfterSkipTurn],
        "target": "enemy"
    },
    "sanguisuga": {
        "type": "insetto",
        "MoveType": "Fisica",
        "BasePower": 55,
        "precisione": 95,
        "ScriptDmage": [AssorbiVita],
        "target": "enemy"
    },
    "ronzio rompi palle": {
        "type": "insetto",
        "MoveType": "State",
        "Stat": [{"stats": ["ELUSIONE"], "Power": 0.4, "Target":"self"}],
        "precisione": 95,
        "target": "self",
        "animation": State,
        "sound":"pew.mp3"
    },
    "Ctrl+C Ctrl+V": {
        "type": "informatico",
        "MoveType": "State",
        "Stat": [{"stats": ["ELUSIONE"], "Power": 0.7, "Target":"self"}],
        "precisione": 100,
        "target": "self",
        "animation": State,
        "sound":"pew.mp3"
    },
    "inquinamento": {
        "type": "plastica",
        "MoveType": "Fisica",
        "BasePower": 65,
        "target": "enemy"
    },
    "Dragoartigli": {
        "type": "drago",
        "MoveType": "Fisica",
        "BasePower": 80,
        "precisione": 90,
        "target": "enemy"
    },
    "Erba schiaffo": {
        "type": "erba",
        "MoveType": "Fisica",
        "BasePower": 55,
        "precisione": 100,
        "target": "enemy"
    },
    "taskkill": {
        "type": "informatico",
        "MoveType": "Magic",
        "BasePower": 80,
        "precisione": 90,
        "target": "enemy"
    },
    "Pistolacqua": {
        "type": "acqua",
        "MoveType": "Magic",
        "BasePower": 40,
        "precisione": 100,
        "target": "enemy"
    },
    "Geloraggio": {
        "type": "ghiaccio",
        "MoveType": "Magic",
        "BasePower": 80,
        "precisione": 95,
        "target": "enemy"
    },
    "rickroll": {
        "type": "meme",
        "MoveType": "Fisica",
        "BasePower": 60,
        "precisione": 95,
        "target": "enemy"
    },
    "sparo": {
        "type": "pistola",
        "MoveType": "Fisica",
        "BasePower": 120,
        "precisione": 50,
        "target": "enemy"
    },
    "ballo": {
        "type": "meme",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT", "DIF","VEL"], "Power": 0.3, "Target":"self"}],
        "precisione": 80,
        "target": "self",
        "animation": State,
        "sound":"drip.mp3"
    },
    "IMPOSTOR": {
        "type": "meme",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT"], "Power": 0.4, "Target":"self"},{"stats": ["DIF"], "Power": -0.2, "Target":"self"}],
        "target": "self",
        "animation": State,
        "sound":"sus.mp3"
    },
    "Machine Learning": {
        "type": "AI",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT","MAGIC","DIF","FUN","VEL"], "Power": 0.7, "Target":"self"}],
        "precisione": 100,
        "Scripts": [AfterSkipTurn],
        "target": "self",
        "animation": State
    },
    "rugito": {
        "type": "normale",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT"], "Power": -0.2, "Target":"enemy"}],
        "precisione": 100,
        "target": "enemy",
        "animation": State,
        "sound":"roar.mp3"
    },
    "Fissare": {
        "type": "normale",
        "MoveType": "State",
        "Stat": [{"stats": ["PRECISIONE"], "Power": 2, "Target":"self"}],
        "precisione": 100,
        "target": "self",
        "animation": State,
        "sound":"pew.mp3"
    },
    "carineria": {
        "type": "cute",
        "MoveType": "Fisica",
        "BasePower": 80,
        "Stat": [{"stats": ["DIF"], "Power": -0.1, "Target":"self", "probabilità":35}],
        "precisione": 90,
        "target": "enemy"
    }
}