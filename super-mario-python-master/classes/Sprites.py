import json
import os
import sys

# Add the directory containing 'classes' to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'classes'))

from Animation import Animation
from Sprite import Sprite
from Spritesheet import Spritesheet

class Sprites:
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "../assets/sprites/Mario.json",  # Adjusted path
                    "../assets/sprites/Goomba.json",  # Adjusted path
                    "../assets/sprites/Koopa.json",   # Adjusted path
                    "../assets/sprites/Animations.json",  # Adjusted path
                    "../assets/sprites/BackgroundSprites.json",  # Adjusted path
                    "../assets/sprites/ItemAnimations.json",  # Adjusted path
                    "../assets/sprites/RedMushroom.json"  # Adjusted path
            ]
        )
        print("Loaded sprites:", self.spriteCollection.keys())  # Debugging line

    def loadSprites(self, urlList):
        resDict = {}
        for url in urlList:
            try:
                with open(url) as jsonData:
                    data = json.load(jsonData)
                    mySpritesheet = Spritesheet(data["spriteSheetURL"])
                    dic = {}

                    if data["type"] == "background":
                        for sprite in data["sprites"]:
                            colorkey = sprite.get("colorKey")
                            dic[sprite["name"]] = Sprite(
                                mySpritesheet.image_at(
                                    sprite["x"],
                                    sprite["y"],
                                    sprite["scalefactor"],
                                    colorkey,
                                ),
                                sprite["collision"],
                                None,
                                sprite["redrawBg"],
                            )
                    elif data["type"] == "animation":
                        for sprite in data["sprites"]:
                            images = [
                                mySpritesheet.image_at(
                                    image["x"],
                                    image["y"],
                                    image["scale"],
                                    colorkey=sprite.get("colorKey"),
                                ) for image in sprite["images"]
                            ]
                            dic[sprite["name"]] = Sprite(
                                None,
                                None,
                                animation=Animation(images, deltaTime=sprite["deltaTime"]),
                            )
                    elif data["type"] in ["character", "item"]:
                        for sprite in data["sprites"]:
                            colorkey = sprite.get("colorKey")
                            xSize, ySize = sprite.get('xsize'), sprite.get('ysize')
                            if xSize is None or ySize is None:
                                xSize, ySize = data['size']
                            dic[sprite["name"]] = Sprite(
                                mySpritesheet.image_at(
                                    sprite["x"],
                                    sprite["y"],
                                    sprite["scalefactor"],
                                    colorkey,
                                    True,
                                    xTileSize=xSize,
                                    yTileSize=ySize,
                                ),
                                sprite["collision"],
                            )

                    resDict.update(dic)

            except FileNotFoundError:
                print(f"File not found: {url}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {url}")
            except KeyError as e:
                print(f"Missing key {e} in file: {url}")
            except Exception as e:
                print(f"An error occurred while loading {url}: {e}")

        return resDict
