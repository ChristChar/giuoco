import random

def AI0(battler, Turn):
    UtilizableMoves = []
    for move in battler.PP:
        if battler.PP[move] > 0:
            UtilizableMoves.append(move)
    if len(UtilizableMoves) > 0:
        return random.choice(UtilizableMoves)
    return "azione"

Levels = {0:AI0}

def AI(battler, Turn, Level):
    return Levels[Level](battler, Turn)