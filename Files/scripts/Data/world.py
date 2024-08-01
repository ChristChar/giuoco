import pygame
import os
import json

f = open('Files/JSON/worldData.json')

World = json.load(f)

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