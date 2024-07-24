import pygame
import random
import Files.scripts.functions as F
import Files.scripts.assets as assets
import Files.scripts.dialogue as dialog
from Files.scripts.Data.nature import NATURE
import Files.scripts.pygameEventCycles as Cycles
from Files.scripts.Data.Moves import MOVES, Defoult
from Files.scripts.Data.Battlers import BattlersType
from Files.scripts.Data.types import types, TypesColor

Stats = ["HP","ATT","MAGIC","DIF","FUN","VEL"]

class Battlers:
    def __init__(self, type, level, isEnemy = False):
        self.type = type
        self.IV = {"HP":random.randint(0,62), "ATT":random.randint(0,62),"MAGIC":random.randint(0,62), 
                   "DIF":random.randint(0,62), "FUN":random.randint(0,62),"VEL":random.randint(0,62)}
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
                ThiseStat = round((2 * ThiseBaseStat + self.IV[stat] + EVS)  / 100 * self.level) + self.level + 10
            else:
                ThiseStat = max(round((2 * ThiseBaseStat + self.IV[stat] + EVS)  / 100 * self.level) + 5 + self.modificator[stat], 1)
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
        if TypeBust == 0:
            Text = dialog.dialoge("Non ha effetto")
            Text.update(assets.screen)
            return 0
        elif TypeBust > 1:
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
            if "animation" in MOVES[move]:
                MOVES[move]["animation"](assets.screen, move, self, enemy, self.isEnemy)
            else:
                Defoult(assets.screen, move, self, enemy, self.isEnemy)
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
            Text = dialog.dialoge(self.type + " usa " + move + "!!")
            Text.update(assets.screen)
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
        MAXPAGE = 2
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
            if Page == 0:
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
                Nature = Sfont.render(f"Di natura {self.natura}", True,( 0,0,0))
                information.blit(Nature, (10, 50*7.5))
                TypeText = "Tipo: "
                for i, type in enumerate(BattlersType[self.type]["types"]):
                    TypeText += type
                    if i+1 < len(BattlersType[self.type]["types"]):
                        TypeText += "/"
                Type = Sfont.render(TypeText, True,(0,0,0))
                information.blit(Type, (10, 50*8.5))
                x = W / 3
                y = H / 25
                pygame.draw.rect(information, (0,0,0), (10, 50*10, x, y))
                if self.HP < self.maxHP / 4:
                    lifeColor = (255,0,0)
                elif self.HP < self.maxHP / 2:
                    lifeColor = (255,255,0)
                else:
                    lifeColor = (0,255,0)
                HpBarW = (x / self.maxHP) * self.HP
                pygame.draw.rect(information, lifeColor, (10, 50*10, HpBarW, y))
                pygame.draw.rect(information, (0,0,0), (10, 50*10.7, x, y/1.7))
                ExpW = (x / self.ExpToLevelUp()) * self.EXP
                pygame.draw.rect(information, (0,255,255), (10, 50*10.7, ExpW, y/1.7))
            elif Page == 1:
                Text = Sfont.render("IV:", True, (0,0,0))
                information.blit(Text, (10, 0))
                MaxLenght = 0
                for i, (stat, value) in enumerate(self.IV.items()):
                    Text = Sfont.render(f"{stat}: {round(value)}", True, (0,0,0))
                    w = Text.get_width()
                    if w > MaxLenght:
                        MaxLenght = w
                    information.blit(Text, (30, 50*(i+1)))
                Text = Sfont.render("EVS:", True, (0,0,0))
                information.blit(Text, (MaxLenght + 50, 0))
                for i, (stat, value) in enumerate(self.EVS.items()):
                    Text = Sfont.render(f"{stat}: {round(value)}", True, (0,0,0))
                    information.blit(Text, (MaxLenght + 80, 50*(i+1)))
                for i, move in enumerate(self.moves):
                    if move != "-":
                        pygame.draw.rect(information, TypesColor[MOVES[move]["type"]], (10, 50 * (i+8), 350, 45))
                        if F.is_color_light(TypesColor[MOVES[move]["type"]]):
                            color = (0,0,0)
                        else:
                            color = (255,255,255)
                        Text = Sfont.render(move, True, color)
                        h = Text.get_height()
                        information.blit(Text, (20, 50 * (i+8) + 45/2-h/2))
            elif Page == 2:
                Rect = pygame.rect.Rect(W*0.05,H*0.05,W*0.9,H*0.9)
                F.draw_text_within(information, BattlersType[self.type]["Dex"], Rect, Sfont, (0,0,0))
            screen.blit(information, (WIDTH-W, HEIGHT/2-H/2))
            for event in pygame.event.get():
                Cycles.BaseCicle(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        viewing = False
                    elif event.key == pygame.K_RIGHT:
                        if Page < MAXPAGE:
                            Page += 1
                    elif event.key == pygame.K_LEFT:
                        if Page > 0:
                            Page -= 1
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
        exp = (BattlersType[enemy.type]["baseEXP"] * enemy.level) / (7 * num_participants)
        self.EXP += exp
        for stat, n in BattlersType[enemy.type]["EVS"].items():
            self.EVS[stat] += n
        EXPtoLevelUp =  self.ExpToLevelUp()
        while self.EXP >= EXPtoLevelUp:
            assets.score += 1
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