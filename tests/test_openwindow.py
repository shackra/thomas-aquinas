# coding: utf-8
# This file is part of Thomas Aquinas.
#
# Thomas Aquinas is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Thomas Aquinas is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Thomas Aquinas.  If not, see <http://www.gnu.org/licenses/>.
#
#                       veni, Sancte Spiritus.

import nose
from nose.tools import eq_, ok_
import logging
import sfml

from lib.scenefactory import AbstractScene
from lib.scenemanager import Director

class Scene(AbstractScene):
    def __init__(self, scenemanager, initialmapfile):
        AbstractScene.__init__(self, scenemanager, initialmapfile)
        self.clock = sfml.Clock()
        self.timelapsed = 0

    def on_draw(self, window):
        window.draw(self)
        self.timelapsed += self.clock.restart().milliseconds
        if self.timelapsed >= 10000.0:
            self.scenemanager.exitgame()

    def on_event(self, event):
        pass

    def __str__(self):
        return "<Scene: Vacía>"

class TestOpenwindow:
    @classmethod
    def setup_class(cls):
        print ("Configurando la prueba...")
        global director
        global scene
        director = Director()
        scene = Scene(director, None)

    @nose.tools.timed(11)
    def test_openwindow(self):
        scene = Scene(director, None)
        director.changescene(scene)
        print ("Una ventana debe abrirse durante 10 segundos")
        director.loop()

    @nose.tools.timed(11)
    def test_minimapa(self):
        scene = Scene(director, "/uniteststuff/minimap.tmx")
        scene.loadmaptiles()
        scene.loadmapimages()
        scene.loadmapobjects()
        director.changescene(scene)
        director.loop()

    def test_loadmaptiles(self):
        scene.loadanothermap("/uniteststuff/4tilesmap.tmx")
        scene.loadmaptiles()
        eq_(len(scene.tmxdata.images), 5)
        ok_(isinstance(scene.tmxdata.images[0], int), ("El primer valor de la "
                                                        "lista no es del tipo"
                                                        " int"))

    def test_loadmapimages(self):
        scene.loadanothermap("/uniteststuff/4tilesmap.tmx")
        scene.loadmaptiles()
        scene.loadmapimages()
