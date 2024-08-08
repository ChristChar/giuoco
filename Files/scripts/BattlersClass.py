import pygame
import random
import Files.scripts.functions as F
import Files.scripts.assets as assets
import Files.scripts.dialogue as dialog
from Files.scripts.Data.nature import NATURE, NaturMove
import Files.scripts.pygameEventCycles as Cycles
from Files.scripts.Data.Moves import MOVES, Defoult
from Files.scripts.Data.Battlers import BattlersType
from Files.scripts.Data.types import types, TypesColor
import Files.scripts.Data.status as status

Stats = ["HP","ATT","MAGIC","DIF","FUN","VEL"]

class Battlers:
    def __init__(self, type, level, isEnemy = False):
        self.state = None
        self.type = type
        self.IV = {"HP":random.randint(0,62), "ATT":random.randint(0,62),"MAGIC":random.randint(0,62), 
                   "DIF":random.randint(0,62), "FUN":random.randint(0,62),"VEL":random.randint(0,62)}
        self.level = level
        self.modificator = {"ATT":0,"MAGIC":0,"DIF":0, "FUN":0,"VEL":0, "PRECISIONE": 1, "ELUSIONE":1}
        self.EVS = {"HP":0, "ATT":0,"MAGIC":0,"DIF":0, "FUN":0,"VEL":0}
        self.natura = random.choice(list(NATURE.keys()))
        self.EXP = 0
        self.riposo = False
        self.flitch = False
        self.LearnableMoves = self.Calcolate_learnable_Moves()
        self.moves = random.sample(self.LearnableMoves, min(4, len(self.LearnableMoves)))
        self.gender = random.choice(["♀","♂"])
        self.isEnemy = isEnemy
        MAXHP = self.Stat_Calculate()["HP"]
        self.HP = MAXHP
        self.maxHP = MAXHP
        self.PP = {}
        self.ResetPP()




    def ResetPP(self):
        self.PP = {}
        for move in self.LearnableMoves:
            self.PP[move] = MOVES[move]["PP"]

    def UpdatePP(self):
         # Aggiorna i PP per le mosse attuali
        updated_PP = {}
        for move in self.LearnableMoves:
            if move in self.PP:
                # Mantieni il PP corrente se la mossa esiste già
                updated_PP[move] = self.PP[move]
            else:
                # Aggiungi la nuova mossa con il suo PP iniziale
                updated_PP[move] = MOVES[move]["PP"]
        
        # Aggiorna il dizionario PP della classe
        self.PP = updated_PP

        
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
                ThiseStat = max(round((2 * ThiseBaseStat + self.IV[stat] + EVS)  / 100 * self.level) + 5 , 1)
            Stat_Calculated[stat] = ThiseStat
        for stat, molt in NATURE[self.natura].items():
            Stat_Calculated[stat] *= molt
        if self.state in status.LowerStat:
            for Stat, Low in list(status.LowerStat[self.state].items()):
                Stat_Calculated[Stat] *= Low
        for stat, molt in assets.Stats.items():
            Stat_Calculated[stat] *= molt
        for stat in ["ATT","MAGIC","DIF","FUN","VEL"]:
            Stat_Calculated[stat] += self.modificator[stat]
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
        if move in self.PP:
            self.PP[move] -= 1
        if self.state in status.SkipTurn:
            Resisten = 0
            for type in BattlersType[self.type]["types"]:
                if type in status.ResistanceTypes[self.state]:
                    Resisten += status.ResistanceTypes[self.state][type]
            if random.random() < (status.CureChance[self.state] + Resisten) / 100:
                Text = dialog.dialoge(self.type+" è guarito dalla "+self.state+"!!")
                Text.update(assets.screen)
                self.state = None
            elif random.random() < status.SkipTurn[self.state]["chance"] / 100:
                Text = dialog.dialoge(self.type+status.SkipTurn[self.state]["Text"])
                Text.update(assets.screen)
                return
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
                    script(assets.screen, self, enemy, move)
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
        scale = Height / 7
        scaleX = scale * 3
        StateBar = pygame.surface.Surface((scaleX, scale), pygame.SRCALPHA)
        StateBar.fill((0,0,0,0))
        F.draw_rounded_rect(StateBar, (200,200,200), (0,0,scaleX,scale),10)
        font = pygame.font.SysFont(None, round(scale/3))
        Name = font.render(self.type+" L"+str(self.level), True, (0,0,0))
        NameLenght, NameHeight = Name.get_size()
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
        if self.state is not None:
            Y = NameHeight
            X = Y*1.2
            Status = pygame.surface.Surface((X,Y))
            Status.fill(status.Color[self.state])
            Font = pygame.font.SysFont(None, round(Y*0.9))
            if F.is_color_light(status.Color[self.state]):
                color = (0,0,0)
            else:
                color = (255,255,255)
            Text = Font.render(self.state, True, color)
            x, y = Text.get_size()
            Status.blit(Text, (X/2-x/2,Y/2-y/2))
            StateBar.blit(Status, (20+NameLenght,5))
        if not isEnemy:
            EXPbarW = scaleX * 0.8
            EXPbarH = scale/12
            pygame.draw.rect(StateBar, (0,0,0), (scaleX/2 - EXPbarW/1.7, scale/4*3.5-EXPbarH/2, EXPbarW, EXPbarH))
            EXPScale = EXPbarW / self.ExpToLevelUp()
            NewEXPbarW = EXPScale * self.EXP
            pygame.draw.rect(StateBar, (0,255,255), (scaleX/2 - EXPbarW/1.7, scale/4*3.5-EXPbarH/2, NewEXPbarW, EXPbarH))
        if isEnemy:
            screen.blit(StateBar, ((Width / 4) - scaleX / 1.5, (Height / 4) - scale / 1.5))
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

    def MakeMoveInformaionSurface(self,screen, move):
        WIDTH, HEIGHT = screen.get_size()
        W, H = WIDTH / 3.5, HEIGHT * 0.2
        COLOR_MOVE_TYPE = {"Fisica":(255,0,0),"Magic":(50,0,255),"State":(100,100,100)}
        MoveSurface = pygame.Surface((W, H))
        MoveData = MOVES[move]
        MoveSurface.fill(TypesColor[MoveData["type"]])
        TextColor = (0, 0, 0) if F.is_color_light(TypesColor[MoveData["type"]]) else (255, 255, 255)

        # Calcola dimensioni del font per il titolo
        title_font_size = round(W / 7)
        TitleFont = pygame.font.SysFont(None, title_font_size)
        Title = TitleFont.render(move, True, TextColor)
        TW, TH = Title.get_size()
        pygame.draw.rect(MoveSurface, COLOR_MOVE_TYPE[MoveData["MoveType"]], (TW+15, 5+TH*0.15, TH*0.7,TH*0.6))
        TitleRect = Title.get_rect(topleft=(5, 5))

        # Calcola dimensioni del font per le informazioni
        info_font_size = round(W / 15)
        InformationFont = pygame.font.SysFont(None, info_font_size)

        # Calcola dimensioni del font per la descrizione
        info_font_size = round(W / 20)
        DexFont = pygame.font.SysFont(None, info_font_size)

        #PP
        PPText = f"PP: {self.PP[move]}"
        PP = InformationFont.render(PPText, True, TextColor)
        PPRect = PP.get_rect(topleft=(5, TitleRect.bottom + 5))
        
        # Base Power
        power = MoveData.get("BasePower", "--")
        PowerText = f"Power: {power}"
        Power = InformationFont.render(PowerText, True, TextColor)
        PowerRect = Power.get_rect(topleft=(5, PPRect.bottom + 5))

        # Precisione
        precisione = MoveData.get("precisione", "--")
        PrecisionText = f"Precisione: {precisione}"
        Precision = InformationFont.render(PrecisionText, True, TextColor)
        PrecisionRect = Precision.get_rect(topleft=(5, PowerRect.bottom + 5))

        #Dex
        if "Dex" in MoveData:
            Rect = pygame.rect.Rect(5,PrecisionRect.bottom + 6, W-10, H-10)
            F.draw_text_within(MoveSurface, MoveData["Dex"], Rect, DexFont, TextColor)

        # Aggiunge gli elementi alla superficie
        MoveSurface.blit(Title, TitleRect)
        MoveSurface.blit(PP, PPRect)
        MoveSurface.blit(Power, PowerRect)
        MoveSurface.blit(Precision, PrecisionRect)

        return MoveSurface

    def GestisciMosse(self,screen):
        MoveSurface = None
        self.Calcolate_New_learnable_move()
        TheOtherMoves = F.Sottrai_liste(self.LearnableMoves, self.moves)
        while True:
            MoveRects = []
            screen.fill((0,10,50))
            WIDTH, HEIGHT = screen.get_size()
            W, H = WIDTH/3, HEIGHT*0.85
            CurrentMove =  pygame.surface.Surface((W, H))
            CurrentMove.fill((255,255,255))
            Sfont = pygame.font.SysFont(None, round(H/12))
            for i, move in enumerate(self.moves):
                Rect = pygame.rect.Rect((10, 50 * (i+1), 350, 45))
                pygame.draw.rect(CurrentMove, TypesColor[MOVES[move]["type"]], Rect)
                if F.is_color_light(TypesColor[MOVES[move]["type"]]):
                    color = (0,0,0)
                else:
                    color = (255,255,255)
                Text = Sfont.render(move, True, color)
                h = Text.get_height()
                CurrentMove.blit(Text, (20, 50 * (i+1) + 45/2-h/2))
                Rect.x += WIDTH/5-W/2
                Rect.y += HEIGHT/2-H/2
                MoveRects.append(Rect)
            screen.blit(CurrentMove, (WIDTH/5-W/2, HEIGHT/2-H/2))
            information = pygame.surface.Surface((WIDTH/4 * 2.5, HEIGHT*0.85))
            W, H = information.get_size()
            information.fill((255,255,255))
            otherMoveRects = []
            for i, move in enumerate(TheOtherMoves):    
                if F.is_color_light(TypesColor[MOVES[move]["type"]]):
                    color = (0,0,0)
                else:
                    color = (255,255,255)
                Text = Sfont.render(move, True, color)
                h = Text.get_height()
                if i == 0:
                    Rect = pygame.rect.Rect((10, 50, 350, 45))
                    TextPosition = (20, 50)
                elif (i+1) % 2 == 0:
                    Rect = pygame.rect.Rect((380, 50 * (1+round(i/2.1)), 350, 45))
                    TextPosition = (390, 50 * (1+round(i/2.1)))
                else:
                    Rect = pygame.rect.Rect((10, 50 * (1+round(i/2.1)), 350, 45))
                    TextPosition = (20, 50 * (1+round(i/2.1)))
                pygame.draw.rect(information, TypesColor[MOVES[move]["type"]], Rect)  
                information.blit(Text, TextPosition)
                Rect.x += WIDTH-W
                Rect.y += HEIGHT/2-H/2
                otherMoveRects.append(Rect)
            screen.blit(information, (WIDTH-W, HEIGHT/2-H/2))
            if MoveSurface is not None:
                MH = MoveSurface.get_height()
                screen.blit(MoveSurface, (0,HEIGHT-MH))
            pygame.display.update()
            for event in pygame.event.get():
                Cycles.BaseCicle(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    HaCliccato = True
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for i, rect in enumerate(MoveRects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            HaCliccato = False
                            if event.button == 1:  # Bottone sinistro del mouse
                                MoveSurface = self.MakeMoveInformaionSurface(screen, self.moves[i])
                            elif event.button == 3:  # Bottone destro del mouse
                                TheOtherMoves.append(self.moves.pop(i))
                    for i, rect in enumerate(otherMoveRects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            HaCliccato = False
                            if event.button == 1:  # Bottone sinistro del mouse
                                MoveSurface = self.MakeMoveInformaionSurface(screen, TheOtherMoves[i])
                            elif event.button == 3:  # Bottone destro del mouse
                                if len(self.moves) < 4:
                                    self.moves.append(TheOtherMoves.pop(i))
                    if HaCliccato:
                        MoveSurface = None
        
                        
            

    def ViewInformation(self, screen):
        Page = 0
        MAXPAGE = 2
        viewing = True
        MoveSurface = None
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
            if self.state is not None:
                Y = HH / 1.5
                X = Y*1.2
                Status = pygame.surface.Surface((X,Y))
                Status.fill(status.Color[self.state])
                Font = pygame.font.SysFont(None, round(Y*0.8))
                if F.is_color_light(status.Color[self.state]):
                    color = (0,0,0)
                else:
                    color = (255,255,255)
                Text = Font.render(self.state, True, color)
                x, y = Text.get_size()
                Status.blit(Text, (X/2-x/2,Y/2-y/2))
                pokemonSurface.blit(Status, (40+WW,(H/2 + W*0.4 + H/5) - Y/2))
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
                MoveRects = []
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
                    Rect = pygame.rect.Rect((10, 50 * (i+8), 350, 45))
                    pygame.draw.rect(information, TypesColor[MOVES[move]["type"]], Rect)
                    if F.is_color_light(TypesColor[MOVES[move]["type"]]):
                        color = (0,0,0)
                    else:
                        color = (255,255,255)
                    Text = Sfont.render(move, True, color)
                    h = Text.get_height()
                    information.blit(Text, (20, 50 * (i+8) + 45/2-h/2))
                    Rect.x += WIDTH-W
                    Rect.y += HEIGHT/2-H/2
                    MoveRects.append(Rect)
                Rect = pygame.rect.Rect((10, 50 * (i+9), 350, 45))
                pygame.draw.rect(information, (200,200,200), Rect)
                Text = Sfont.render("Gestisci Mosse", True, (0,0,0))
                h = Text.get_height()
                information.blit(Text, (20, 50 * (i+9) + 45/2-h/2))
                Rect.x += WIDTH-W
                Rect.y += HEIGHT/2-H/2
                MoveRects.append(Rect)
                if MoveSurface is not None:
                    MH = MoveSurface.get_height()
                    screen.blit(MoveSurface, (0,HEIGHT-MH))
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if Page == 1:
                        if event.button == 1:
                            HaCliccato = True
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            for i, rect in enumerate(MoveRects):
                                if rect.collidepoint(mouse_x, mouse_y):
                                    if i == len(self.moves):
                                        self.GestisciMosse(screen)
                                    else:
                                        HaCliccato = False
                                        MoveSurface = self.MakeMoveInformaionSurface(screen, self.moves[i])
                            if HaCliccato:
                                MoveSurface = None
                                    
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
        exp = (BattlersType[enemy.type]["baseEXP"] * enemy.level) / (5.5 * num_participants)
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
            if str(self.level) in BattlersType[self.type]["moves"]:
                for move in BattlersType[self.type]["moves"][str(self.level)]:
                    TEXT = dialog.dialoge(f"{self.type} ha imparato una nuova mossa: {move}!!")
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
    
    def StatusCheck(self):
        if self.state in status.Damage:
            Resisten = 0
            for type in BattlersType[self.type]["types"]:
                if type in status.ResistanceTypes[self.state]:
                    Resisten += status.ResistanceTypes[self.state][type]
            if random.random() < (status.CureChance[self.state] + Resisten) / 100:
                Text = dialog.dialoge(self.type+" è guarito dalla "+self.state+"!!")
                Text.update(assets.screen)
                self.state = None
            else:
                Text = dialog.dialoge(self.type+status.Damage[self.state]["Text"])
                Text.update(assets.screen)
                Percet = self.maxHP / 100 * status.Damage[self.state]["%"]
                self.HP -= Percet

    def Calcolate_learnable_Moves(self):
        self.LearnableMoves = BattlersType[self.type]["moves"]["start"].copy()
        if self.natura in NaturMove:
            self.LearnableMoves.extend(NaturMove[self.natura])
        for i in range(1, self.level + 1):
            if str(i) in BattlersType[self.type]["moves"]:
                self.LearnableMoves.extend(BattlersType[self.type]["moves"][str(i)])
        return list(dict.fromkeys(self.LearnableMoves))


    def Calcolate_New_learnable_move(self):
        self.LearnableMoves.extend(self.Calcolate_learnable_Moves())
        #self.LearnableMoves.extend(["azione","Assorbi Luce","Chilling","Lanciare la pizza"])
        self.LearnableMoves = list(dict.fromkeys(self.LearnableMoves))
        self.UpdatePP()