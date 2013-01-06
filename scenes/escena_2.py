# encoding: utf-8
from src.scenefactory import AbstractScene
import sfml
from src import common
import escena_1
import logging
import pdb

class Helloworld(AbstractScene):
    def __init__(self, scenemanager):
        AbstractScene.__init__(self, scenemanager)
        self.__tipografia = sfml.Font.get_default_font()
        self.texto = sfml.Text(self.__str__())
        self.texto.font = self.__tipografia
        self.texto.character_size = 10
        self.texto.style = sfml.Text.BOLD
        self.texto.color = sfml.Color.WHITE
        self.loadmap("tmx/mapa prueba.tmx")
        
    def on_event(self, event):
        if type(event) is sfml.KeyEvent and event.pressed:
            if event.code == common.settings.getcontrollerbutton("up_button"):
                self.irescena1()
        if type(event) is sfml.MouseButtonEvent and event.pressed:
            if sfml.Mouse.is_button_pressed(sfml.Mouse.LEFT):
                #pdb.set_trace()
                position = sfml.Mouse.get_position(self.scenemanager.window)
                logging.debug("position: {0}".format(position))
                self.scenemanager.movecamera(position[0],
                                             position[1], False)
                logging.debug("Posicion del centro de la camara: {0}".format(
                        self.scenemanager.getcameraposition()))
                
    def on_update(self):
        pass
    
    def on_draw(self, window):
        self.drawmap()
        window.draw(self.texto)
        
    def irescena1(self):
        escena = escena_1.Helloworld(self.scenemanager)
        self.scenemanager.changescene(escena)
        
    def __str__(self):
        return "<Scene: HelloWorld, file: {0}>".format(__file__)
    
    
