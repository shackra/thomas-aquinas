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

import ctypes
import logging
from libs import _audio
from vector import Vector3f
from objectbase import ObjectBase

class Music(ObjectBase):
    """
    reproduce la Música del juego.
    """
    _audio.sfMusic_createFromFile.argtypes = [ctypes.c_char_p]
    def __init__(self):
        super()
        raise UserError("Así no me instancies")

    @classmethod
    def fromfile(cls, filename):
        """
        Crea una instancia de Music y carga los datos desde un archivo.

        Esté metodo no inicia la reproducción de la música (usé play() para hacerlo).
        Esta es una lista completa de los formatos de audio soportados: ogg, wav, flac,
        aiff, au, raw, paf, svx, nist, voc, ircam, w64, mat4, mat5 pvf, htk, sds, avr,
        sd2, caf, wve, mpc2k, rf64.
        """
        music = cls()
        music.this = _audio.sfMusic_createFromFile(filename)

        return music
