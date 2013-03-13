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

import logging
import nose
from nose.tools import ok_, eq_, raises
from lib.spritefactory import Entity
from lib import media

import sfml

class TestEntity:
    @classmethod
    def setup_class(cls):
        print ("Creando una ventana SFML")
        global window
        global tex
        window = sfml.RenderWindow(sfml.VideoMode(320, 240),
                                   "Test_spritefactory")
        tex = media.loadimg("uniteststuff/test.png", False)

    def test_entitybuild(self):
        entity = Entity("test", tex, window, None, None)
        eq_(entity.id, "test")
        ok_(isinstance(entity.sprite, sfml.Sprite),
            "La entidad no tiene un objet sprite")
        ok_(isinstance(entity.clock, sfml.Clock),
            "La entidad no tiene un objeto clock")
        eq_(entity.zindex, None)
        
