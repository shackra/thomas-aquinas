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
import logging
import sfml

from src.scenefactory import AbstractScene
from src.scenemanager import Director

class Scene(AbstractScene):
    def __init__(self, scenemanager):
        AbstractScene.__init__(self, scenemanager)
        self.loadmap() # Cargamos ningun mapa
        self.clock = sfml.Clock()
        self.timelapsed = 0
        
    def on_draw(self, window):
        window.draw(self)

    def on_event(self, event):
        self.timelapsed += self.clock.restart().milliseconds
        if self.timelapsed >= 3.0:
            self.scenemanager.exitgame()

class TestOpenwindow:
    @classmethod
    def setup_class(cls):
        print ("Configurando la prueba...")
        self.director = Director()
        self.scene = Scene(self.director)

    @classmethod
    def teardown_class(cls):
        print ("Limpiando la configuracion de la prueba")
        del(self.director)
        del(self.scene)

    def test_openwindow(self):
        self.director.changescene(self.scene)
        print ("Una ventana debe abrirse durante tres segundos")
        self.director.loop()
