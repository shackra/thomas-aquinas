#!/usr/bin/env python2
# coding: utf-8

from lib import scenemanager
from lib.scenefactory import AbstractScene
from lib import common
#import logging
import sfml

class SceneMove(AbstractScene):
    def __init__(self, scenemanager, initialmapfile):
        AbstractScene.__init__(self, scenemanager, initialmapfile)
        self.clock = sfml.Clock()

    def on_draw(self, window):
        window.draw(self)

    def on_event(self, event):
        if isinstance(event, sfml.window.MouseButtonEvent):
            if event.pressed:
                mousex, mousey = self.scenemanager.convertcoords(
                    event.position)
                self.scenemanager.movecamera(mousex, mousey, False, 3)

    def __str__(self):
        return "<Scene: Vacía>"

director = scenemanager.Director()
escena = SceneMove(director, "/uniteststuff/bigmap.tmx")
escena.loadmaptiles()
escena.loadmapimages()
escena.loadmapobjects()
director.changescene(escena)
director.loop()
