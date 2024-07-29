import Files.scripts.assets as assets
import Files.scripts.Data.world as World

def SpawinList():
    Chance = []
    for batler, chance in World.World[assets.World].items():
        Chance.extend([batler] * chance)
    return Chance
