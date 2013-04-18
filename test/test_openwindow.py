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
from time import sleep

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

    def reset(self):
        self.timelapsed = 0

    def __str__(self):
        return "<Scene: Vacía>"

class SceneMove(AbstractScene):
    def __init__(self, scenemanager, initialmapfile):
        AbstractScene.__init__(self, scenemanager, initialmapfile)
        self.clock = sfml.Clock()
        self.timelapsed = 0
        self.moving = False

    def on_draw(self, window):
        if not self.moving:
            self.moving = True
            self.startmoving()

        window.draw(self)
        self.timelapsed += self.clock.restart().milliseconds
        if self.timelapsed >= 20000.0:
            self.scenemanager.exitgame()

    def on_event(self, event):
        pass

    def startmoving(self):
        """ movemos la camara atraves del escenario.
        """
        self.scenemanager.movecamera(18*32, 12*32, False, 16)

    def __str__(self):
        return "<Scene: Vacía>"

def setup_func():
    global director
    global scene
    director = Director()
    scene = Scene(director, None)

def setup_func2():
    global director
    global scene
    director = Director()
    scene = SceneMove(director, None)

def teardown_func():
    director.changescene(scene)
    director.loop()
    sleep(1)

def teardown_func2():
    sleep(1)

@nose.with_setup(setup_func, teardown_func)
def test_openwindow():
    director.changescene(scene)

@nose.with_setup(setup_func, teardown_func)
def test_minimapa():
    scene.loadanothermap("/uniteststuff/minimap.tmx")
    scene.loadmaptiles()
    scene.loadmapimages()
    scene.loadmapobjects()

@nose.with_setup(setup_func, teardown_func)
def test_bigmapa():
    scene.loadanothermap("/uniteststuff/bigmap.tmx")
    scene.loadmaptiles()
    scene.loadmapimages()
    scene.loadmapobjects()

@nose.with_setup(setup_func2, teardown_func)
def test_movebigmapa():
    scene.loadanothermap("/uniteststuff/bigmap.tmx")
    scene.loadmaptiles()
    scene.loadmapimages()
    scene.loadmapobjects()

