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
from vector import Vector3f
from libs import _audio


class Listener(object):
    """
    Define la posición de escucha.
    """

    __singleton = None

    _audio.sfListener_setGlobalVolume.argtypes = [ctypes.c_float]
    _audio.sfListener_setPosition.argtypes = [Vector3f]
    _audio.sfListener_setDirection.argtypes = [Vector3f]

    _audio.sfListener_getGlobalVolume.restype = ctypes.c_float
    _audio.sfListener_getPosition.restype = Vector3f
    _audio.sfListener_getDirection.restype = Vector3f

    def __new__(cls):
        if cls.__singleton is None:
            cls.__singleton = super(Listener, cls).__new__(cls)
        return cls.__singleton

    @property
    def volume(self):
        """
        Retorna el volumen global.
        """
        return _audio.sfListener_getGlobalVolume()

    @volume.setter
    def volume(self, volume):
        """
        Cambia el volumen global de todos los sonidos y la musica
        el volumen es un numero entre 0 y 100; es combinado con el
        volumen de cada sonido/canción. El volumen por defecto es
        de 100 (el máximo)
        """
        _audio.sfListener_setGlobalVolume(float(volume))

    @property
    def position(self):
        """
        Obtiene la posición actual del escucha en la escena.
        """
        return _audio.sfListener_getPosition()

    @position.setter
    def position(self, position):
        """
        Define la posición del escucha en la escena.

        La posición por defecto del escucha es (0, 0, 0).
        """
        _audio.sfListener_setPostion(position)

    @property
    def direction(self):
        """
        Obtiene la orientación actual del escucha en la escena.
        """
        return _audio.sfListener_getDirection()

    @direction.setter
    def direction(self, orentation):
        """
        Establece la orientación del escucha en la escena.

        La orientación define los ejes 3D del escucha (izquierda, arriba, frente)
        en la escena. El vector de la orientación no tiene que ser normalizado.
        por defecto, la orientación del escucha es (0, 0, -1).
        """
        _audio.sfListener_setDirection(orentation)
