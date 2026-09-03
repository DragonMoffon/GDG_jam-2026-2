from dataclasses import dataclass, fields

from arcade import SpriteList

@dataclass
class GameLayers:
    ground: SpriteList
    shadows: SpriteList
    pieces: SpriteList