import pygame
import random
import ctypes
from Files.scripts.Data import world
import Files.scripts.functions as F
import Files.scripts.assets as assets
import Files.scripts.dialogue as dialog
from Files.scripts.BattlersClass import Battlers
import Files.scripts.pygameEventCycles as Cycles
import Files.scripts.BattlersSpawnChance as E
import Files.scripts.AI as AI
from Files.scripts.Data.Battlers import BattlersType
from Files.scripts.animation.DeathAnimation import Death
from Files.scripts.Data.Moves import MOVES

assets.World = random.choice(list(world.World.keys()))

Stats = ["HP","ATT","MAGIC","DIF","FUN","VEL"]

squadra = [Battlers(random.choice(list(BattlersType.keys())), 5)]

Gino1 = squadra[0]

ToNextWorld = random.randint(5,10)

NTurn = 1

def CuraSquadra():
    for battler in squadra:
        battler.HP = battler.maxHP
        battler.state = None
        battler.modificator = {"ATT":0,"MAGIC":0,"DIF":0, "FUN":0,"VEL":0, "PRECISIONE": 1, "ELUSIONE":1}
        battler.ResetPP()

def Buy():
    global squadra
    if len(squadra) < 6:
        assets.score -= 2
        levels = []
        for battlers in squadra:
            levels.append(battlers.level)
        LevelBase =  sum(levels) / len(levels)
        squadra.append(Battlers(random.choice(E.SpawinList()), random.randint(round(LevelBase * 0.8), round(LevelBase * 1.2))))
    else:
        ctypes.windll.user32.MessageBoxW(0, 'Hai la squadra piena', 'Lolo', 0x10)

Level = 2

def RandomizeEnemy():
    return Battlers(random.choice(E.SpawinList()), random.randint(round(Level * 0.7), round(Level * 1.3)), True)

Gino2 = RandomizeEnemy()

battleAction = [["lotta", "borsa"],["Battlers", "negozio"]]

CurrentBattleAction = battleAction

def DrawBattleSelection(screen):
    action = CurrentBattleAction[assets.BattleMenuSelectedY][assets.BattleMenuSelectedX]
    IsMove = action in MOVES or action == "-"
    Width, Height = assets.ScreenDimension
    scale = Height / 3
    if IsMove:
        scaleX = Width - scale * 2.5
    else:
        scaleX = scale * 2
    surface = pygame.surface.Surface((scaleX, scale))
    surface.fill((200, 200, 200))
    pygame.draw.rect(surface, (255, 255, 255), (scaleX / 2 - (scaleX * 0.85) / 2, scale / 2 - (scale * 0.88) / 2, scaleX * 0.9, scale * 0.88))
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
                if IsMove and action != "-":
                    Move = Gino1.MakeMoveInformaionSurface(screen, action)
                    Move = pygame.transform.scale(Move, (scale * 2.5, scale))
                    screen.blit(Move, (Width-scale * 2.5, Height - scale))
    if IsMove:
        screen.blit(surface, (0, Height - scale))
    else:
        screen.blit(surface, (Width-scaleX, Height - scale))

def EndTurnChecks(screen):
    global Gino2, Gino1, Level,CurrentBattleAction, ToNextWorld, NTurn
    Return = True
    Change = False
    if Gino1.HP < 1:
        Death(screen, Gino1, Gino2, False)
        squadra.remove(Gino1)
        
        if len(squadra) > 0:
            Change = True
            CurrentBattleAction = battleAction
            Return = False
        else:
            print(assets.score)
            End()
            quit()
    if Gino2.HP < 1:
        Death(screen, Gino2, Gino1, True)
        if ToNextWorld <= 0:
            ToNextWorld = random.randint(5,10)
            assets.World = random.choice(list(world.World.keys()))
            CuraSquadra()
        if Return:
            Gino1.ExpDropped(Gino2, screen)
        Gino2 = RandomizeEnemy()
        NTurn = 1
        Level += random.choice([0,0,0,1,1,1,1,2])
        Level = max(1,Level)
        assets.score += 1
        Return = False
        ToNextWorld -= 1
    
    if Change:
        Gino1 = None
        while Gino1 is None:
            ViewTeam(screen, False)
    return Return

def PlayerTurn(screen, playerMove):
    if Gino1.riposo:
        Gino1.riposo = False
        Text = dialog.dialoge(Gino1.type + " deve riposarsi")
        Text.update(screen)
    elif Gino1.flitch:
        Gino1.flitch = False
        Text = dialog.dialoge(Gino1.type + " Ha tentennato")
        Text.update(screen)
    else:
        Gino1.useMove(playerMove, Gino2)
        Gino2.drawStateBar(screen, True)

def EnemyTurn(screen, a):
    if Gino2.riposo:
        Gino2.riposo = False
        Text = dialog.dialoge(Gino2.type + " deve riposarsi")
        Text.update(screen)
    elif Gino2.flitch:
        Gino2.flitch = False
        Text = dialog.dialoge(Gino2.type + " Ha tentennato")
        Text.update(screen)
    else:
        move = AI.AI(Gino2, NTurn, Gino2.AI, Gino1)
        Gino2.useMove(move, Gino1)
        Gino1.drawStateBar(screen, False)



def Turn(screen, playerMove):
    global NTurn
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
    Gino2.StatusCheck()
    Gino1.StatusCheck() 
    NTurn += 1
    EndTurnChecks(screen)
   

def Make_Right_click_window(screen, MousePosition, Position):
    Width, Height = screen.get_size()
    Mx, My = MousePosition
    Rects = {}
    Option = ["informazioni", "cambia", "libera"]
    W, H = Width / 10, (Height / 25) * len(Option) + 5 * (len(Option) - 1)
    font = pygame.font.SysFont(None, round(Height / 30))
    FH = font.get_height()
    Surface = pygame.Surface((W, H))
    Surface.fill((0, 0, 0))
    
    for i, option in enumerate(Option):
        Rects[option] = pygame.rect.Rect(0, (Height / 25 + 5) * i, W, Height / 25)
        ScreenRect = Rects[option].copy()
        ScreenRect.x += Position[0]
        ScreenRect.y += Position[1]
        
        if ScreenRect.collidepoint(Mx, My):
            color = (200, 200, 200)
        else:
            color = (255, 255, 255)
        
        pygame.draw.rect(Surface, color, Rects[option])
        Text = font.render(option, True, (0, 0, 0))
        Surface.blit(Text, (W / 2 - Text.get_width() / 2, (Height / 25 + 5) * i + FH / 4))
        
        Rects[option] = ScreenRect
    
    return Surface, Rects

def ViewTeam(screen, switch = True):
    global Gino1
    rects = []
    RightClick = False
    BattlerRightClicked = None
    RightSurface = None
    RightRect = None
    RightPosition = None
    mouse_x, mouse_y = 0, 0  # Inizializza la posizione del mouse
    
    for i in range(len(squadra)):
        rects.append(pygame.rect.Rect(0, 0, 225, 225))
    
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Aggiorna la posizione del mouse all'inizio del ciclo
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
                    x = col * (grid_width + horizontal_space) + screen_width / 24
                    y = row * (grid_height + vertical_space) + screen_height / 24
                    rects[itemN].x, rects[itemN].y = x, y
                    if squadra[itemN] == Gino1:
                        F.draw_rounded_rect(screen, (240, 240, 240), rects[itemN], 10)
                    screen.blit(pygame.transform.scale(BattlersType[squadra[itemN].type]["sprite"], (225, 225)), (x, y))
                    itemN += 1
        
        if RightClick:
            RightSurface, RightRect = Make_Right_click_window(screen, (mouse_x, mouse_y), RightPosition)
            screen.blit(RightSurface, RightPosition)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            Cycles.BaseCicle(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                Click = False
                if RightClick:
                    for Option, Rect in RightRect.items():
                        if Rect.collidepoint(mouse_x, mouse_y):
                            if event.button == 1:
                                Click = True
                                RightClick = False
                                if Option == "informazioni":
                                    BattlerRightClicked.ViewInformation(screen)
                                elif Option == "cambia":
                                    Gino1 = BattlerRightClicked
                                    if switch:
                                        EnemyTurn(screen,1)
                                        return
                                elif Option == "libera":
                                    if len(squadra) > 1 and BattlerRightClicked != Gino1:
                                        squadra.remove(BattlerRightClicked)                     
                if Click:
                    break
                Click = True
                for i, rect in enumerate(rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        if event.button == 1:
                            squadra[i].ViewInformation(screen)
                        else:
                            Click = False
                            RightClick = True
                            BattlerRightClicked = squadra[i]
                            RightPosition = (mouse_x, mouse_y)
                            RightSurface, RightRect = Make_Right_click_window(screen, (mouse_x, mouse_y), RightPosition)
                if Click:
                    RightClick = False
                
                


def End():
    with open("Files/stats.stt", 'r') as file:
        lines = [line.rstrip('\n') for line in file.readlines()]
    TotalScore = int(lines[0])
    TotalScore += assets.score
    with open("Files/stats.stt", 'w') as file:
        file.write(str(TotalScore))