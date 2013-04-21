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
import platform
import os
import logging

""" Cargamos las librerías compartidas o los DLLs.
"""

platos = platform.system()
arch = str(ctypes.sizeof(ctypes.c_voidp) * 8)
libnames = {"gnu": ("libsfml-audio.so.2.0", "libsfml-system.so.2.0"),
            "osx": ("libcsfml-audio.2.0.dylib", "libcsfml-system.2.0.dylib"),
            "win": ("csfml-audio-2.dll", "csfml-system-2.dll")}

# instancias de las librerías ctypes cargadas
_audio = None
_system = None
__libpath = os.path.dirname(os.path.abspath(__file__))
#__libpath = os.path.dirname(os.path.abspath(sys.executable))

# Alias a la función del modulo ctypes; para GNU y OSX
__xdll = ctypes.cdll

if platos in ("Windows", "Microsoft"):
    __os = "win"
    __xdll = ctypes.windll
    arch = "32"

elif platos == "Darwin":
    __os = "osx"
    arch = "32"

elif platos in ("Linux", "FreeBSD"):
    __os = "gnu"

# cargamos las librerías propiamente dichas
try:
    __path = os.path.join(__libpath, "lib", __os, arch)
    _audio = __xdll.LoadLibrary(os.path.join(__path, libnames[__os][0]))
    _system = __xdll.LoadLibrary(os.path.join(__path, libnames[__os][1]))
except (WindowsError, OSError) as e:
    logging.critical("{} or {} do not exists or "
                     "were changed for other(s) file(s) "
                     "or is corrupted, details: {}".format(libnames[__os][0],
                                                           libnames[__os][1],
                                                           e))
    raise
