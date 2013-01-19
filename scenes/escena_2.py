# coding: utf-8
from src.scenefactory import AbstractScene
from src.spritefactory import AbstractSprite
import sfml
from src import common
from src import media
import logging

class Mai(AbstractSprite):
    def __init__(self, texture, near, solid,
                 movable, window, spritedatafile, rectangle=None):
        AbstractSprite.__init__(self, texture, near, solid,
                                movable, window, spritedatafile, rectangle)
        self.sprite.origin = sfml.Vector2(171 / 2.0, 155 / 2.0)
        self.setstate(0)
        
class Maitest(AbstractScene):
    def __init__(self, scenemanager):
        AbstractScene.__init__(self, scenemanager)
        self.loadmap("tmx/mai.tmx")
        self.spritesize = 0
        self.maitext = media.loadimg("sprites/others/Mai Shiranui "
                                     "basic spritesheet.png", False)
        mai = Mai(self.maitext, 0, True, False, self.scenemanager.window,
                  "sprites/others/Mai Shiranui basic spritesheet.json",
                  ((0,0),(1,1)))
        self.__sprite = {"mai": mai}
        screensize = common.settings.getscreensize()
        newposition = (screensize[0] / 2, screensize[1] / 1.5)
        self.__sprite["mai"].sprite.position = newposition
        
    def on_event(self, event):
        if isinstance(event, sfml.MouseWheelEvent):
            actual = self.__sprite["mai"].getstate()
            if event.delta <= 0.0:
                self.__sprite["mai"].setstate(actual - 1)
            else:
                self.__sprite["mai"].setstate(actual + 1)
                
    def on_update(self):
        # escalamos a Mai si fuera necesario
        #self.__sprite["mai"].sprite.scale(self.spritesize)
        pass
    
    def on_draw(self, window):
        logging.debug("Dibujando el mapa")
        self.drawmap() # aun no esta implementado
        self.__sprite["mai"].on_draw() #el bucle de dibujado de sprites, duh!
        
    def __str__(self):
        return "Escena donde se prueba la animacion de sprites."
    
