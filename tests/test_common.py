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
from lib import common

class TestCommon:
    def test_loadedconf(self):
        ok_(isinstance(common.settings, common.Conf))

    def test_userfolderget(self):
        path = common.settings.fromuserfolderget("test")
        eq_(path, "/home/jorge/.thomas-aquinas/test")

    def test_rootfolderget(self):
        path = common.settings.fromrootfolderget("test")
        eq_(path, u"/home/jorge/coders/desarrollo"
            "/thomas-aquinas/data/test")

    def test_getuserfolder(self):
        path = common.settings.getuserfolder()
        eq_(path, "/home/jorge/.thomas-aquinas")

    def test_getrootfolder(self):
        path = common.settings.getrootfolder()
        eq_(path, u"/home/jorge/coders/desarrollo"
            "/thomas-aquinas/data/")

    def test_joinpaths(self):
        path = common.settings.joinpaths("this", "should", "work")
        eq_(path, u"this/should/work")

    def test_joinpathsrmdoubleslash(self):
        path = common.settings.joinpaths("should/", "work")
        eq_(path, u"should/work")

    def test_getosname(self):
        osname = common.settings.getosname()
        eq_(osname, "posix")

    def test_getscreensize(self):
        screensize = common.settings.getscreensize()
        eq_(screensize, (800, 600))

    def test_setscreensize(self):
        common.settings.setscreensize((1024, 768))
        newscreensize = common.settings.getscreensize()
        eq_(newscreensize, (1024, 768))

    def test_getscreentitle(self):
        title = common.settings.getscreentitle()
        eq_(title, "Probando el framework Thomas de Aquino")

    def test_setscreentitle(self):
        common.settings.setscreentitle("hola mundo")
        newtitle = common.settings.getscreentitle()
        eq_(newtitle, "hola mundo")

    def test_getcontrollerbutton(self):
        button = common.settings.getcontrollerbutton("action_button")
        eq_(button, 57)

    def test_setcontrollerbutton(self):
        common.settings.setcontrollerbutton("action_button", 1)
        newbutton = common.settings.getcontrollerbutton("action_button")
        eq_(newbutton, 1)

    def test_usingkeyboard(self):
        result = common.settings.usingkeyboard()
        ok_(result)

    def test_usingjoysitck(self):
        result = common.settings.usingjoystick()
        ok_(not result)

    def test_alternatecontrollertype(self):
        common.settings.alternatecontrollertype()
        result = common.settings.usingjoystick()
        ok_(result, "No se cambio el valor")
        
