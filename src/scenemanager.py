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
class TAAttrIsNotScene(Exception): pass

class Director:
    """Objeto principal del juego.

    Aquí es donde sucede toda la magia. Dibujamos, actualizamos
    y propagamos eventos entre clases derivadas de 
    la clase AbstractScene.

    El diseño de esta clase esta fuertemente basada en director.py
    del proyecto Asadetris desarrollado por Hugo de LosersJuegos"""

    def __init__(self, icon=None):
        self.window = sfml.RenderWindow(sfml.VideoMode(
            common.settings.getscreensize()[0], 
            common.settings.getscreensize()[1]),
                                        common.settings.getscreentitle())
        self.window.framerate_limit = 60
        if icon: 
            self.window.icon = media.loadmedia(icon).pixels

        self.__actualscene = None
        self.__fullscreenmode = False
        self.__exitgame = False
        # revisar si hay Joysticks conectados al PC.
        self.__globalvariables = {}
        
        # Iniciamos algunas variables globales
        self.setglobalvariable("game title",
                               common.settings.getscreentitle())

    def __getitem__(self, item):
        return self.__globalvariables[str(item)]

    def __iter__(self):
        return self.__globalvariables.items()

    def loop(self):
        "¡El juego se pone en marcha!"

        timesleep = sfml.milliseconds(10)

        while not self.__exitgame:
            # propagación de eventos
            for event in self.window.events:
                if type(event) is sfml.CloseEvent:
                    self.__exitgame = True
                    logging.info("Cerrando el programa...")
                    logging.info("Salvando la configuracion...")
                    common.settings.saveconf()
                    logging.info("Configuracion del juego salvada!")
                    # logging.info("Guardando las variables globales...")
                    # pass
                    # logging.info("Variables globales salvadas!")
                    logging.info("¡Gracias por jugar!")
                elif type(event) is sfml.KeyEvent and event.pressed:
                    if event.code is sfml.Keyboard.F3:
                        # alternamos entre modo pantalla completa y modo ventana
                        self.alternatefullscreenmode()

                # Le pasamos el evento a la escena para que haga algo
                try:
                    self.__actualscene.on_event(event)
                except AttributeError:
                    raise TAAttrIsNotScene, ("Objeto {0} no es "
                                             "instancia de SceneFactory".format(
                                             type(self.__actualscene)))
                ## TODO:
                # Le pasamos el evento al dialogo para que haga algo
                #self.__widgetmanager.on_event(event)

            # actualizamos la escena
            try:
                self.__actualscene.on_update()
            except AttributeError:
                raise TAAttrIsNotScene, ("Objeto {0} no es "
                                         "instancia de SceneFactory".format(
                                             type(self.__actualscene)))
            
            # dibujamos la escena
            self.window.clear(sfml.Color.BLACK)
            try:
                self.__actualscene.on_draw(self.window)
            except AttributeError:
                raise TAAttrIsNotScene, ("Objeto {0} no es "
                                         "instancia de SceneFactory".format(
                                             type(self.__actualscene)))
            # TODO: crear un sistema de widgets personalisable
            #   con CSS.
            # TODO: Dibujamos los widgets
            # self.__widgetmanager.on_draw(self.window)
            self.window.display()

            # dormimos la aplicación unos milisegundos
            sfml.sleep(timesleep)

        ## GAME OVER!
        
        self.window.close()

    def changescene(self, scene):
        "Cambia la escena actual."
        self.__actualscene = scene

    def alternatefullscreenmode(self):
        "Alterna entre modo pantalla completa y modo ventana"
        if not self.__fullscreenmode:
            self.window.recreate(
                sfml.VideoMode(self.window.width,
                               self.window.height), 
                self.getglobalvariable("game title"),
                sfml.Style.FULLSCREEN)
            self.__fullscreenmode = True
        else:
            self.window.recreate(
                sfml.VideoMode(self.window.width,
                               self.window.height), 
                self.getglobalvariable("game title"))
            self.__fullscreenmode = False

    def setglobalvariable(self, name, value):
        """ Crea una variable global a la cual cualquier escena puede acceder.

        es algo difícil compartir datos entre escenas, por ello se usara la
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