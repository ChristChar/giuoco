import pygame

BattlersType = {"Gino":{"BaseStat":{"HP":104,"ATT":72,"MAGIC":37,"DIF":97,"FUN":145,"VEL":105}, #560stat
                        "types":["meme", "AI"], 
                        "moves":{"start":["azione","rickroll", "ballo"]}, 
                        "baseEXP": 245, 
                        "growth_rate": "Slow", 
                        "EVS": {"FUN":2},
                        "Dex":"Gino è molto bello"},
                "Among us":{"BaseStat":{"HP":94,"ATT":132,"MAGIC":9,"DIF":65,"FUN":95,"VEL":93}, #488stat
                        "types":["meme"], 
                        "moves":{"start":["azione", "ballo","rugito","IMPOSTOR"]}, 
                        "baseEXP": 201, 
                        "growth_rate": "Medium Slow", 
                        "EVS": {"ATT":2},
                        "Dex":"SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS SUS"},
                "Gatto":{"BaseStat":{"HP":82,"ATT":43,"MAGIC":45,"DIF":76,"FUN":195,"VEL":128}, #569stat
                         "types":["normale","cute","meme"], 
                         "moves":{"start":["azione", "carineria","rugito"]}, 
                         "baseEXP": 223, 
                         "growth_rate": "Fast", 
                         "EVS": {"FUN":4},
                        "Dex":"Gioca anche a Cat vs Memes che puoi trovare su gamejolt in questo link: https://gamejolt.com/games/CAT-VS-MEMES/901164"},
                "Rocky":{"BaseStat":{"HP":63,"ATT":121,"MAGIC":2,"DIF":118,"FUN":132,"VEL":84}, #520stat
                         "types":["sasso","pistola"], 
                         "moves":{"start":["azione", "sparo","Fissare","Sassata"]}, 
                         "baseEXP": 218, 
                         "growth_rate": "Medium Slow", 
                         "EVS": {"ATT":1,"DIF":1},
                        "Dex":"Un sasso con un fucile, cosa vuoi di più?"},
                "SQUIT":{"BaseStat":{"HP":65,"ATT":67,"MAGIC":74,"DIF":71,"FUN":45,"VEL":34}, #356stat 
                         "types":["acqua","normale"], 
                         "moves":{"start":["rugito", "Pistolacqua"]}, 
                         "baseEXP": 113, 
                         "growth_rate": "Fast", 
                         "EVS": {"MAGIC":1},
                        "Dex":"SQUIT è una fusione nata su pokerogue fra Squirtle ed Sentret shiny"}, 
                "Red Pikmin":{"BaseStat":{"HP":67,"ATT":46,"MAGIC":23,"DIF":34,"FUN":72,"VEL":89}, #331stat
                          "types":["erba", "fuoco"], 
                          "moves":{"start":["Erba schiaffo","rugito","Braciere"]},
                          "baseEXP": 97, 
                          "growth_rate": "Fast", 
                          "EVS": {"VEL":1},
                          "Dex":"il pikmin proviene del pianeta pnf 404, cioè il pianeta Terra post apocalittico!!!"}, 
                "Blue Pikmin":{"BaseStat":{"HP":67,"ATT":26,"MAGIC":33,"DIF":34,"FUN":72,"VEL":99}, #331stat
                          "types":["erba", "acqua"], 
                          "moves":{"start":["Erba schiaffo","Pistolacqua","Fissare"]},
                          "baseEXP": 97, 
                          "growth_rate": "Fast", 
                          "EVS": {"VEL":1},
                          "Dex":"Lui sa nuotare, gli altri affogano malamente"}, 
                "Yellow Pikmin":{"BaseStat":{"HP":67,"ATT":31,"MAGIC":38,"DIF":34,"FUN":72,"VEL":89}, #331stat
                          "types":["erba", "elettro"], 
                          "moves":{"start":["Erba schiaffo","Tuonoshock","Tuononda"]},
                          "baseEXP": 97, 
                          "growth_rate": "Fast", 
                          "EVS": {"VEL":1},
                          "Dex":"Batteria portatile"}, 
                "Purple Pikmin":{"BaseStat":{"HP":77,"ATT":76,"MAGIC":23,"DIF":46,"FUN":82,"VEL":59}, #362stat
                          "types":["erba"], 
                          "moves":{"start":["Erba schiaffo","rugito"]},
                          "baseEXP": 108, 
                          "growth_rate": "Fast", 
                          "EVS": {"ATT":1},
                          "Dex":"FORZA FISICA, solo quello conta"}, 
                "White Pikmin":{"BaseStat":{"HP":67,"ATT":36,"MAGIC":23,"DIF":14,"FUN":82,"VEL":109}, #331stat
                          "types":["erba","veleno"], 
                          "moves":{"start":["Erba schiaffo","rugito","smog"]},
                          "baseEXP": 97, 
                          "growth_rate": "Fast", 
                          "EVS": {"VEL":2},
                          "Dex":"Fissalo molto attentamente negli occhi e dimmi come ti senti"}, 
                "Dinosauro":{"BaseStat":{"HP":123,"ATT":230,"MAGIC":1,"DIF":96,"FUN":37,"VEL":156}, #643stat
                          "types":["drago"], 
                          "moves":{"start":["Dragoartigli","rugito"]},
                          "baseEXP": 325, 
                          "growth_rate": "Fluctuating", 
                          "EVS": {"ATT":3,"VEL":2},
                          "Dex":"Ti apettavi un T-rex? Invece beccati questo dinosauro aviano, l'antenato del pettirosso"},
                "Rubber duck":{"BaseStat":{"HP":135,"ATT":65,"MAGIC":55,"DIF":130,"FUN":89,"VEL":46}, #520stat
                          "types":["plastica","acqua"], 
                          "moves":{"start":["inquinamento", "Pistolacqua"]},
                          "baseEXP": 214, 
                          "growth_rate": "Medium Slow", 
                          "EVS": {"HP":1,"DIF":1},
                          "Dex":"QUAK QUAK, give me some bread pls"},
                "Zanzara":{"BaseStat":{"HP":37,"ATT":46,"MAGIC":3,"DIF":25,"FUN":2,"VEL":255}, #520stat
                          "types":["insetto","malvaggio"], 
                          "moves":{"start":["sanguisuga", "ronzio rompi palle"]},
                          "baseEXP": 214, 
                          "growth_rate": "Medium Fast", 
                          "EVS": {"VEL":3},
                          "Dex":"Il rompi palle in insetto"},
                "ChatGPT":{"BaseStat":{"HP":142,"ATT":45,"MAGIC":88,"DIF":71,"FUN":13,"VEL":11}, #370stat
                          "types":["AI","informatico"], 
                          "moves":{"start":["taskkill", "Machine Learning"]},
                          "baseEXP": 134, 
                          "growth_rate": "Slow", 
                          "EVS": {"HP":2,"MAGIC":1},
                          "Dex":"ChatGPT è un modello di linguaggio sviluppato da OpenAI basato sull'architettura GPT-4. È progettato per comprendere e generare testo umano in modo naturale, rispondendo a una vasta gamma di domande e assistendo con molteplici compiti, come scrivere codice, fornire spiegazioni tecniche, creare contenuti creativi, tradurre lingue e molto altro. ChatGPT è in grado di apprendere dal contesto delle conversazioni e fornire risposte coerenti e utili, rendendolo uno strumento versatile per supportare utenti in vari settori."},
                "Cursore":{"BaseStat":{"HP":104,"ATT":63,"MAGIC":89,"DIF":93,"FUN":21,"VEL":200}, #570stat
                          "types":["informatico"], 
                          "moves":{"start":["taskkill", "Ctrl+C Ctrl+V"]},
                          "baseEXP": 243, 
                          "growth_rate": "Medium Slow", 
                          "EVS": {"HP":1,"VEL":2},
                          "Dex":"lo stai usando tu in questo preciso momento con il tuo bel topo"},
                "Freddy":{"BaseStat":{"HP":156,"ATT":107,"MAGIC":43,"DIF":201,"FUN":67,"VEL":12}, #586stat
                          "types":["informatico", "meme"], 
                          "moves":{"start":["IPER RAGGIO","Fissare"]},
                          "baseEXP": 312, 
                          "growth_rate": "Slow", 
                          "EVS": {"HP":1,"DIF":2, "ATT":1},
                          "Dex":"hur hur hur hur hur hur hur"},
                "Sole":{"BaseStat":{"HP":201,"ATT":48,"MAGIC":149,"DIF":176,"FUN":36,"VEL":32}, #643stat
                          "types":["fuoco","luce","spazio"], 
                          "moves":{"start":["IPER RAGGIO","Brilla","Lanciafiamme"]},
                          "baseEXP": 436, 
                          "growth_rate": 'Fluctuating', 
                          "EVS": {"HP":2,"MAGIC":1,"DIF":2},
                          "Dex":"LODARE IL SOLE"},
                "Wooper":{"BaseStat":{"HP":65,"ATT":55,"MAGIC":25,"DIF":50,"FUN":72,"VEL":20}, #287stat
                          "types":["acqua","cute"], 
                          "moves":{"start":["Pistolacqua","carineria","rugito"]},
                          "baseEXP": 64, 
                          "growth_rate": 'Fast', 
                          "EVS": {"HP":1},
                          "Dex":"Più precisamente beta wooper"},
                "Pinguino":{"BaseStat":{"HP":82,"ATT":57,"MAGIC":43,"DIF":74,"FUN":57,"VEL":92}, #405stat
                          "types":["acqua","ghiaccio","drago"], 
                          "moves":{"start":["Pistolacqua","Dragoartigli","Geloraggio","rugito"]},
                          "baseEXP": 102, 
                          "growth_rate": 'Medium Fast', 
                          "EVS": {"HP":1, "VEL":1},
                          "Dex":"è di tipo drago perchè discende dai dinosauri =)"},
                "Cane":{"BaseStat":{"HP":68,"ATT":78,"MAGIC":62,"DIF":45,"FUN":43,"VEL":80}, #376stat
                          "types":["normale"], 
                          "moves":{"start":["rugito","Morso","carineria"]},
                          "baseEXP": 82, 
                          "growth_rate": 'Medium Fast', 
                          "EVS": {"VEL":1},
                          "Dex":"BAU"},
                "Nuvola":{"BaseStat":{"HP":104,"ATT":25,"MAGIC":58,"DIF":37,"FUN":17,"VEL":93}, #334stat
                          "types":["gas","acqua","elettro"], 
                          "moves":{"start":["Pistolacqua","Tuonoshock","vento"]},
                          "baseEXP": 74, 
                          "growth_rate": 'Fast', 
                          "EVS": {"HP":1},
                          "Dex":"Io ci vedo Super Mario"},
                "PC da gaming":{"BaseStat":{"HP":132,"ATT":45,"MAGIC":38,"DIF":58,"FUN":89,"VEL":122}, #484stat
                          "types":["gamer","informatico","luce"], 
                          "moves":{"start":["Brilla","Tuonoshock","taskkill","Trhyhard"]},
                          "baseEXP": 127, 
                          "growth_rate": 'Fast', 
                          "EVS": {"HP":1, "VEL":1},
                          "Dex":"La leggenda dice che questo PC da gaming ha così tante luci da gaming che è in grado di accecare chiunque lo guardi"},
                "Albero":{"BaseStat":{"HP":164,"ATT":78,"MAGIC":11,"DIF":168,"FUN":56,"VEL":8}, #485stat
                          "types":["erba","terra"], 
                          "moves":{"start":["Terremoto","Radice schiaffo"]},
                          "baseEXP": 128, 
                          "growth_rate": 'Fast', 
                          "EVS": {"HP":1, "DIF":1},
                          "Dex":"Per fare il tavolo ci vuole il legno, per fare il legno ci vuole l'albero, per fare l'albero ci vuole un seme, per fare il seme ci vuole un frutto, per fare un frutto ci vuole un fiore, per fare il fiore ci vuole una pianta, per fare la piante..."},
                "Forchetta":{"BaseStat":{"HP":67,"ATT":73,"MAGIC":45,"DIF":64,"FUN":24,"VEL":12}, #285stat
                          "types":["acciaio"], 
                          "moves":{"start":["Ferrartigli","Ferroscudo"]},
                          "baseEXP": 56, 
                          "growth_rate": 'Fast', 
                          "EVS": {"ATT":1},
                          "Dex":"Forchetta"},
                "Creeper":{"BaseStat":{"HP":50,"ATT":255,"MAGIC":10,"DIF":10,"FUN":10,"VEL":255}, #590stat
                          "types":["normale"], 
                          "moves":{"start":["ESPLOSIONE"]},
                          "baseEXP": 590, 
                          "growth_rate": 'Fast', 
                          "EVS": {"ATT":1,"VEL":1},
                          "Dex":"Esplode prima che te lo aspetti"}}

for i in BattlersType:
    BattlersType[i]["sprite"] = pygame.image.load("Files/image/Battlers/"+i+".png")