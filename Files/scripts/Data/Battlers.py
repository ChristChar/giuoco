import pygame

BattlersType = {"Gino":{"BaseStat":{"HP":104,"ATT":72,"MAGIC":37,"DIF":97,"FUN":145,"VEL":105}, #560stat
                        "types":["meme", "AI"], 
                        "moves":{"start":["azione","rickroll", "ballo"]}, 
                        "baseEXP": 245, 
                        "growth_rate": "Slow", 
                        "EVS": {"FUN":2}},
                "Among us":{"BaseStat":{"HP":94,"ATT":132,"MAGIC":9,"DIF":65,"FUN":95,"VEL":93}, #488stat
                        "types":["meme"], 
                        "moves":{"start":["azione", "ballo","rugito"]}, 
                        "baseEXP": 201, 
                        "growth_rate": "Medium Slow", 
                        "EVS": {"ATT":2}},
                "Gatto":{"BaseStat":{"HP":82,"ATT":43,"MAGIC":45,"DIF":76,"FUN":195,"VEL":128}, #569stat
                         "types":["cute","meme"], 
                         "moves":{"start":["azione", "carineria","rugito"]}, 
                         "baseEXP": 223, 
                         "growth_rate": "Fast", 
                         "EVS": {"FUN":4}},
                "Rocky":{"BaseStat":{"HP":63,"ATT":121,"MAGIC":2,"DIF":118,"FUN":132,"VEL":84}, #520stat
                         "types":["sasso","pistola"], 
                         "moves":{"start":["azione", "sparo","Fissare"]}, 
                         "baseEXP": 218, 
                         "growth_rate": "Medium Slow", 
                         "EVS": {"ATT":1,"DIF":1}},
                "SQUIT":{"BaseStat":{"HP":65,"ATT":67,"MAGIC":74,"DIF":71,"FUN":45,"VEL":34}, #356stat 
                         "types":["acqua","normale"], 
                         "moves":{"start":["rugito", "Pistolacqua"]}, 
                         "baseEXP": 113, 
                         "growth_rate": "Fast", 
                         "EVS": {"MAGIC":1}}, 
                "Pikmin":{"BaseStat":{"HP":67,"ATT":46,"MAGIC":23,"DIF":34,"FUN":72,"VEL":89}, #331stat
                          "types":["erba"], 
                          "moves":{"start":["Erba schiaffo","rugito"]},
                          "baseEXP": 97, 
                          "growth_rate": "Fast", 
                          "EVS": {"VEL":1}}, 
                "Dinosauro":{"BaseStat":{"HP":123,"ATT":230,"MAGIC":1,"DIF":96,"FUN":37,"VEL":156}, #643stat
                          "types":["drago"], 
                          "moves":{"start":["Dragoartigli","rugito"]},
                          "baseEXP": 325, 
                          "growth_rate": "Fluctuating", 
                          "EVS": {"ATT":3,"VEL":2}},
                "Rubber duck":{"BaseStat":{"HP":135,"ATT":65,"MAGIC":55,"DIF":130,"FUN":89,"VEL":46}, #520stat
                          "types":["plastica","acqua"], 
                          "moves":{"start":["inquinamento", "Pistolacqua"]},
                          "baseEXP": 214, 
                          "growth_rate": "Medium Slow", 
                          "EVS": {"HP":1,"DIF":1}},
                "Zanzara":{"BaseStat":{"HP":37,"ATT":46,"MAGIC":3,"DIF":25,"FUN":2,"VEL":255}, #520stat
                          "types":["insetto","malvaggio"], 
                          "moves":{"start":["sanguisuga", "ronzio rompi palle"]},
                          "baseEXP": 214, 
                          "growth_rate": "Medium Fast", 
                          "EVS": {"VEL":3}},
                "ChatGPT":{"BaseStat":{"HP":142,"ATT":45,"MAGIC":88,"DIF":71,"FUN":13,"VEL":11}, #370stat
                          "types":["AI","informatico"], 
                          "moves":{"start":["taskkill", "Machine Learning"]},
                          "baseEXP": 134, 
                          "growth_rate": "Slow", 
                          "EVS": {"HP":2,"MAGIC":1}},
                "Cursore":{"BaseStat":{"HP":104,"ATT":63,"MAGIC":89,"DIF":93,"FUN":21,"VEL":200}, #570stat
                          "types":["informatico"], 
                          "moves":{"start":["taskkill", "Ctrl+C Ctrl+V"]},
                          "baseEXP": 243, 
                          "growth_rate": "Medium Slow", 
                          "EVS": {"HP":1,"VEL":2}},
                "Freddy":{"BaseStat":{"HP":156,"ATT":107,"MAGIC":43,"DIF":201,"FUN":67,"VEL":12}, #586stat
                          "types":["informatico", "meme"], 
                          "moves":{"start":["IPER RAGGIO","Fissare"]},
                          "baseEXP": 312, 
                          "growth_rate": "Slow", 
                          "EVS": {"HP":1,"DIF":2, "ATT":1}},
                "Sole":{"BaseStat":{"HP":201,"ATT":48,"MAGIC":149,"DIF":176,"FUN":36,"VEL":32}, #643stat
                          "types":["fuoco","luce"], 
                          "moves":{"start":["IPER RAGGIO","Brilla","Lanciafiamme"]},
                          "baseEXP": 436, 
                          "growth_rate": 'Fluctuating', 
                          "EVS": {"HP":2,"MAGIC":1,"DIF":2}},
                "Wooper":{"BaseStat":{"HP":65,"ATT":55,"MAGIC":25,"DIF":50,"FUN":72,"VEL":20}, #287stat
                          "types":["acqua","cute"], 
                          "moves":{"start":["Pistolacqua","carineria","rugito"]},
                          "baseEXP": 64, 
                          "growth_rate": 'Fast', 
                          "EVS": {"HP":1}},
                "Pinguino":{"BaseStat":{"HP":82,"ATT":57,"MAGIC":43,"DIF":74,"FUN":57,"VEL":92}, #405stat
                          "types":["acqua","ghiaccio","drago"], 
                          "moves":{"start":["Pistolacqua","Dragoartigli","Geloraggio","rugito"]},
                          "baseEXP": 102, 
                          "growth_rate": 'Medium Fast', 
                          "EVS": {"HP":1, "VEL":1}}}

for i in BattlersType:
    BattlersType[i]["sprite"] = pygame.image.load("Files/image/Battlers/"+i+".png")