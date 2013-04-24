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
from libs import _system

class Time(ctypes.Structure):
    """
    Represents a time value.
    """
    _fields_ = [
        ("microseconds", ctypes.c_int64)
    ]

    def __repr__(self):
        return "<Time: {} microseconds, {} milliseconds, {} seconds>".format(self.microseconds,
                                                                             self.milliseconds,
                                                                             self.seconds)

    @property
    def seconds(self):
        return sfTime_asSeconds(self)

    @property
    def milliseconds(self):
        return sfTime_asMilliseconds(self)

    @property
    def microseconds(self):
        return sfTime_asMicroseconds(self)


def sfTime_asSeconds(time):
    """
    Método privado que devuelve la estructura de tiempo en segundos.
    """
    _system.sfTime_asSeconds.argtypes = [Time]
    _system.sfTime_asSeconds.restype = ctypes.c_float
    return _system.sfTime_asSeconds(time)

def sfTime_asMilliseconds(time):
    """
    Método privado que devuelve la estructura de tiempo en milisegundos.
    """
    _system.sfTime_asMilliseconds.argtypes = [Time]
    _system.sfTime_asMilliseconds.restype = ctypes.c_int32
    return _system.sfTime_asMilliseconds(time)

def sfTime_asMicroseconds(time):
    """
    Método privado que devuelve la estructura de tiempo en microsegundos
    """
    _system.sfTime_asMicroseconds.argtypes = [Time]
    _system.sfTime_asMicroseconds.restype = ctypes.c_int64
    return _system.sfTime_asMicroseconds(time)

def Seconds(amount):
    """
    """
    _system.sfSeconds.argtypes = [ctypes.c_float]
    _system.sfSeconds.restype = Time
    return _system.sfSeconds(float(amount) if not isinstance(amount, float) else amount)

def Milliseconds(amount):
    """
    """
    _system.sfMilliseconds.argtypes = [ctypes.c_int32]
    _system.sfMilliseconds.restype = Time
    return _system.sfMilliseconds(amount)

def Microseconds(amount):
    _system.sfMicroseconds.argtypes = [ctypes.c_int64]
    _system.sfMicroseconds.restype = Time
    return _system.sfMicroseconds(amount)
