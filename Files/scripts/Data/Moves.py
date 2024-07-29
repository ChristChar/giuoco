import math
import pygame
import random
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

def AfterSkipTurn(screen, self, enemy, move):
    self.riposo = True

def AfterDie(screen, self, enemy, move):
    self.HP = 0

def Flitch(screen, self, enemy, move):
    if random.random() < MOVES[move]["FlitchChance"] / 100:
        enemy.flitch = True

def PAR(screen, self, enemy, move):
    if random.random() < MOVES[move]["PARChance"] / 100:
        if enemy.state == None:
            if MOVES[move]["target"] == "enemy":
                Text = dialog.dialoge(f"{enemy.type} è paralizzato")
                enemy.state = "PAR"
            else:
                Text = dialog.dialoge(f"{self.type} è paralizzato")
                self.state = "PAR"
            Text.update(screen)

def BRN(screen, self, enemy, move):
    if random.random() < MOVES[move]["BRNChance"] / 100:
        if enemy.state == None:
            if MOVES[move]["target"] == "enemy":
                Text = dialog.dialoge(f"{enemy.type} è scottato")
                enemy.state = "BRN"
            else:
                Text = dialog.dialoge(f"{self.type} è scottato")
                self.state = "BRN"
            Text.update(screen)
            
def SLE(screen, self, enemy, move):
    if random.random() < MOVES[move]["SLEChance"] / 100:
        if enemy.state == None:
            if MOVES[move]["target"] == "enemy":    
                Text = dialog.dialoge(f"{enemy.type} è addormentato")
                enemy.state = "SLE"
            else:
                Text = dialog.dialoge(f"{self.type} è addormentato")
                self.state = "SLE"
            Text.update(screen)

def DRG(screen, self, enemy, move):
    if random.random() < MOVES[move]["DRGChance"] / 100:
        if enemy.state == None:
            if MOVES[move]["target"] == "enemy":
                Text = dialog.dialoge(f"{enemy.type} è sotto effetto di qualcosa di strano")
                enemy.state = "DRG"
            else:
                Text = dialog.dialoge(f"{self.type} è sotto effetto di qualcosa di strano")
                self.state = "DRG"
            Text.update(screen)
 
def POI(screen, self, enemy, move):
    if random.random() < MOVES[move]["POIChance"] / 100:
        if enemy.state == None:
            if MOVES[move]["target"] == "enemy":
                Text = dialog.dialoge(f"{enemy.type} è avvelenato")
                enemy.state = "POI"
            else:
                Text = dialog.dialoge(f"{self.type} è avvelenato")
                self.state = "POI"
            Text.update(screen)
            

#animazioni
def Defoult(screen, Move, Attacker, Defender, IsEnemy):
    Width, Height = screen.get_size()
    if "sound" in MOVES[Move]:
        roar = pygame.mixer.Sound(f"Files/sound/{MOVES[Move]["sound"]}")
        roar.play()
    else:
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
        roar = pygame.mixer.Sound(f"Files/sound/{MOVES[Move]['sound']}")
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
        
        pygame.draw.circle(screen, BALL_COLOR, (Bx, By), round(Height / DIMENSION))

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
        roar = pygame.mixer.Sound(f"Files/sound/{MOVES[Move]['sound']}")
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
        

MOVES = {
    "azione": {
        "type": "normale",
        "MoveType": "Fisica",
        "BasePower": 40,
        "precisione": 100,
        "target": "enemy"
    },
    "Panschiaffo": {
        "type": "cibo",
        "MoveType": "Fisica",
        "BasePower": 55,
        "precisione": 95,
        "target": "enemy"
    },
    "dormire": {
        "type": "normale",
        "MoveType": "State",
        "target": "self",
        "animation":State,
        "Scripts":[SLE],
        "SLEChance":100,
        "Dex":"Chi la usa dorme"
    },
    "ESPLOSIONE": {
        "type": "normale",
        "MoveType": "Fisica",
        "BasePower": 300,
        "precisione": 100,
        "target": "enemy",
        "animation": Brilla,
        "color": (255,255,255,85),
        "Scripts": [AfterDie],
        "Dex":"Chi la usa Esplode Morendo immediatamente"
        },
    "Ferrartigli": {
        "type": "acciaio",
        "MoveType": "Fisica",
        "BasePower": 55,
        "precisione": 95,
        "target": "enemy"
    },
    "Ferroscudo": {
        "type": "acciaio",
        "MoveType": "State",
        "precisione": 100,
        "Stat": [{"stats": ["DIF"], "Power": 0.5, "Target":"self"}],
        "target": "self",
        "animation":State,
        "Dex":"Chi la usa aumenta la sua difesa"
    },
    "Terremoto": {
        "type": "terra",
        "MoveType": "Fisica",
        "BasePower": 100,
        "precisione": 100,
        "target": "enemy",
        "animation": Brilla,
        "color": (150,50,0,85),
    },
    "smog": {
        "type": "veleno",
        "MoveType": "Fisica",
        "BasePower": 35,
        "precisione": 100,
        "target": "enemy",
        "animation": Brilla,
        "color": (150,0,150,85),
        "Scripts":[POI],
        "POIChance":10,
        "Dex":"Può avvelenare l'avversario"
    },
    "Braciere": {
        "type": "fuoco",
        "MoveType": "Magic",
        "BasePower": 40,
        "precisione": 100,
        "target": "enemy",
        "animation": LanciaPalle,
        "color": (255,200,0),
        "dimension":20,
        "Scripts":[BRN],
        "BRNChance": 5,
        "Dex":"Può scottare l'avversario"
    },
    "???": {
        "type": "glitch",
        "MoveType": "Magic",
        "BasePower": 100,
        "precisione": 85,
        "target": "enemy",
        "animation": LanciaPalle,
        "color": (0,0,0),
        "dimension":30,
        "Scripts":[DRG],
        "DRGChance": 5,
        "Dex":"???"
    },
    "Sassata": {
        "type": "sasso",
        "MoveType": "Fisica",
        "BasePower": 55,
        "precisione": 95,
        "target": "enemy",
        "animation": LanciaPalle,
        "color": (255,200,0),
        "dimension":10
    },
    "Trhyhard": {
        "type": "gamer",
        "MoveType": "State",
        "precisione": 95,
        "Stat": [{"stats": ["ATT","MAGIC"], "Power": 0.25, "Target":"self"}],
        "target": "self",
        "animation":State,
        "Dex":"Chi la usa aumenta l'attacco ed la magia"
    },
    "vento": {
        "type": "gas",
        "MoveType": "Magic",
        "BasePower": 55,
        "precisione": 95,
        "target": "enemy",
        "animation": LanciaPalle,
        "color": (200,200,200),
        "dimension":15,
    },
    "Tuonoshock": {
        "type": "elettro",
        "MoveType": "Magic",
        "BasePower": 40,
        "precisione": 100,
        "target": "enemy",
        "animation": LanciaPalle,
        "color": (255,255,0),
        "dimension":20,
        "Scripts":[PAR],
        "PARChance":10,
        "Dex":"Può causare la paralisi"
    },
    "Tuononda":{
        "type": "elettro",
        "MoveType": "State",
        "precisione": 100,
        "target": "enemy",
        "animation":State,
        "Scripts":[PAR],
        "PARChance":100,
        "Dex":"Chi la usa paralizza l'avversario"
    },
    "Morso": {
        "type": "normale",
        "MoveType": "Fisica",
        "BasePower": 60,
        "precisione": 100,
        "target": "enemy",
        "FlitchChance":20,
        "Scripts": [Flitch],
        "Dex":"può far tentennare l'avversario"
    },
    "Lanciafiamme": {
        "type": "fuoco",
        "MoveType": "Magic",
        "BasePower": 90,
        "precisione": 95,
        "target": "enemy",
        "animation": LanciaPalle,
        "color": (255,200,0),
        "dimension":15,
        "Scripts":[BRN],
        "BRNChance":12,
        "Dex":"Può scottare l'avversario"
    },
    "Brilla": {
        "type": "luce",
        "MoveType": "Magic",
        "BasePower": 80,
        "precisione": 85,
        "Stat": [{"stats": ["PRECISIONE"], "Power": -0.25, "Target":"enemy", "probabilità":65}],
        "target": "enemy",
        "animation": Brilla,
        "color": (255,255,255,85),
        "FlitchChance":30,
        "Scripts": [Flitch],
        "Dex":"Può sia Ridurre la precisione avversaria sia fallo tentennare"
    },
    "IPER RAGGIO": {
        "type": "magia",
        "MoveType": "Magic",
        "BasePower": 200,
        "precisione": 100,
        "Scripts": [AfterSkipTurn],
        "target": "enemy",
        "animation": LanciaPalle,
        "color": (255,255,255),
        "dimension":15,
        "sound":"drip.mp3",
        "Dex":"Chi la usa lancia un raggio potentissimo che lo costringe a riposarsi al prossimo turno"
    },
    "INVESTIRE": {
        "type": "malvaggio",
        "MoveType": "Fisica",
        "BasePower": 250,
        "precisione": 85,
        "Scripts": [AfterSkipTurn],
        "target": "enemy",
        "sound":"drip.mp3",
        "Dex":"Chi lo usa investe l'avversario, ma dopo deve riposare"
    },
    "sanguisuga": {
        "type": "insetto",
        "MoveType": "Fisica",
        "BasePower": 55,
        "precisione": 95,
        "ScriptDmage": [AssorbiVita],
        "target": "enemy",
        "Dex":"Chi la usa succhia il sangue all'aversario curandosi"
    },
    "ronzio rompi palle": {
        "type": "insetto",
        "MoveType": "State",
        "Stat": [{"stats": ["ELUSIONE"], "Power": 0.35, "Target":"self"}],
        "precisione": 95,
        "target": "self",
        "animation": State,
        "sound":"pew.mp3",
        "Dex":"Chi la usa fa rumori fastidiosi che aumentano la propria illusione"
    },
    "Ctrl+C Ctrl+V": {
        "type": "informatico",
        "MoveType": "State",
        "Stat": [{"stats": ["ELUSIONE"], "Power": 0.45, "Target":"self"}],
        "precisione": 100,
        "target": "self",
        "animation": State,
        "sound":"pew.mp3",
        "Dex":"Chi la usa fa copia incolla su se stesso aumentando la propria illusione"
    },
    "inquinamento": {
        "type": "plastica",
        "MoveType": "Fisica",
        "BasePower": 65,
        "target": "enemy",
        "animation": Brilla,
        "color": (100,100,100,85),
        "FlitchChance":5,
        "Scripts": [Flitch],
        "Scripts":[POI],
        "POIChance":5,
        "Dex":"Ha una piccola possibilita di avvelenare o far tentennare l'avversario"
    },
    "Dragoartigli": {
        "type": "drago",
        "MoveType": "Fisica",
        "BasePower": 80,
        "precisione": 90,
        "target": "enemy",
        "FlitchChance":5,
        "Scripts": [Flitch],
        "Dex":"Ha una piccola possibilita di far tentennare l'avversario"
    },
    "Erba schiaffo": {
        "type": "erba",
        "MoveType": "Fisica",
        "BasePower": 55,
        "precisione": 100,
        "target": "enemy"
    },
    "Radice schiaffo": {
        "type": "erba",
        "MoveType": "Fisica",
        "BasePower": 110,
        "precisione": 100,
        "target": "enemy"
    },
    "taskkill": {
        "type": "informatico",
        "MoveType": "Magic",
        "BasePower": 80,
        "precisione": 90,
        "target": "enemy",
        "FlitchChance":8,
        "Scripts": [Flitch],
        "Dex":"Può far tentennare l'avversario"
    },
    "Pistolacqua": {
        "type": "acqua",
        "MoveType": "Magic",
        "BasePower": 40,
        "precisione": 100,
        "target": "enemy",
        "animation": LanciaPalle,
        "color": (9,200,255),
        "dimension":20
    },
    "Geloraggio": {
        "type": "ghiaccio",
        "MoveType": "Magic",
        "BasePower": 80,
        "precisione": 95,
        "target": "enemy",
        "animation": LanciaPalle,
        "color": (100,255,255),
        "dimension":15
    },
    "rickroll": {
        "type": "meme",
        "MoveType": "Fisica",
        "BasePower": 60,
        "precisione": 95,
        "target": "enemy",
        "sound":"rick.mp3",
        "FlitchChance":8,
        "Scripts": [Flitch],
        "Dex":"può far tentennare l'aversario"
                },
    "sparo": {
        "type": "pistola",
        "MoveType": "Fisica",
        "BasePower": 120,
        "precisione": 50,
        "target": "enemy",
        "animation": LanciaPalle,
        "color": (0,0,0),
        "dimension":30,
        "sound":"gun.mp3",
        "FlitchChance":8,
        "Scripts": [Flitch],
        "Dex":"Chi la usa SPARA l'avversario con una piccola possibilità di farlo tentennare"
    },
    "ballo": {
        "type": "meme",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT", "DIF","VEL"], "Power": 0.35, "Target":"self"}],
        "precisione": 80,
        "target": "self",
        "animation": State,
        "sound":"drip.mp3",
        "Dex":"Chi la usa fa un piccolo ballo che aumenta Attacco, Difesa e velocità"
    },
    "IMPOSTOR": {
        "type": "meme",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT"], "Power": 0.6, "Target":"self"},{"stats": ["DIF"], "Power": -0.35, "Target":"self"}],
        "target": "self",
        "animation": State,
        "sound":"sus.mp3",
        "Dex":"Chi lo usa è molto SUS diminuendo la difesa ma aumentando di molto l'attacco"
    },
    "Machine Learning": {
        "type": "AI",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT","MAGIC","DIF","FUN","VEL"], "Power": 0.5, "Target":"self"}],
        "precisione": 100,
        "Scripts": [AfterSkipTurn],
        "target": "self",
        "animation": State,
        "Dex":"Chi la usa si allena a diventare più intelligente aumentando tutte le statistiche, ma il turno dopo deve riposare"
    },
    "VODKA": {
        "type": "veleno",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT","MAGIC","DIF","FUN","VEL"], "Power": 0.35, "Target":"self"}],
        "precisione": 100,
        "Scripts": [DRG],
        "DRGChance":100,
        "target": "self",
        "animation": State,
        "Dex":"Chi la usa ottiene lo sato DRG ma aumenta tutte le statistiche"
    },
    "rugito": {
        "type": "normale",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT"], "Power": -0.25, "Target":"enemy"}],
        "precisione": 100,
        "target": "enemy",
        "animation": State,
        "sound":"roar.mp3",
        "Dex":"Chi lo usa diminuise l'attacco avversario"
    },
    "Fissare": {
        "type": "normale",
        "MoveType": "State",
        "Stat": [{"stats": ["PRECISIONE"], "Power": 0.4, "Target":"self"},{"stats": ["DIF"], "Power": -0.15, "Target":"enemy"}],
        "precisione": 100,
        "target": "self",
        "animation": State,
        "sound":"pew.mp3",
        "Dex":"Chi la usa aumenta la propria precisione e diminuisce la difesa avversaria"
    },
    "carineria": {
        "type": "cute",
        "MoveType": "Fisica",
        "BasePower": 80,
        "Stat": [{"stats": ["DIF"], "Power": -0.1, "Target":"self", "probabilità":35}],
        "precisione": 90,
        "target": "enemy",
        "Dex":"Può ridurre la propria difesa"
    }
}