import random
import json

f = open('Files/JSON/TypeData.json')

types = json.load(f)

TypesColor = {"fuoco":(255,180,0),
                "acqua":(0,255,255),
                "erba":(0,200,0),
                "elettro":(255,255,0),
                "sasso":(255,230,150),
                "terra":(150,50,0),
                "luce":(255,255,200),
                "ghiaccio":(150,250,250),
                "acciaio":(150,150,150),
                "gas":(200,200,200),
                "normale":(255,255,255),
                "veleno":(150,0,150),
                "meme":(200,255,255),
                "cringe":(10,0,0),
                "magia":(200,0,200),
                "malvaggio":(30,30,30),
                "cute":(255,200,200),
                "pistola":(90,90,90),
                "drago":(70,0,150),
                "plastica":(220,220,220),
                "insetto": (100,200,0),
                "AI": (255,0,30),
                "informatico": (0,200,30),
                "gamer":(random.randint(100,255),random.randint(100,255),random.randint(100,255)),
                "spazio":(0,0,50),
                "glitch":(0,0,0),
                "cibo":(222, 184, 135),
                "lotta":(255,255,0),
                "volante":(150,170,220),
                "carta":(245,245,245)}