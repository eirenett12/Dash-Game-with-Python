from kink import di

from sprites import ImageSprite

import pygame as pg

import config


class SpriteIntro(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 0, 0, 255, *groups)