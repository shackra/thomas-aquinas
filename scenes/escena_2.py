# coding: utf-8
from src.scenefactory import AbstractScene
from src.spritefactory import AbstractSprite
import sfml
from src import common
from src import media
import logging

class Mai(AbstractSprite):
    def __init__(self, texture, near, window, spritedatafile):
        super(Mai, self).__init__(texture, near, window, spritedatafile)
        self.setstate(0) # dejamos a Mai en el estado 0 por ahora.
        
class Maitest(AbstractScene):
    def __init__(self, scenemanager):
        AbstractScene.__init__(self, scenemanager)
        self.loadmap("tmx/mai.tmx")
        self.spritesize = 0
        self.maitext = media.loadimg("sprites/others/Mai Shiranui "
                                     "basic spritesheet.png", False)
        self.__sprite = {"mai": Mai(self.maitext, 0, self.scenemanager.window,
                                     "sprites/others/Mai Shiranui "
                                     "basic spritesheet.json")}
        screensize = common.settings.getscreensize()
        newposition = (screensize[0] / 2, screensize[1] / 3)
        self.__sprite["mai"].position = newposition
        
    def on_event(self, event):
        if isinstance(event, sfml.MouseWheelEvent):
            self.scenemanager.tweener.AddTween(self, spritesize=event.delta,
                                               tweenTime=3)
            
    def on_update(self):
        # escalamos a Mai si fuera necesario
        self.__sprite["mai"].scale(self.spritesize)
        
    def on_draw(self, window):
        self.drawmap() # aun no esta implementado
        self.__sprite["mai"].on_draw() #el bucle de dibujado de sprites, duh!
        
    def __str__(self):
        return "Escena donde se prueba la animacion de sprites."
