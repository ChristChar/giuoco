import pygame
import sys
import Files.scripts.assets as assets
import Files.scripts.BattlersDatabase as data
import Files.scripts.functions as F


class button:
    def __init__(self, text, color, position, script, ScriptVariable = None):
        self.position = position
        self.text = text
        self.color = color
        self.script = script
        if ScriptVariable is not None:
            self.scriptVariable = ScriptVariable
        self.rect = pygame.rect.Rect(0,0,150,50)
        if F.is_color_light(self.color):
            self.Tcolor = (0,0,0)
        else:
            self.Tcolor = (255,255,255)

    def draw(self, screen, i):
        ScW, ScH = assets.ScreenDimension
        NewScalY = ScH / 10
        self.rect.height = NewScalY
        NewScalX = NewScalY * 3
        self.rect.width = NewScalX
        if self.position == "center":
            posX = ScW / 2 - NewScalX / 2
            self.rect.x = posX
            posY = ScH / 2 - NewScalY / 2
            self.rect.y = posY + i * ScH / 9
        elif self.position == "-x-y":
            posX = NewScalX + 20
            self.rect.x = posX
            posY = NewScalY + 20
            self.rect.y = posY - i * ScH / 9
        elif self.position == "+x-y":
            posX = ScW - NewScalX - 20
            self.rect.x = posX
            posY = NewScalY + 20
            self.rect.y = posY - i * ScH / 9
        elif self.position == "-x+y":
            posX = NewScalX + 20
            self.rect.x = posX
            posY = ScH - NewScalY - 20
            self.rect.y = posY - i * ScH / 9
        elif self.position == "+x+y":
            posX = ScW - NewScalX - 20
            self.rect.x = posX
            posY = ScH - NewScalY - 20
            self.rect.y = posY - i * ScH / 9
        MX, MY = pygame.mouse.get_pos()
        if self.rect.collidepoint(MX,MY):
            color = tuple(max(0, min(255, value - 50)) for value in self.color)
        else:
            color = self.color
        F.draw_rounded_rect(screen, color, self.rect, 10)
        TeW, TeH = 999, 999
        D = round(NewScalY)
        font = pygame.font.SysFont(None, D)
        text = font.render(self.text, True,  self.Tcolor)
        TeW, TeH = text.get_size()
        if TeW+5 > self.rect.width:
            D = round(NewScalY / 2)     
            font = pygame.font.SysFont(None, D)
            text = font.render(self.text, True, self.Tcolor)
            TeW, TeH = text.get_size()
        screen.blit(text, (self.rect.x + self.rect.width/2 - TeW/2, self.rect.y + self.rect.height/2 - TeH/2))
    
    def WhenClicked(self):
        if isinstance(self.script, str):
            assets.mode = self.script
        else:
            self.script()

    def ControllClicked(self, event):
        mouse_x, mouse_y = event.pos
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.WhenClicked()

def quit():
    pygame.quit()
    sys.exit()

start = button("START", (255,0,0),"center", "game")
Quit = button("QUIT", (0,200,255),"center", quit)
BUY = button("Buy", (255, 255, 0), "center", data.Buy)
stat = button("Stat Moltiplicator", (150, 150, 150), "center", "Stats")

Buttons = {"menu":[start,Quit],"game":[], "shop":[BUY], "statshop":[stat], "Stats":[]}

def updateButtons(screen):
    for i, Butt in enumerate(Buttons[assets.mode]):
        Butt.draw(screen, i)

def ControllButtons(event):
    for Butt in Buttons[assets.mode]:
        Butt.ControllClicked(event)
