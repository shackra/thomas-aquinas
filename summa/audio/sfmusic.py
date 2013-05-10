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
from sftime import Time

class Music(ObjectBase):
    u"""
    reproduce la Música del juego.
    """
    _audio.sfMusic_createFromFile.argtypes = [ctypes.c_char_p]
    _audio.sfMusic_setLoop.argtypes = [ctypes.c_bool]
    _audio.sfMusic_setVolume.argtypes = [ctypes.c_float]
    _audio.sfMusic_setPosition.argtypes = [Vector3f]
    _audio.sfMusic_setRelativeToListener.argtypes = [ctypes.c_bool]
    _audio.sfMusic_setMinDistance.argtypes = [ctypes.c_float]
    _audio.sfMusic_setAttenuation.argtypes = [ctypes.c_float]
    _audio.sfMusic_setPlayingOffset.argtypes = [Time]

    #_audio.sfMusic_createFromFile.argtypes = [ctypes.c_char_p]
    _audio.sfMusic_getLoop.restype = ctypes.c_bool
    _audio.sfMusic_getVolume.restype = ctypes.c_float
    _audio.sfMusic_getPosition.restype = Vector3f
    _audio.sfMusic_isRelativeToListener.restype = ctypes.c_bool
    _audio.sfMusic_getMinDistance.restype = ctypes.c_float
    _audio.sfMusic_getAttenuation.restype = ctypes.c_float
    _audio.sfMusic_getPlayingOffset.restype = Time


    def __init__(self):
        super(Music, self).__init__(self)

    def __del__(self):
        _audio.sfMusic_Destroy(self.this)

    @classmethod
    def fromfile(cls, filename):
        u"""
        Crea una instancia de Music y carga los datos desde un archivo.

        Esté metodo no inicia la reproducción de la música (usé play() para hacerlo).
        Esta es una lista completa de los formatos de audio soportados: ogg, wav, flac,
        aiff, au, raw, paf, svx, nist, voc, ircam, w64, mat4, mat5 pvf, htk, sds, avr,
        sd2, caf, wve, mpc2k, rf64.
        """
        music = cls()
        music.this = _audio.sfMusic_createFromFile(filename)

        return music

    @property
    def loop(self):
        u"""
        Indica cuando la música esta o no en modo bucle.
        """
        return _audio.sfMusic_getLoop(self.this)

    @loop.setter
    def loop(self, loop):
        u"""
        Establece si o no se usa el modo bucle para la música.
        """
        _audio.sfMusic_setLoop(self.this, loop)

    @property
    def duration(self):
        u"""
        Retorna la duración total de la música.
        """
        return _audio.sfMusic_getDuration(self.this)

    def play(self):
        u"""
        Inicia la reproducción de música.
        """
        _audio.sfMusic_play(self.this)

    def pause(self):
        u"""
        Pausa la música.
        """
        _audio.sfMusic_pause(self.this)

    def stop(self):
        u"""
        Detiene la reproducción de música
        """
        _audio.sfMusic_stop(self.this)

    @property
    def channelCount(self):
        u"""
        Retorna el numero de canales de la canción.
        """
        return _audio.sfMusic_getChannelCount(self.this)

    @property
    def sampleRate(self):
        u"""
        Retorna el ratio de muestra de la canción.
        """
        return _audio.sfMusic_getSampleRate(self.this)

    @property
    def status(self):
        u"""
        Retorna el estado actual de la musica (detenido, pausado, reproduciendo).
        """
        return _audio.sfMusic_getStatus(self.this)

    @property
    def playingOffset(self):
        u"""
        Obtiene la posición actual de la reproducción de la música.
        """
        return _audio.sfMusic_getPlayingOffset(self.this)

    @playingOffset.setter
    def playingOffset(self, timeOffset):
        u""" Cambia la posicion actual de la reproducción de la música.

        Arguments:
        - `self`:
        - `timeOffset`:
        """
        _audio.sfMusic_setPlayingOffset(self.this, timeOffset)

    @property
    def pitch(self):
        u""" Retorna el pitch de la musica.

        Arguments:
        - `self`:
        """
        return _audio.sfMusic_getPitch(self.this)

    @pitch.setter
    def pitch(self, pitch):
        u"""
        Establece el pitch de la música.
        """
        _audio.sfMusic_setPitch(self.this, pitch)

    @property
    def volume(self):
        u"""
        Retorna el nivel de volumen de la música.
        """
        return _audio.sfMusic_getVolume(self.this)

    @volume.setter
    def volume(self, volume):
        u"""
        Establece el nivel de volumen de la música.
        """
        _audio.sfMusic_setVolume(self.this, volume)

    @property
    def position(self):
        u"""
        Retorna la posición 3D de la música en la escena de audio.
        """
        return _audio.sfMusic_getPosition(self.this)

    @position.setter
    def position(self, position):
        u"""
        Establece la posición 3D de la música en la escena de audio.
        """
        _audio.sfMusic_setPosition(self.this, position)

    @property
    def relativeToListener(self):
        u"""
        Indica si la canción es relativa o absoluta al escucha.
        """
        return _audio.sfMusic_isRelativeToListener(self.this)

    @relativeToListener.setter
    def relativeToListener(self, relative):
        u"""
        Establece si la canción es relativa o absoluta al escucha.
        """
        _audio.sfMusic_setRelativeToListener(self.this, relative)

    @property
    def minDistance(self):
        u"""
        Distancia mínima de la musica.
        """
        return _audio.sfMusic_getMinDistance(self.this)

    @minDistance.setter
    def minDistance(self, distance):
        u"""
        Establece la distancia mínima de la música.
        """
        _audio.sfMusic_setMinDistance(self.this, distance)

    @property
    def attenuation(self):
        u"""
        Factor de atenuación de la música.
        """
        return _audio.sfMusic_getAttenuation(self.this)

    @attenuation.setter
    def attenuation(self, attenuation):
        u"""
        Establece el factor de atenuación de la música.
        """
        _audio.sfMusic_setAttenuation(self.this, attenuation)
