import random
from Files.scripts.Data.Moves import MOVES
import Files.scripts.Data.Moves as Mo

def AI0(battler, Turn, Avversario):
    UtilizableMoves = []
    for move in battler.PP:
        if battler.PP[move] > 0:
            UtilizableMoves.append(move)
    if len(UtilizableMoves) > 0:
        return random.choice(UtilizableMoves)
    return "azione"

def AI1(battler, Turn, enemy):
    UtilizableMoves = []
    for move in battler.PP:
        if battler.PP[move] > 0:
            UtilizableMoves.append(move)
    if len(UtilizableMoves) > 0:
        StatusMoves = []
        DamageMoves = []
        for i in UtilizableMoves:
            if MOVES[i]["MoveType"] == "State":
                StatusMoves.append(i)
            else:
                DamageMoves.append(i)
        if random.random() < 1 / Turn and len(StatusMoves) > 0:
            return random.choice(StatusMoves)
        elif len(DamageMoves) > 0:
            Power = {}
            for move in DamageMoves:
                if "BasePower" in MOVES[i]:
                    MovePower = MOVES[i]["BasePower"]
                    MovePower *= battler.Calcolate_typeBoost(move, enemy)
                    Power[move] = MovePower
            BestPower = [0,random.choice(UtilizableMoves)]
            for move, power in Power.items():
                if power > BestPower[0]:
                    BestPower[0] = power
                    BestPower[1] = move
            return BestPower[1]
    return "azione"

def AI2(battler, Turn, enemy):
    UtilizableMoves = [move for move in battler.PP if battler.PP[move] > 0]
    
    if UtilizableMoves:
        StatusMoves = []
        DamageMoves = []
        
        for move in UtilizableMoves:
            if MOVES[move]["MoveType"] == "State":
                StatusMoves.append(move)
            else:
                DamageMoves.append(move)
        
        HealMove = []
        StatusMove = []
        StatMove = []
        
        for move in StatusMoves:
            if "Scripts" in MOVES[move]:
                if Mo.RigeneraVita in MOVES[move]["Scripts"]:
                    HealMove.append(move)
                
                status_effects = [Mo.DRG, Mo.PAR, Mo.POI, Mo.BRN, Mo.SLE]
                if MOVES[move]["target"] == "enemy" and any(status in MOVES[move]["Scripts"] for status in status_effects):
                    StatusMove.append(move)
            
            if "Stat" in MOVES[move]:
                StatMove.append(move)
        
        if HealMove and battler.HP < battler.maxHP / 2:
            return random.choice(HealMove)
        
        if StatusMove and enemy.state is None:
            return random.choice(StatusMove)
        
        if random.random() < 1 / Turn and StatMove:
            return random.choice(StatMove)
        
        if DamageMoves:
            Power = {}
            for move in DamageMoves:
                if "BasePower" in MOVES[move]:
                    MovePower = MOVES[move]["BasePower"]
                    MovePower *= battler.Calcolate_typeBoost(move, enemy)
                    
                    BonusPower = 1
                    if "ScriptDmage" in MOVES[move] and "AssorbiVita" in MOVES[move]["ScriptDmage"]:
                        MovePower *= 1.3
                    if "FlitchChance" in MOVES[move]:
                        BonusPower += MOVES[move]["FlitchChance"]
                    if "precisione" in MOVES[move]:
                        BonusPower += MOVES[move]["precisione"]
                    else:
                        MovePower *= 1.7
                    
                    Power[move] = MovePower + BonusPower
            
            BestPower = [0, random.choice(UtilizableMoves)]
            for move, power in Power.items():
                if power > BestPower[0]:
                    BestPower = [power, move]
            
            return BestPower[1]
    
    return "azione"


Levels = {0:AI0, 1:AI1, 2:AI2}

def AI(battler, Turn, Level, avversario):
    return Levels[Level](battler, Turn, avversario)