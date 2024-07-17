import Files.scripts.dialogue as dialog

def AssorbiVita(screen, damage, self):
    Heal = damage/2
    self.HP = min(self.HP + Heal, self.maxHP)
    self.drawStateBar(screen, self.isEnemy)
    Text = dialog.dialoge(f"{self.type} si cura!")
    Text.update(screen)

def AfterSkipTurn(screen, self):
    self.riposo = True


MOVES = {
    "azione": {
        "type": "normale",
        "MoveType": "Fisica",
        "BasePower": 40,
        "precisione": 100,
        "target": "enemy"
    },
    "IPER RAGGIO": {
        "type": "magia",
        "MoveType": "Magic",
        "BasePower": 159,
        "precisione": 100,
         "Scripts": [AfterSkipTurn],
        "target": "enemy"
    },
    "sanguisuga": {
        "type": "insetto",
        "MoveType": "Fisica",
        "BasePower": 55,
        "precisione": 95,
        "ScriptDmage": [AssorbiVita],
        "target": "enemy"
    },
    "ronzio rompi palle": {
        "type": "insetto",
        "MoveType": "State",
        "Stat": [{"stats": ["ELUSIONE"], "Power": 0.6, "Target":"self"}],
        "precisione": 95,
        "target": "self"
    },
    "Ctrl+C Ctrl+V": {
        "type": "informatico",
        "MoveType": "State",
        "Stat": [{"stats": ["ELUSIONE"], "Power": 1, "Target":"self"}],
        "precisione": 100,
        "target": "self"
    },
    "inquinamento": {
        "type": "plastica",
        "MoveType": "Fisica",
        "BasePower": 65,
        "target": "enemy"
    },
    "Dragoartigli": {
        "type": "drago",
        "MoveType": "Fisica",
        "BasePower": 80,
        "precisione": 90,
        "target": "enemy"
    },
    "Erba schiaffo": {
        "type": "erba",
        "MoveType": "Fisica",
        "BasePower": 55,
        "precisione": 100,
        "target": "enemy"
    },
    "taskkill": {
        "type": "informatico",
        "MoveType": "Magic",
        "BasePower": 80,
        "precisione": 90,
        "target": "enemy"
    },
    "taskkill": {
        "type": "informatico",
        "MoveType": "Magic",
        "BasePower": 80,
        "precisione": 90,
        "target": "enemy"
    },
    "Pistolacqua": {
        "type": "acqua",
        "MoveType": "Magic",
        "BasePower": 40,
        "precisione": 100,
        "target": "enemy"
    },
    "rickroll": {
        "type": "meme",
        "MoveType": "Fisica",
        "BasePower": 60,
        "precisione": 95,
        "target": "enemy"
    },
    "sparo": {
        "type": "pistola",
        "MoveType": "Fisica",
        "BasePower": 120,
        "precisione": 50,
        "target": "enemy"
    },
    "ballo": {
        "type": "meme",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT", "DIF","VEL"], "Power": 0.7, "Target":"self"}],
        "precisione": 80,
        "target": "self"
    },
    "Machine Learning": {
        "type": "AI",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT","MAGIC","DIF","FUN","VEL"], "Power": 2, "Target":"self"}],
        "precisione": 100,
        "Scripts": [AfterSkipTurn],
        "target": "self"
    },
    "rugito": {
        "type": "normale",
        "MoveType": "State",
        "Stat": [{"stats": ["ATT"], "Power": -0.5, "Target":"enemy"}],
        "precisione": 100,
        "target": "enemy"
    },
    "Fissare": {
        "type": "normale",
        "MoveType": "State",
        "Stat": [{"stats": ["PRECISIONE"], "Power": 2, "Target":"self"}],
        "precisione": 100,
        "target": "self"
    },
    "carineria": {
        "type": "cute",
        "MoveType": "Fisica",
        "BasePower": 80,
        "Stat": [{"stats": ["DIF"], "Power": -0.3, "Target":"self", "probabilità":40}],
        "precisione": 90,
        "target": "enemy"
    }
}