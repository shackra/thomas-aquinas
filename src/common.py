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
import os
import ConfigParser

class Conf:
    def __init__(self, gamefolder, configurationfiles):
        self.loadconf(configurationfiles)
        self._checkconf()
        self.__os = os.name
        
        if self.__os == "posix":
            self.__USERFOLDER = self.joinpaths(os.environ["HOME"], ".{game}")

            if self.__parsed.has_option("DATA_PATH", "root_path"):
                self.__ROOTFOLDER = self.__parsed.get("DATA_PATH", "root_path")
            else:
                self.__ROOTFOLDER = "/usr/share/games/{game}"

        elif self.__os == "nt":
            self.__USERFOLDER = self.joinpaths(os.environ["APPDATA"], "{game}")

            if self.__parsed.has_option("DATA_PATH", "root_path"):
                self.__ROOTFOLDER = self.__parsed.get("DATA_PATH", "root_path")
            else:
                self.__ROOTFOLDER = self.joinpaths(os.environ["PROGRAMFILES"],
                                               "{game}")
        
        self.__USERFOLDER = self.__USERFOLDER.format(game=gamefolder)
        self.__ROOTFOLDER = self.__ROOTFOLDER.format(game=gamefolder)
        
    def loadconf(self, configurationfiles=None):
        """ Carga la configuracion del juego y del usuario u otras.
        
        Si configurationfiles es una cadena o una lista de cadenas de texto
        los usara 
        """
        if configurationfiles:
            self.confilepath = self.__convertpath(configurationfiles)
            self.__parsed = ConfigParser.SafeConfigParser()
            self.__parsed(self.confilepath)
        else:
            # queremos recargar la configuracion, eh?
            self.__parsed(self.confilepath)

    def saveconf(self, onuserfolder=True, filepath=None):
        """ Salva la configuracion actual en un archivo ini.
        
        Si onuserfolder es verdadero, se guardara toda la configuracion
        en la carpeta personal del usuario. De lo contrario se guardara
        en el archivo especificado por filepath.

        en caso de problemas de escritura en filepath, se escribira
        el archivo de configuracion en la carpeta del usuario."""
        
        confilepath = None
        
        if onuserfolder:
            try:
                confilepath = open(
                    self.joinpaths(self.getuserdir(), "gameconf.ini"), "w")
            except IOError:
                # logging
                raise
        else:
            if filepath and isinstance(filepath, str):
                try:
                    confilepath = open(
                    self.__convertpath(filepath), "w")
                except IOError:
                    # logging
                    confilepath = open(
                        self.joinpaths(self.getuserdir(), "gameconf.ini"), "w")
            else:
                # logging
                try:
                    confilepath = open(
                        self.joinpaths(self.getuserdir(), "gameconf.ini"), "w")
                except IOError:
                    # logging
                    raise

        self.__parsed.write(confilepath)
        confilepath.close()

    def fromuserfolderget(self, *args):
        """ Retorna una direccion absoluta del directorio en la carpeta personal
        """
        return self.joinpaths(self.getuserfolder(), args)

    def fromrootfolderget(self, *args):
        """ Retorna una direccion absoluta desde el directorio del juego.
        """
        return self.joinpaths(self.getrootfolder(), args)

    def getuserdir(self):
        """ Retorna el directorio personal del usuario.
        """
        return self.__convertpath(self.__USERFOLDER)

    def getrootfolder(self):
        """ Retorna el directorio donde se almacena el juego.
        """
        return self.__convertpath(self.__ROOTFOLDER)

    def joinpaths(*args):
        """ Retorna una direccion de archivo juntando todos los argumentos.
        """
        argspath = ""
        for arg in args:
            argspath = arg + "/"

        return self.__convertpath(argspath)

    def __convertpath(self, whichone):
        """ Convierte y retorna direcciones de archivos de forma adecuada.

        Para cualquier direccion de archivos se usara las barras inclinadas,
        incluso para archivos dentro de Windows. Éste metodo se encargara
        de retornar la dirección correcta del archivo, según el sistema
        operativo en uso.
        En caso de que whichone sea una lista, se iterara la lista y se
        devolvera el mismo tipo con las direcciones corregidas."""
        if isinstance(whichone, str):
            try:
                unicodewhichone = whichone.decode("utf-8")
            except:
                unicodewhichone = whichone
                if self.__os == "nt":
                    return unicodewhichone.replace("/", "\\")
                else:
                    return unicodewhichone
        elif isinstance(whichone, list):
            pathlist = []
            for thisone in whichone:
                pathlist.append(self.__convertpath(thisone))
            return pathlist
        else:
            raise ValueError, "argument is not a str or list object"

    def _checkconf(self):
        """ Revisa que los datos basicos existan.
        
        Deben existir algunos datos basicos sobre la configuracion
        los cuales los juegos necesitan para funcionar de forma apropiada.
        En caso de faltar algun valor, el juego DEBERIA cerrarse y notificar
        al usuario."""
        problem = None
        # Variables que contienen la ubicacion de los archivos audiovisuales
        if self.__parsed.has_section("DATA_PATH"):
            for opcion in ["root_path", "common_data"]:
                if not self.__parsed.has_option("DATA_PATH", opcion):
                    problem = (opcion, "option")
                    break
        else:
            problem = ("DATA_PATH", "section")
        
        # Variables que contienen la distribucion basica de los botones del
        # control del jugador.
        if self.__parsed.has_section("CONTROLLER"):
            for opcion in ["action_button", "cancel_button", "pause_button",
                           "up_button", "down_button", "left_button", 
                           "right_button", "keyboard_or_joystick"]:
                if not self.__parsed.has_option("CONTROLLER", opcion):
                    problem = (opcion, "option")
                    break
        else:
            problem = ("CONTROLLER", "section")

        # Variables que contienen los valores de configuracion de visualizacion
        # del juego.
        if self.__parsed.has_section("DISPLAY"):
            for opcion in ["screen_size", "window_title"]:
                if not self.__parsed.has_option("DISPLAY", opcion):
                    problem = (opcion, "option")
                    break
        else:
            problem = ("DISPLAY", "section")

        # Finalmente disparamos una excepcion
        if problem: raise Exception, problem
            
    def getosname():
        """ Retorna el nombre del sistema operativo.

        nt: para cualquier sistema operativo Windows.
        posix: para cualquier sistema operativo
        derivado de Unix (GNU/Linux, *BSD)"""
        return self.__os

    def getscreensize(self):
        """ Retorna una tupla con las dimensiones de la pantalla del juego.
        """
        sizestring = self.__parsed.get("DISPLAY", "screen_size")
        # partimos la cadena, convertimos a entero y ponemos todo en una tupla
        # es de esperar que las dimensiones de la pantalla se expresen como
        # 320x240 por ejemplo.
        size = (int(sizestring.split("x")[0]), int(sizestring.split("x")[1]))
        return size

    def setscreensize(self, (width, height)):
        """ Guarda el nuevo tamaño de la pantalla del juego.

        Este dato no sera guardado en un archivo de configuracion hasta llamar
        al metodo saveconf().
        """
        sizestring = "{w}x{h}".format(w=width, h=height)
        self.__parsed.set("DISPLAY", "screen_size", sizestring)

    def getscreentitle(self):
        """ Retorna el texto a mostrar en la barra de titulo del juego.
        """
        return self.__parsed.get("DISPLAY", "window_title").decode("utf-8")

    def setscreentitle(self, title):
        """ Guarda el nuevo texto de la barra de titulo del juego
        """
        self.__parsed.set("DISPLAY", "window_title", title)

    def getcontrollerbutton(self, button):
        """ Retorna el codigo SFML de la tecla perteneciente al boton especifico

        el argumento button puede ser cualquier cosa, aunque usualmente puede
        pedirse las teclas asignadas para action_button, cancel_button,
        pause_button, etc.
        """
        return self.__parsed.getint("CONTROLLER", str(button))

    def setcontrollerbutton(self, button, code):
        """ Guarda un boton con su respectivo codigo numerico.

        Este dato no sera guardado en un archivo de configuracion hasta llamar
        al metodo saveconf().
        """
        self.__parsed.set("CONTROLLER", str(button), code)

    def usingkeyboard(self):
        """ Retorna verdadero si se esta usando el teclado.
        """
        if self.__parsed.getboolean("CONTROLLER", "keyboard_or_joystick"):
            return True
        else:
            return False

    def usingjoystick(self):
        """ Retorna verdadero si se esta usando un joystick
        """
        if self.__parsed.getboolean("CONTROLLER", "keyboard_or_joystick"):
            return False
        else:
            return True


def __name__ != "__main__":
    # Esta linea a de cambiarse segun el proyecto en el que se use el modulo
    conf = Conf("gameconf.ini")