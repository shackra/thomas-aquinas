# encoding: utf-8
from src.scenefactory import AbstractScene
from src.spritefactory import Entity
import sfml
from src import common
from src import media
import logging

class Helloworld(AbstractScene):
    def __init__(self, scenemanager):
        AbstractScene.__init__(self, scenemanager)
        self.loadmap("tmx/mapa prueba.tmx")
        doll = Entity("doll", media.loadimg("sprites/others/test.png", False),
                      self.scenemanager.window, "sprites/others/test.json",
                      None)
        doll.setstate(0)
        doll.addcontroller(move)
        doll.zindex = 1
        self.addsprite(doll)
        
    def on_event(self, event):
        self.updatesprites(event)
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

    def on_draw(self, window):
        window.draw(self)

    def __str__(self):
        return "<Scene: HelloWorld, file: {0}>".format(__file__)

def move(entity, event):
    """ Controlador que mueve a la entidad.
    """
    if isinstance(event, sfml.KeyEvent) and event.pressed:
        if event.code == common.settings.getcontrollerbutton("up_button"):
            entity.sprite.position += sfml.Vector2(0, -10)
            entity.setstate(1)
        elif event.code == common.settings.getcontrollerbutton("down_button"):
            entity.sprite.position += sfml.Vector2(0, 10)
            entity.setstate(2)
        elif event.code == common.settings.getcontrollerbutton("left_button"):
            entity.sprite.position += sfml.Vector2(-10, 0)
            entity.setstate(3)
        elif event.code == common.settings.getcontrollerbutton("right_button"):
            entity.sprite.position += sfml.Vector2(10, 0)
            entity.setstate(4)
    elif isinstance(event, sfml.KeyEvent) and event.released:
        entity.setstate(0)
