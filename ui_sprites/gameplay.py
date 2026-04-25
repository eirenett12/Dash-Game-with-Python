from math import sin
from kink import di

from sprites import ImageSprite, TextSprite

import pygame as pg

import config


class SpritePenguin(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 0, 0, 255, *groups)

    def update_image(self, _player_position: int):
        # print(f"Updating SpritePenguin with {sin(pg.time.get_ticks()/2)*100+200}.")
        # self.set_pos(450, sin(pg.time.get_ticks()/2)*100+200)
        self.set_pos(100, _player_position)


class TextSpriteScore(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 30, 436, 255, "Score: ", di["clr_white"], *groups)


class SpriteTree(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 0, 0, 255, *groups)