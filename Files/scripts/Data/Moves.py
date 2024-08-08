import pygame
import random
import Files.scripts.dialogue as dialog
from Files.scripts.animation.MoveAnimation import *
import json

pygame.mixer.init()

#effetti
def AssorbiVita(screen, damage, self):
    Heal = damage/2
    self.HP = min(self.HP + Heal, self.maxHP)
    self.drawStateBar(screen, self.isEnemy)
    Text = dialog.dialoge(f"{self.type} si cura!")
    Text.update(screen)

def RigeneraVita(screen,self,enemy,move):
    Heal = self.maxHP * (MOVES[move]["Heal%"] / 100)
    self.HP = min(self.HP+Heal, self.maxHP)

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

        
f = open('Files/JSON/MoveData.json')

MOVES = json.load(f)

for move_name, moveData in MOVES.items():
    if "animation" in moveData:
        # Supponendo che animation sia il nome di una funzione, non eseguire 'exec' direttamente
        # Qui dovresti avere un dizionario di funzioni predefinite a cui mappare i nomi
        animation_name = moveData["animation"]
        moveData["animation"] = globals().get(animation_name, None)
    
    if "Scripts" in moveData:
        for i, script_name in enumerate(moveData["Scripts"]):
            # Supponendo che script sia il nome di una funzione, non eseguire 'exec' direttamente
            # Qui dovresti avere un dizionario di funzioni predefinite a cui mappare i nomi
            moveData["Scripts"][i] = globals().get(script_name, None)
    
    if "ScriptDmage" in moveData:
        for i, script_name in enumerate(moveData["ScriptDmage"]):
            # Supponendo che script sia il nome di una funzione, non eseguire 'exec' direttamente
            # Qui dovresti avere un dizionario di funzioni predefinite a cui mappare i nomi
            moveData["ScriptDmage"][i] = globals().get(script_name, None)

        