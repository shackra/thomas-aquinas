# encoding: utf-8
from src.scenefactory import AbstractScene
import sfml
from src import common
import logging

class Helloworld(AbstractScene):
    def __init__(self, scenemanager):
        AbstractScene.__init__(self, scenemanager)
        self.loadmap("tmx/mapa prueba.tmx")
        self.sprites = []
        
    def on_event(self, event):
        if type(event) is sfml.MouseButtonEvent and event.pressed:
            if sfml.Mouse.is_button_pressed(sfml.Mouse.LEFT):
                # La posicion es relativa a la ventana y no al mapa.
                # FIXME: calibrar la posicion del clic en relacion al mapa.
                position = sfml.Mouse.get_position(self.scenemanager.window)
                logging.debug("Posicion: {0}".format(position))
                position = self.scenemanager.convertcoords(position)
                logging.debug("Convert Coords: {0}".format(position))
                self.scenemanager.movecamera(position[0],
                                             position[1], False)
                logging.debug("Nueva posicion del centro "
                              "de la camara: {0}".format(
                        self.scenemanager.getcameraposition()))
                
    def on_update(self):
        pass
    
    def on_draw(self, window):
        window.draw(self)
        
    def __str__(self):
        return "<Scene: HelloWorld, file: {0}>".format(__file__)
