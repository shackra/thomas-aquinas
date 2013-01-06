# encoding: utf-8
from src.scenefactory import AbstractScene
import sfml
from src import common
import escena_2

class Helloworld(AbstractScene):
    def __init__(self, scenemanager):
        AbstractScene.__init__(self, scenemanager)
        self.__tipografia = sfml.Font.get_default_font()
        self.texto = sfml.Text(self.__str__())
        self.texto.font = self.__tipografia
        self.texto.character_size = 10
        self.texto.style = sfml.Text.BOLD
        self.texto.color = sfml.Color.WHITE
        self.loadmap("tmx/mapa de prueba isometrico.tmx")

    def on_event(self, event):
        if type(event) is sfml.KeyEvent and event.pressed:
            if event.code == common.settings.getcontrollerbutton("down_button"):
                self.irescena2()

    def on_update(self):
        pass

    def on_draw(self, window):
        self.drawmap()
        window.draw(self.texto)

    def irescena2(self):
        escena = escena_2.Helloworld(self.scenemanager)
        self.scenemanager.changescene(escena)

    def __str__(self):
        return "<Scene: HelloWorld, file: {0}>".format(__file__)
