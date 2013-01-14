# coding: utf-8
from src.scenefactory import AbstractScene
from src.spritefactory import AbstractSprite
import sfml
from src import common
from src import media
import logging

class Mai(AbstractSprite):
    def __init__(self, )
    
class Maitest(AbstractScene):
    def __init__(self, scenemanager):
        AbstractScene.__init__(self, scenemanager)
        self.loadmap("tmx/mai.tmx")
        self.spritesize = 0
        self.maitext = media.loadimg("sprites/others/Mai Shiranui "
                                     "basic spritesheet.png", False)
        self.__sprites = {"mai": Mai(self.maitext, 0, self.scenemanager.window,
                                     "sprites/others/maidata.json")}

    def on_event(self, event):
        if isinstance(event, sfml.MouseWheelEvent):
            self.scenemanager.tweener.AddTween(self, spritesize=event.delta,
                                               tweenTime=3)
            
            
