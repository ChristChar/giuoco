import pygame
import os


World = {"Forest":{"Gatto":20,"Zanzara":10,"Cane":20,"Nuvola":10,"Sole":5,"Albero":15,"Bidoof":15,"Creeper":5},
         "cucina":{"Pane":45, "Forchetta":45,"Zanzara":5,"Rubber duck":5},
         "spiaggia":{"Sole":10,"Nuvola":10,"SQUIT":25,"Rubber duck":25,"Zanzara":5,"Wooper":20,"Pinguino":5},
         "Stanza da gaming":{"Pane":5,"PC da gaming":40,"Cane":7,"Cursore":20,"ChatGPT":15,"Zanzara":1,"Rubber duck":5,"Gatto":7},
         "MemeWorld":{"Gino":30,"Among us":30,"Gatto":40},
         "pnf-404":{"Red Pikmin":1,"Blue Pikmin":1,"Yellow Pikmin":1,"Purple Pikmin":1,"White Pikmin":1,"Rock Pikmin":1},
         "strada":{"Gatto":10,"Cane":10,"Rocky":10,"Zanzara":5,"Freddy":5,"Nuvola":5,"Sole":5,"Albero":10,"Ferrari":20,"Pettirosso":10,
                   "Dinosauro":5,"Gino":5}}

image_folder = "Files/image/Background/"
image = {}
for i in World:
    image_path = f"{image_folder}{i}.png"
    if os.path.exists(image_path):
        try:
            image[i] = pygame.image.load(image_path)
        except pygame.error as e:
            print(f"Errore durante il caricamento dell'immagine {image_path}: {e}")
    else:
        print(f"Il file {image_path} non esiste")