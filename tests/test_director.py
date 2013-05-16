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

from nose.tools import ok_, eq_, raises, with_setup

from summa.director import director
from summa.director import Director
from summa.layer import ColorLayer
from summa.scene import Scene
import pyglet


class TestDirectorScene(Scene):
    def __init__(self):
        super(TestDirectorScene, self).__init__()
        self._dt = 0
        self._next_scene = None
        self._changetype = 0
        self.schedule(self.timeit)

    def changescene(self):
        if self._next_scene is None:
            pyglet.app.exit()

        if self._changetype == 0:
            director.push(self._next_scene)
        elif self._changetype == 1:
            self._next_scene = None
            director.pop()
        elif self._changetype == 2:
            director.replace(self._next_scene)
        elif self._changetype == 3:
            self._next_scene = None
            director.scene.end(True)

    def timeit(self, dt):
        if self._dt >= 60*5:
            self._dt = 0
            self.changescene()
        else:
            self._dt += 1

    def setnextscene(self, change, scene):
        self._next_scene = scene
        self._changetype = change


def setup_func():
    director.init(width=800, height=600, caption=u"Pruebas Unitarias")

def teardown_func():
    director.window.close()

def test_is_singleton():
    ok_(director is Director(), ("La clase Director() "
                                 "no es un singleton"))

@with_setup(setup_func, teardown_func)
def test_director_init():
    # iniciamos el director con los valores por defecto.
    window = director.window
    ok_(window, "No se inicio director de forma exitosa!")

@with_setup(setup_func, teardown_func)
def test_director_get_window_size():
    one_tuple = director.get_window_size()
    ok_(isinstance(one_tuple, tuple), "El objeto retornado no es una tupla")
    ok_(isinstance(one_tuple[0], int), "El primer objeto de la tupla no es Int")
    ok_(isinstance(one_tuple[1], int), ("El segundo objeto de "
                                        "la tupla no es Int"))
    eq_(one_tuple, (800, 600), ("Las dimensiones de la pantalla "
                                "no son las especificadas en la prueba."
                                " el director ignora las dimensiones."))

@with_setup(setup_func, teardown_func)
def test_director_run():
    bluelayer = ColorLayer(0, 0, 255, 255)
    redlayer = ColorLayer(255, 0, 0, 255)
    greenlayer = ColorLayer(0, 255, 0, 255)
    scene1 = TestDirectorScene()
    scene2 = TestDirectorScene()
    scene3 = TestDirectorScene()
    scene1.add(bluelayer)
    scene2.add(redlayer)
    scene3.add(greenlayer)

    scene1.setnextscene(0, scene2)
    scene2.setnextscene(2, scene3)
    director.run(scene1)
