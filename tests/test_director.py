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

import customstuff

def test_is_singleton():
    ok_(director is Director(), ("La clase Director() "
                                 "no es un singleton"))

def test_director_init():
    # Debido a que la clase Director es algo difícil de testear
    # sin que tire una excepción de fallo de segmentación
    # probare varias cosas relacionadas con esta clase
    # en una sola prueba.
    director.init(width=800, height=600, caption=u"Pruebas Unitarias")
    window = director.window
    ok_(window, "No se inicio director de forma exitosa!")
    one_tuple = director.get_window_size()
    ok_(isinstance(one_tuple, tuple), "El objeto retornado no es una tupla")
    ok_(isinstance(one_tuple[0], int), "El primer objeto de la tupla no es Int")
    ok_(isinstance(one_tuple[1], int), ("El segundo objeto de "
                                        "la tupla no es Int"))
    eq_(one_tuple, (800, 600), ("Las dimensiones de la pantalla "
                                "no son las especificadas en la prueba."
                                " el director ignora las dimensiones."))
    bluelayer = ColorLayer(0, 0, 255, 255)
    redlayer = ColorLayer(255, 0, 0, 255)
    greenlayer = ColorLayer(0, 255, 0, 255)
    scene1 = customstuff.TimedScene()
    scene2 = customstuff.TimedScene()
    scene3 = customstuff.TimedScene()
    scene1.add(bluelayer)
    scene2.add(redlayer)
    scene3.add(greenlayer)

    scene1.setnextscene(0, scene2)
    scene2.setnextscene(2, scene3)
    director.run(scene1)
