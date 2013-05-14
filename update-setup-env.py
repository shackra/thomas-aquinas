#!/usr/bin/env python2
# coding: utf-8
# Thomas-Aquinas: a 2D game framework based on Cocos2D
# Copyright (C) 2012 Jorge Javier Araya Navarro <jorgean@lavabit.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import virtualenv, textwrap

extra_text = """
import os, subprocess, sys
def after_install(options, home_dir):
    if sys.platform == "win32":
        bin = "Scripts"
        startenv = [os.path.join(home_dir, bin, "activate")]
    else:
        bin = "bin"
        startenv = ["source", os.path.join(home_dir, bin, "activate")]

    easyinstall = os.path.join(home_dir, bin, 'easy_install')
    pyglet = [easyinstall, 'pyglet==1.1.4']
    # instalando los paquetes dentro del entorno
    subprocess.call(pyglet)
    """

salida = virtualenv.create_bootstrap_script(textwrap.dedent(extra_text))

with open("setup-env.py", "w") as archivo:
    archivo.write(salida)
