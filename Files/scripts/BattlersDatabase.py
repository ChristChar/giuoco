from itertools import chain
import pygame
import random
import ctypes
import Files.scripts.functions as F
import Files.scripts.assets as assets
import Files.scripts.dialogue as dialog
from Files.scripts.Data.Moves import Defoult
from Files.scripts.BattlersClass import Battlers
import Files.scripts.pygameEventCycles as Cycles
from Files.scripts.Data.Battlers import BattlersType

Stats = ["HP","ATT","MAGIC","DIF","FUN","VEL"]

squadra = [Battlers(random.choice(assets.spawn_list), 5)]

Gino1 = squadra[0]


def Buy():
    global squadra
    if len(squadra) < 6:
        assets.score -= 2
        levels = []
        for battlers in squadra:
            levels.append(battlers.level)
        LevelBase =  sum(levels) / len(levels)
        squadra.append(Battlers(random.choice(assets.spawn_list), random.randint(round(LevelBase * 0.8), round(LevelBase * 1.2))))
    else:
        ctypes.windll.user32.MessageBoxW(0, 'Hai la squadra piena', 'Lolo', 0x10)

Level = 2

def RandomizeEnemy():
    return Battlers(random.choice(assets.spawn_list), random.randint(round(Level * 0.7), round(Level * 1.3)), True)

Gino2 = RandomizeEnemy()

battleAction = [["lotta", "borsa"],["Battlers", "negozio"]]

CurrentBattleAction = battleAction

def DrawBattleSelection(screen):
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
    global Gino2, Gino1, Level,CurrentBattleAction
    Return = True
    Change = False
    if Gino1.HP < 1:
        Text = dialog.dialoge(Gino1.type + " non ha più energie")
        Text.update(screen)
        squadra.remove(Gino1)
        del Gino1
        if len(squadra) > 0:
            Change = True
            CurrentBattleAction = battleAction
            Return = False
        else:
            print(assets.score)
            End()
            quit()
    if Gino2.HP < 1:
        Text = dialog.dialoge(Gino2.type + " non ha più energie")
        Text.update(screen)
        if Return:
            Gino1.ExpDropped(Gino2, screen)
        Gino2 = RandomizeEnemy()
        Level += random.choice([0,0,0,0,0,1,1,1,2,-1,-1])
        Level = max(1,Level)
        assets.score += 1
        Return = False
    if Change:
         while True:
            ViewTeam(screen)
            try:
                Gino1
                break
            except:
                pass
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
        move = random.choice(Gino2.moves)
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
    Gino2.StatusCheck()
    Gino1.StatusCheck()
    EndTurnChecks(screen)


def ViewTeam(screen):
    global Gino1
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
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, rect in enumerate(rects):
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, rect in enumerate(rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        if event.button == 1:
                            squadra[i].ViewInformation(screen)
                        else:
                            Gino1 = squadra[i]

def End():
    with open("Files/stats.stt", 'r') as file:
        lines = [line.rstrip('\n') for line in file.readlines()]
    TotalScore = int(lines[0])
    TotalScore += assets.score
    with open("Files/stats.stt", 'w') as file:
        file.write(str(TotalScore))