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
import sfml
from lib import media

class TestLoadstuff:
    def test_loadtex(self):
        texture = media.loadmedia("uniteststuff/imgtex.png", toram=False)
        nose.tools.ok_(texture, "Se a cargado algo en la variable texture")
        nose.tools.ok_(isinstance(texture, sfml.Texture),
                       "Una textura se a cargado correctamente")

    def test_loadimg(self):
        img = media.loadmedia("uniteststuff/imgtex.png")
        nose.tools.ok_(img, "Se a cargado algo en la variable img")
        nose.tools.ok_(isinstance(img, sfml.Image),
                       "Una imagen se a cargado correctamente")

    def test_loadsnd(self):
        snd = media.loadmedia("uniteststuff/sound.flac", mediatype="snd")
        nose.tools.ok_(snd, "Se a cargado algo en la variable snd")
        nose.tools.ok_(isinstance(snd, sfml.Sound),
                       "Un sonido se a cargado correctamente")

    def test_loadmsc(self):
        msc = media.loadmedia("uniteststuff/cattails.ogg", mediatype="msc")
        nose.tools.ok_(msc, "Se a cargado algo en la variable msc")
        nose.tools.ok_(isinstance(msc, sfml.Music),
                       "Una musica se a cargado correctamente")

    @nose.tools.raises(IOError, media.TAUnknownFileFormatException)
    def test_fail_loadtex(self):
        tex1 = media.loadmedia("uniteststuff/file.fail", toram=False)

    @nose.tools.raises(IOError)
    def test_fail_loadimg(self):
        tex2 = media.loadimg("uniteststuff/sound.flac")

    @nose.tools.raises(IOError)
    def test_fail_loadsnd(self):
        snd = media.loadsound("uniteststuff/imgtex.png")

    @nose.tools.raises(IOError)
    def test_fail_loadmsc(self):
        msc = media.loadsong("/uniteststuff/imgtex.png")
