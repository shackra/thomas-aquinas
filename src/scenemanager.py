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
import common
import sfml

class Director:
    """Objeto principal del juego.

    Aqui es donde sucede toda la magia. Dibujamos, actualizamos
    y propagamos eventos entre clases derivadas de 
    la clase AbstractScene.

    El diseño de esta clase esta fuertemente basada en director.py
    del proyecto Asadetris desarrollado por Hugo de LosersJuegos"""

    def __init__(self):
        self.window = sfml.RenderWindow(sfml.VideoMode(
            common.settings.getscreensize()), common.settings.getscreentitle())
        self.window.framerate_limit = 60

        self.__actualscene = None
        self.__fullscreenmode = False
        self.__exit_game = False
        # revisar si hay Joysticks conectados al PC.

    def loop(self):
        "¡El juego se pone en marcha!"

        timesleep = sfml.system.Time
        timesleep.microseconds = 10000

        while not self.__exit_game:
            # propagacion de eventos
            for event in self.window.events:
                if type(event) is sfml.CloseEvent:
                    self.__exit_game = True
                elif type(event) is sfml.KeyEvent and event.pressed:
                    # alternamos entre modo pantalla completa y modo ventana
                    self.alternatefullscreen()

                    # Le pasamos el evento a la escena para que haga algo
                    self.__actualscene.on_event(event)

            # actualizamos la escena
            self.__actualscene.on_update()
            sfml.sleep(timesleep)

            # dibujamos la escena
            self.window.clear(sfml.Color.BLACK)
            self.__actualscene.on_draw(self.window)
            self.window.display()

        ## GAME OVER!
        common.conf.saveconf()
        self.window.close()

    def changescene(self, scene):
        "Cambia la escena actual."
        self.__actualscene = scene

    def alternatefullscreen(self):
        "Alterna entre modo pantalla completa y modo ventana"
