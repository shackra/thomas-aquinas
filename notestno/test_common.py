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
#    def test_loadedconf(self):
#        ok_(isinstance(common.settings, common.Conf))

    def test_userfolderget(self):
        path = common.Conf.fromuserfolderget("test")
        eq_(path, "/home/jorge/.thomas-aquinas/test")

    def test_rootfolderget(self):
        path = common.Conf.fromrootfolderget("test")
        eq_(path, u"/home/jorge/coders/desarrollo"
            "/thomas-aquinas/data/test")

    def test_getuserfolder(self):
        path = common.Conf.getuserfolder()
        eq_(path, "/home/jorge/.thomas-aquinas")

    def test_getrootfolder(self):
        path = common.Conf.getrootfolder()
        eq_(path, u"/home/jorge/coders/desarrollo"
            "/thomas-aquinas/data/")

    def test_joinpaths(self):
        path = common.Conf.joinpaths("this", "should", "work")
        eq_(path, u"this/should/work")

    def test_joinpathsrmdoubleslash(self):
        path = common.Conf.joinpaths("should/", "work")
        eq_(path, u"should/work")

    def test_getosname(self):
        osname = common.Conf.getosname()
        eq_(osname, "posix")

    def test_getscreensize(self):
        screensize = common.Conf.getscreensize()
        eq_(screensize, (320, 240))

    def test_setscreensize(self):
        common.Conf.setscreensize((1024, 768))
        newscreensize = common.Conf.getscreensize()
        eq_(newscreensize, (1024, 768))
        common.Conf.setscreensize((320, 240))

    def test_getscreentitle(self):
        title = common.Conf.getscreentitle()
        eq_(title, "Prueba")

    def test_setscreentitle(self):
        common.Conf.setscreentitle("hola mundo")
        newtitle = common.Conf.getscreentitle()
        eq_(newtitle, "hola mundo")

    def test_getcontrollerbutton(self):
        button = common.Conf.getcontrollerbutton("action_button")
        eq_(button, 57)

    def test_setcontrollerbutton(self):
        common.Conf.setcontrollerbutton("action_button", 1)
        newbutton = common.Conf.getcontrollerbutton("action_button")
        eq_(newbutton, 1)

    def test_usingkeyboard(self):
        result = common.Conf.usingkeyboard()
        ok_(result)

    def test_usingjoysitck(self):
        result = common.Conf.usingjoystick()
        ok_(not result)

    def test_alternatecontrollertype(self):
        common.Conf.alternatecontrollertype()
        result = common.Conf.usingjoystick()
        ok_(result, "No se cambio el valor")
