import pygame
import random
import ctypes
import Files.scripts.functions as F
import Files.scripts.assets as assets
import Files.scripts.dialogue as dialog
from Files.scripts.Data.Moves import MOVES
import Files.scripts.pygameEventCycles as Cycles
from Files.scripts.Data.Battlers import BattlersType
from Files.scripts.Data.nature import NATURE
from Files.scripts.Data.types import types

score = 0

class Battlers:
    def __init__(self, type, level, isEnemy = False):
        self.type = type
        self.IV = {"HP":random.randint(0,31), "ATT":random.randint(0,31),"MAGIC":random.randint(0,31), 
                   "DIF":random.randint(0,31), "FUN":random.randint(0,31),"VEL":random.randint(0,31)}
        self.level = level
        self.modificator = {"ATT":0,"MAGIC":0,"DIF":0, "FUN":0,"VEL":0, "PRECISIONE": 1, "ELUSIONE":1}
        self.EVS = {"HP":0, "ATT":0,"MAGIC":0,"DIF":0, "FUN":0,"VEL":0}
        self.natura = random.choice(list(NATURE.keys()))
        MAXHP = self.Stat_Calculate()["HP"]
        self.HP = MAXHP
        self.maxHP = MAXHP
        self.EXP = 0
        self.riposo = False
        self.moves = BattlersType[self.type]["moves"]["start"]
        self.gender = random.choice(["♀","♂"])
        self.isEnemy = isEnemy
        
        
    
    def Stat_Calculate(self):
        Stat_Calculated = {}
        for stat in Stats:
            ThiseBaseStat = BattlersType[self.type]["BaseStat"][stat] 
            if self.EVS[stat] != 0:
                EVS = (self.EVS[stat] / 4)
            else:
                EVS = 0
            if stat == "HP":
                ThiseStat = round((2 * ThiseBaseStat + self.IV[stat] + EVS * self.level)  / 100) + self.level + 10
            else:
                ThiseStat = max(round((2 * ThiseBaseStat + self.IV[stat] + EVS * self.level)  / 100 + self.modificator[stat]) + 5, 1)
            Stat_Calculated[stat] = ThiseStat
        for stat, molt in NATURE[self.natura].items():
            Stat_Calculated[stat] *= molt
        return Stat_Calculated


    def Damage_Calculate(self, move, enemy):
        if MOVES[move]["MoveType"] == "Fisica":
            Attacco = self.Stat_Calculate()["ATT"]
        else:
            Attacco = self.Stat_Calculate()["MAGIC"]
        DifesaAvversaria = enemy.Stat_Calculate()["DIF"]
        damage = ((((self.level * 2 / 5) + 2) * Attacco * MOVES[move]["BasePower"] / DifesaAvversaria) / 50) + 2
        if random.random() < 0.05:
            damage *= 2 
            Text = dialog.dialoge("Brutto Colpo!!")
            Text.update(assets.screen)
        Roll = random.uniform(-0.05,0.05)
        damage *= (1 + Roll)  
        TypeBust = 1
        for EnemyType in BattlersType[enemy.type]["types"]:
            if MOVES[move]["type"] in types[EnemyType]:
                TypeBust *= types[EnemyType][MOVES[move]["type"]]
        damage *= TypeBust
        if TypeBust > 1:
            Text = dialog.dialoge("è super efficace!!")
            Text.update(assets.screen)
        elif TypeBust < 1:
            Text = dialog.dialoge("non è molto efficace")
            Text.update(assets.screen)
        if MOVES[move]["type"] in BattlersType[self.type]["types"]:
            damage *= 1.5
        damage = round(damage)
        return damage
    
    def useMove(self, move, enemy):
        if "precisione" in MOVES[move]:
            if MOVES[move]["target"] == "enemy":
                chance = MOVES[move]["precisione"] / 100 * self.modificator["PRECISIONE"] / enemy.modificator["ELUSIONE"]
            else:
                chance = MOVES[move]["precisione"] / 100
        else:
            chance = 1
        if random.random() < chance:
            if "Stat" in MOVES[move]:
                for Modific in MOVES[move]["Stat"]:
                    if "probabilità" in Modific:
                        if random.random() > Modific["probabilità"] / 100:
                            break
                    if Modific["Power"] > 0:
                        AorD = " aumenta!!"
                    else:
                        AorD =  " diminuisce!!"
                    ElencoStat = ""
                    for i, stat in enumerate(Modific["stats"]):
                        ElencoStat += stat
                        if i == len(Modific["stats"]) - 2:
                            ElencoStat += " e "
                        elif i == len(Modific["stats"]) - 1:
                            break
                        else:
                            ElencoStat += ", "
                    if Modific["Target"] == "self":
                        for stat in Modific["stats"]:
                            if stat == "PRECISIONE" or stat == "ELUSIONE":
                                self.modificator[stat] +=  Modific["Power"]
                            else:
                                self.modificator[stat] += self.Stat_Calculate()["FUN"] * random.uniform(0.5,1.3) * Modific["Power"]
                        Text = dialog.dialoge(ElencoStat+" di "+self.type+ AorD)
                    elif Modific["Target"] == "enemy":
                        for stat in Modific["stats"]:
                            if stat == "PRECISIONE" or stat == "ELUSIONE":
                                 enemy.modificator[stat] += Modific["Power"]
                            else:
                                enemy.modificator[stat] += enemy.Stat_Calculate()["FUN"] * random.uniform(0.5,1.3) * Modific["Power"]
                        Text = dialog.dialoge(ElencoStat+" di "+enemy.type+ AorD)
                    Text.update(assets.screen)
            if "Scripts" in MOVES[move]:
                for script in MOVES[move]["Scripts"]:
                    script(assets.screen, self)
            if  MOVES[move]["MoveType"] != "State":
                Damage = self.Damage_Calculate(move, enemy)
                enemy.HP -= Damage
                if "ScriptDmage" in MOVES[move]:
                    for i in MOVES[move]["ScriptDmage"]:
                        i(assets.screen, Damage, self)
        else:
            Text = dialog.dialoge("Ma fallisce")
            Text.update(assets.screen)

    def drawStateBar(self, screen, isEnemy):
        Width, Height = assets.ScreenDimension
        scale = Height / 8
        scaleX = scale * 3
        StateBar = pygame.surface.Surface((scaleX, scale))
        StateBar.fill((200,200,200))
        font = pygame.font.SysFont(None, round(scale/3))
        Name = font.render(self.type+" L"+str(self.level), True, (0,0,0))
        StateBar.blit(Name, (5,5))
        LifeBarW = scaleX / 1.5
        LifeBarH = scale / 5
        pygame.draw.rect(StateBar, (0,0,0), (scaleX/2-LifeBarW/2, scale/2-LifeBarH/2, LifeBarW, LifeBarH))
        if self.HP < self.maxHP / 4:
            lifeColor = (255,0,0)
        elif self.HP < self.maxHP / 2:
            lifeColor = (255,255,0)
        else:
            lifeColor = (0,255,0)
        HpBarW = (LifeBarW / self.maxHP) * self.HP
        pygame.draw.rect(StateBar, lifeColor, (scaleX/2-LifeBarW/2, scale/2-LifeBarH/2, HpBarW, LifeBarH))
        if not isEnemy:
            EXPbarW = scaleX * 0.8
            EXPbarH = scale/12
            pygame.draw.rect(StateBar, (0,0,0), (scaleX/2 - EXPbarW/1.7, scale/4*3.5-EXPbarH/2, EXPbarW, EXPbarH))
            EXPScale = EXPbarW / self.ExpToLevelUp()
            NewEXPbarW = EXPScale * self.EXP
            pygame.draw.rect(StateBar, (0,255,255), (scaleX/2 - EXPbarW/1.7, scale/4*3.5-EXPbarH/2, NewEXPbarW, EXPbarH))
        if isEnemy:
            screen.blit(StateBar, ((Width / 4) - scaleX / 2, (Height / 4) - scale / 2))
        else:
            screen.blit(StateBar, (((Width / 4) * 3) - scaleX / 2, (Height - Height / 3) - scale - Height/40))


    def Draw(self, screen, isEnemy=True):
        Width, Height = assets.ScreenDimension
        if isEnemy:
            scale = round(Height / 3)
            sprite = pygame.transform.scale(BattlersType[self.type]["sprite"], (scale, scale))
            screen.blit(sprite, (((Width / 4) * 3) - scale / 2, (Height / 4) - scale / 2))
        else:
            scale = round(Height / 1.6)
            sprite = pygame.transform.flip(pygame.transform.scale(BattlersType[self.type]["sprite"], (scale, scale)), True, False)
            screen.blit(sprite, ((Width / 4) - scale / 2, (Height - Height / 3) - scale / 1.7))
        self.drawStateBar(screen, isEnemy)

    def ViewInformation(self, screen):
        Page = 0
        viewing = True
        while viewing:
            screen.fill((0,10,50))
            WIDTH, HEIGHT = screen.get_size()
            pokemonSurface = pygame.surface.Surface((WIDTH/4, HEIGHT*0.85))
            pokemonSurface.fill((255,255,255))
            W, H = pokemonSurface.get_size() 
            pygame.draw.rect(pokemonSurface, (220,220,220), (0, (H/2 + W*0.4) - W, W, W))
            sprite = pygame.transform.scale(BattlersType[self.type]["sprite"], (W*0.8, W*0.8))
            pokemonSurface.blit(sprite, (W/2 - W*0.8/2, H/2 - W*0.8/2))
            pygame.draw.rect(pokemonSurface, (150,150,150), (0, H/2 + W*0.4, W, H/8))
            font = pygame.font.SysFont(None, round(H/8))
            Name = font.render(self.type, True, (255,255,255))
            WW, HH = Name.get_size()
            pokemonSurface.blit(Name, (10, (H/2 + W*0.4 + H/16) - HH/2))
            Name = font.render(f"L {self.level}", True, (0,0,0))
            WW, HH = Name.get_size()
            pokemonSurface.blit(Name, (10, (H/2 + W*0.4 + H/5) - HH/2))
            screen.blit(pokemonSurface, (WIDTH/5-W/2, HEIGHT/2-H/2))
            information = pygame.surface.Surface((WIDTH/4 * 2.5, HEIGHT*0.85))
            W, H = information.get_size()
            information.fill((255,255,255))
            Sfont = pygame.font.SysFont(None, round(H/12))
            HH = Sfont.get_height()
            for i, (stat, value) in enumerate(self.Stat_Calculate().items()):
                if stat in NATURE[self.natura]:
                    if NATURE[self.natura][stat] > 1:
                        M = NATURE[self.natura][stat] * 1.4
                        color = (70,min(70 * M, 255),70)
                    else:
                        M = 2 - NATURE[self.natura][stat]
                        M *= 1.4
                        color = (min(70 * M, 255),70, 70)
                else:
                    color = (70,70, 70)
                Text = Sfont.render(f"{stat}: {round(value)}", True, color)
                information.blit(Text, (10, 50*i))
            Nature = font.render(f"Di natura {self.natura}", True, (0,0,0))
            information.blit(Nature, (10, 50*7.5))
            screen.blit(information, (WIDTH-W, HEIGHT/2-H/2))
            for event in pygame.event.get():
                Cycles.BaseCicle(event)
            pygame.display.update()


    def MakeMoveList(self):
        MoveOption = [[],[]]
        for i, move in enumerate(self.moves):
            if i < 2:
                MoveOption[0].append(move)
            else:
                MoveOption[1].append(move)
        Difference = 4 - len(self.moves)
        if Difference > 0:
            for i in range(Difference):
                if i < Difference - 2:
                    MoveOption[0].append("-")
                else:
                    MoveOption[1].append("-")
        return MoveOption
    
    def ExpDropped(self, enemy, screen, num_participants = 1):
        global score
        exp = (BattlersType[enemy.type]["baseEXP"] * enemy.level) / (7 * num_participants)
        self.EXP += exp
        for stat, n in BattlersType[enemy.type]["EVS"].items():
            self.EVS[stat] += n
        EXPtoLevelUp =  self.ExpToLevelUp()
        if self.EXP >= EXPtoLevelUp:
            score += 1
            self.EXP -= EXPtoLevelUp
            self.level += 1
            NewHP = self.Stat_Calculate()["HP"]
            ChngeHP = NewHP - self.maxHP
            self.HP += ChngeHP
            self.maxHP = NewHP
            TEXT = dialog.dialoge(f"{self.type} è salito al livello {self.level}!!")
            TEXT.update(screen)

    def ExpToLevelUp(self):
        level = self.level
        growth_rate = BattlersType[self.type]["growth_rate"]
        if growth_rate == 'Erratic':
            if level <= 50:
                exp = (level ** 3 * (100 - level)) // 50
            elif level <= 68:
                exp = (level ** 3 * (150 - level)) // 100
            elif level <= 98:
                exp = (level ** 3 * ((1911 - 10 * level) // 3)) // 500
            else:
                exp = (level ** 3 * (160 - level)) // 100
        elif growth_rate == 'Fast':
            exp = (4 * level ** 3) // 5
        elif growth_rate == 'Medium Fast':
            exp = level ** 3
        elif growth_rate == 'Medium Slow':
            exp = int(1.2 * level ** 3 - 15 * level ** 2 + 100 * level - 140)
        elif growth_rate == 'Slow':
            exp = (5 * level ** 3) // 4
        elif growth_rate == 'Fluctuating':
            if level <= 15:
                exp = level ** 3 * ((level + 1) // 3 + 24) // 50
            elif level <= 36:
                exp = level ** 3 * (level + 14) // 50
            else:
                exp = level ** 3 * (level // 2 + 32) // 50        
        return exp

Stats = ["HP","ATT","MAGIC","DIF","FUN","VEL"]

squadra = [Battlers(random.choice(list(BattlersType.keys())), 5)]

Gino1 = squadra[0]


def Buy():
    global squadra
    if len(squadra) < 6:
        levels = []
        for battlers in squadra:
            levels.append(battlers.level)
        LevelBase =  sum(levels) / len(levels)
        squadra.append(Battlers(random.choice(list(BattlersType.keys())), random.randint(round(LevelBase * 0.8), round(LevelBase * 1.2))))
    else:
        ctypes.windll.user32.MessageBoxW(0, 'Hai la squadra piena', 'Lolo', 0x10)

Level = 2

def RandomizeEnemy():
    return Battlers(random.choice(list(BattlersType.keys())), random.randint(round(Level * 0.7), round(Level * 1.3)), True)

Gino2 = RandomizeEnemy()

battleAction = [["lotta", "borsa"],["Battlers", "negozio"]]

CurrentBattleAction = battleAction

def DrawBattleSelection(screen):
    Gino1.ViewInformation(assets.screen)
    Width, Height = assets.ScreenDimension
    scale = Height / 3
    scaleX = scale * 2
    surface = pygame.surface.Surface((scaleX, scale))
    surface.fill((200, 200, 200))
    pygame.draw.rect(surface, (255, 255, 255), (scaleX / 2 - (scaleX * 0.9) / 2, scale / 2 - (scale * 0.88) / 2, scaleX * 0.9, scale * 0.88))
    font = pygame.font.SysFont(None, round(Height / 17))
    for y, yList in enumerate(CurrentBattleAction):
        for x, action in enumerate(yList):
            ActionText = font.render(action, False, (0, 0, 0))
            W, H = ActionText.get_size()
            text_x = (scaleX / 4) * (x * 2 + 1) - W / 2
            text_y = (scale / 4) * (y * 1.5 + 1) - H / 2
            surface.blit(ActionText, (text_x, text_y))
            if assets.BattleMenuSelectedX == x and assets.BattleMenuSelectedY == y:
                arrow = pygame.transform.scale(assets.arrow, (H, H))
                arrow_x = text_x - H  # Posiziona la freccia alla sinistra del testo
                arrow_y = text_y
                surface.blit(arrow, (arrow_x, arrow_y))
    screen.blit(surface, (Width - scaleX, Height - scale))

def EndTurnChecks(screen):
    global Gino2, Level, score
    if Gino2.HP < 1:
        Text = dialog.dialoge(Gino2.type + " non ha più energie")
        Text.update(screen)
        Gino1.ExpDropped(Gino2, screen)
        Gino2 = RandomizeEnemy()
        Level += random.choice([0,0,0,1,1,2,-1])
        score += 1
        return False
    elif Gino1.HP < 1:
        Text = dialog.dialoge(Gino1.type + " non ha più energie")
        Text.update(screen)
        print(score)
        quit()
    return True

def PlayerTurn(screen, playerMove):
    if Gino1.riposo:
        Gino1.riposo = False
        Text = dialog.dialoge(Gino1.type + " deve riposarsi")
        Text.update(screen)
    else:
        Text = dialog.dialoge(Gino1.type + " usa " + playerMove + "!!")
        Text.update(screen)
        Gino1.useMove(playerMove, Gino2)
        Gino2.drawStateBar(screen, True)

def EnemyTurn(screen, a):
    if Gino2.riposo:
        Gino2.riposo = False
        Text = dialog.dialoge(Gino2.type + " deve riposarsi")
        Text.update(screen)
    else:
        move = random.choice(Gino2.moves)
        Text = dialog.dialoge(Gino2.type + " usa " + move + "!!")
        Text.update(screen)
        Gino2.useMove(move, Gino1)
        Gino1.drawStateBar(screen, False)



def Turn(screen, playerMove):
    TurnOrder = [PlayerTurn, EnemyTurn]
    if Gino1.Stat_Calculate()["VEL"] > Gino2.Stat_Calculate()["VEL"]:
        TurnOrder = [PlayerTurn, EnemyTurn]
    elif Gino1.Stat_Calculate()["VEL"] < Gino2.Stat_Calculate()["VEL"]:
        TurnOrder = [EnemyTurn, PlayerTurn]
    else:
        random.shuffle(TurnOrder)
    TurnOrder[0](screen, playerMove)
    if EndTurnChecks(screen):
        TurnOrder[1](screen, playerMove)
        EndTurnChecks(screen)


def ViewTeam(screen):
    rects = []
    for i in range(len(squadra)):
        rects.append(pygame.rect.Rect(0,0,225,225))
    while True:
        screen.fill((255, 255, 255))
        screen_width, screen_height = screen.get_size()
        grid_width = screen_width // 3 
        grid_height = screen_height // 2
        horizontal_space = (grid_width * 0.1) // (3 - 1)
        vertical_space = -80 // (2 - 1)
        itemN = 0
        for row in range(2):
            for col in range(3):
                if len(squadra) > itemN:
                    x = col * (grid_width + horizontal_space)
                    y = row * (grid_height + vertical_space)
                    screen.blit(pygame.transform.scale(BattlersType[squadra[itemN].type]["sprite"], (225,225)), (x, y)) 
                    rects[itemN].x, rects[itemN].y = x,y 
                    itemN += 1
        for i, rect in enumerate(rects):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_x, mouse_y):
                dimension = screen_height / 6
                description_box = pygame.Rect(mouse_x+10, mouse_y+10, dimension*1.7, dimension)
                pygame.draw.rect(screen, (0, 0, 0), description_box) 
                font = pygame.font.SysFont(None, int(dimension / 4.5))
                try:
                    types = ""
                    for type in BattlersType[squadra[i].type]["types"]:
                        types += type
                        types += " "
                    description_text = f"{squadra[i].type}: L: {squadra[i].level} type: {types}"
                    description_box = pygame.Rect(mouse_x+15, mouse_y+15, dimension*1.65, dimension*0.95)
                except IndexError:
                    pass
                F.draw_text_within(screen, description_text, description_box, font, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            Cycles.BaseCicle(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            