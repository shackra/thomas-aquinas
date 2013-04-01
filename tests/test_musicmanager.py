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


from lib import media
import nose
from nose.tools import ok_, eq_, raises
from time import sleep
import logging

class TestMusicManager:
    @classmethod
    def teardown_class(cls):
        media.MusicManager.songs = {}

    @raises(UserWarning)
    def test_raisewarning(self):
        fail = media.MusicManager()

    def test_loadsong(self):
        media.MusicManager.loadsong("uniteststuff/cattails.ogg")
        ok_(media.MusicManager.songs.has_key("cattails.ogg"),
            "La canción no se cargo")

    @raises(UserWarning)
    def test_loadsongtwice(self):
        media.MusicManager.loadsong("uniteststuff/cattails.ogg")

    def test_playsong(self):
        logging.info("Se esta reproduciendo la canción: cattails.ogg")
        media.MusicManager.playsong("cattails.ogg", loop=False)
        logging.info("Se detendrá la reproducción en 10 segundos...")
        sleep(10)
        media.MusicManager.stopsong()
        logging.info("Reproducción detenida de forma exitosa.")

    def test_playsongthenpause(self):
        logging.info("Se esta reproduciendo la canción: cattails.ogg")
        media.MusicManager.playsong("cattails.ogg", loop=False)
        logging.info("Se pausara la reproducción en 5 segundos...")
        sleep(5)
        media.MusicManager.pausesong()
        logging.info("Reproducción pausada. "
                     "se continuara dentro de 5 segundos...")
        sleep(5)
        logging.info("Se continua con la reproducción..."
                     " En 10 segundos se detendra")
        media.MusicManager.unpausesong()
        sleep(10)
        media.MusicManager.stopsong()

    def test_playsongthenchangesong(self):
        media.MusicManager.loadsong("uniteststuff/Movement Proposition.ogg")
        logging.info("Se esta reproduciendo la canción: cattails.ogg")
        media.MusicManager.playsong("cattails.ogg", loop=False)
        logging.info("Se cambiara la canción en 10 segundos...")
        sleep(10)
        media.MusicManager.fadeoutandplaysong(5, "Movement Proposition.ogg",
                                              0, False)
        for i in xrange(10):
            media.MusicManager.updatetweener(1)
            sleep(0.6)
        sleep(10)
        media.MusicManager.stopsong()
