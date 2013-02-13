# coding: utf-8
from src.scenefactory import AbstractScene
from src.spritefactory import Entity
import sfml
from src import common
from src import media
import logging


class Maitest(AbstractScene):
    def __init__(self, scenemanager):
        super(AbstractScene, self).__init__(self)
        self.scenemanager = scenemanager
        self.loadmap()
        maitext = media.loadimg("sprites/others/Mai Shiranui "
                                     "basic spritesheet.png", False)
        mai = Entity("mai", maitext, self.scenemanager.window,
                     "sprites/others/Mai Shiranui basic spritesheet.json", None)
        mai.sprite.origin = sfml.Vector2(171 / 2.0, 155 / 2.0)
        mai.setstate(0)
        screensize = common.settings.getscreensize()
        newposition = (screensize[0] / 2, screensize[1] / 1.5)
        mai.sprite.position = newposition
        self.addsprite(mai)
        
    def on_event(self, event):
        if isinstance(event, sfml.MouseWheelEvent):
            pass
                
    def on_update(self):
        # escalamos a Mai si fuera necesario
        #self.__sprite["mai"].sprite.scale(self.spritesize)
        pass
    
    def on_draw(self, window):
        window.draw(self)
        
    def __str__(self):
        return "Escena donde se prueba la animacion de sprites."    
    
