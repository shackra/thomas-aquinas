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
import media

class TAGlobalVariableException(Exception): pass

class Director:
    """Objeto principal del juego.

    Aqui es donde sucede toda la magia. Dibujamos, actualizamos
    y propagamos eventos entre clases derivadas de 
    la clase AbstractScene.

    El diseño de esta clase esta fuertemente basada en director.py
    del proyecto Asadetris desarrollado por Hugo de LosersJuegos"""

    def __init__(self, icon):
        self.window = sfml.RenderWindow(sfml.VideoMode(
            common.settings.getscreensize()), common.settings.getscreentitle())
        self.window.framerate_limit = 60
        self.window.icon = media.loadmedia("icon.png")

        self.__actualscene = None
        self.__fullscreenmode = False
        self.__exitgame = False
        # revisar si hay Joysticks conectados al PC.
        self.__globalvariables = {}

    def __getitem__(self, item):
        return self.__globalvariables[str(item)]

    def __iter__(self):
        return self.__globalvariables.items()

    def loop(self):
        "¡El juego se pone en marcha!"

        timesleep = sfml.system.Time
        timesleep.microseconds = 10000

        while not self.__exitgame:
            # propagacion de eventos
            for event in self.window.events:
                if type(event) is sfml.CloseEvent:
                    self.__exitgame = True
                elif type(event) is sfml.KeyEvent and event.pressed:
                    if event.code is sfml.Keyboard.F3:
                        # alternamos entre modo pantalla completa y modo ventana
                        self.alternatefullscreen()

                # Le pasamos el evento a la escena para que haga algo
                self.__actualscene.on_event(event)
                ## TODO:
                # Le pasamos el evento al dialogo para que haga algo
                #self.__widgetmanager.on_event(event)

            # actualizamos la escena
            self.__actualscene.on_update()
            sfml.sleep(timesleep)

            # dibujamos la escena
            self.window.clear(sfml.Color.BLACK)
            self.__actualscene.on_draw(self.window)
            # TODO: crear un sistema de widgets personalizable
            #   con CSS.
            # TODO: Dibujamos los widgets
            # self.__widgetmanager.on_draw(self.window)
            self.window.display()

        ## GAME OVER!
        common.conf.saveconf()
        self.window.close()

    def changescene(self, scene):
        "Cambia la escena actual."
        self.__actualscene = scene

    def alternatefullscreenmode(self):
        "Alterna entre modo pantalla completa y modo ventana"
        if not self.__fullscreenmode:
            self.window = self.window.recreate(
                sfml.VideoMode(self.window.width,
                               self.window.height), 
                self.window.title,
                sfml.Style.FULLSCREEN)
            self.__fullscreenmode = True
        else:
            self.window = self.window.recreate(
                sfml.VideoMode(self.window.width,
                               self.window.height), 
                self.window.title)
            self.__fullscreenmode = False

    def setglobalvariable(self, name, value):
        """ Crea una variable global a la cual cualquier escena puede acceder.

        es algo dificil compartir datos entre escenas, por ello se usara la
        clase Director para almacenar variables que luego puedan ser usadas
        por otras escenas.
        """
        self.__globalvariables[str(name)] = value

    def getglobalvariable(self, name):
        """ Retorna alguna el valor de alguna variable global.
        """
        if self.__globalvariables.has_key(str(name)):
            return self.__globalvariables[str(name)]
        else:
            raise TAGlobalVariableException, "{0} variable no definida".format(
                name)

    def delglobalvariable(self, name):
        """ Borra una variable global previamente definida.
        """
        if self.__globalvariables.has_key(str(name)):
            self.__globalvariables.pop(str(name))