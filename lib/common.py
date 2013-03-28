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
import chardet

LOGGING_FORMAT = "%(levelname)s - #%(lineno)d - %(funcName)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)

class TAConfOptionException(Exception): pass
class TAConfSectionException(Exception): pass
class TAConfFailException(Exception): pass


class Conf:
    __os = os.name
    __gamefolder = None
    confilepath = None
    __parsed = ConfigParser.SafeConfigParser()
    
    def __init__(self):
        raise UserWarning, "No me instancies!"

    @classmethod
    def loadconf(cls, gamefolder, configurationfiles=None):
        """ Carga la configuración del juego y del usuario u otras.

        Si configurationfiles es una cadena o una lista de cadenas de texto
        los usara.

        Si existe alguna configuración guardada en la carpeta del juego que
        reside en la carpeta personal del usuario, la carga junto con la
        configuración principal del proyecto.
        """
        
        cls.__gamefolder = gamefolder
        
        if cls.getosname() != "nt":
            cls.__USERFOLDER = cls.joinpaths(os.environ["HOME"],
                                               ".{game}")
        else:
            cls.__USERFOLDER = cls.joinpaths(os.environ["APPDATA"],
                                               "{game}")

        cls.__USERFOLDER = cls.__USERFOLDER.format(
            game=cls.__gamefolder)

        # verificando que la carpeta del juego exista en la carpeta
        # personal del usuario.
        if not os.path.isdir(cls.__USERFOLDER):
            os.mkdir(cls.__USERFOLDER)

        # ¿Existe una configuración del usuario guardada con anterioridad?
        usergameconf = cls.fromuserfolderget("gameconf.ini")
        if os.path.isfile(cls.__convertpath(usergameconf)):
            logging.info("Una configuración personal existe, sera cargada.")
            configurationfiles = [configurationfiles, usergameconf]

        if configurationfiles:
            logging.info("Cargando configuración del juego...")
            cls.confilepath = cls.__parsed.read(
                cls.__convertpath(configurationfiles))
            if cls.confilepath:
                cls._checkconf()
                logging.info("Configuración del juego "
                             "cargada de forma exitosa!")

                if cls.__os == "posix":
                    if cls.__parsed.has_option("DATA_PATH", "root_path"):
                        cls.__ROOTFOLDER = cls.__parsed.get("DATA_PATH",
                                                              "root_path")
                    else:
                        cls.__ROOTFOLDER = "/usr/share/games/{game}"

                elif cls.__os == "nt":
                    if cls.__parsed.has_option("DATA_PATH", "root_path"):
                        cls.__ROOTFOLDER = cls.__parsed.get("DATA_PATH",
                                                              "root_path")
                    else:
                        cls.__ROOTFOLDER = cls.joinpaths(
                            os.environ["PROGRAMFILES"], "{game}")

                cls.__ROOTFOLDER = cls.__ROOTFOLDER.format(
                    game=cls.__gamefolder)
            else:
                if cls.confilepath:
                    logging.info("Recargando la configuracion...")
                    cls.loadconf(cls.confilepath)
                    logging.info("Recarga completada!")
                else:
                    raise TAConfFailException, ("La configuración no pudo ser"
                                                " cargada de manera exitosa")

    @classmethod
    def saveconf(cls):
        """ Salva la configuración actual en un archivo ini.

        La configuración se guarda en la carpeta del juego, dentro de la
        carpeta personal del usuario."""
        with open(cls.joinpaths(cls.getuserfolder(),
                "gameconf.ini"), "w") as conf:
            cls.__parsed.write(conf)

    @classmethod
    def fromuserfolderget(cls, file):
        """ Retorna una dirección absoluta del directorio en la carpeta personal
        """
        return cls.joinpaths(cls.getuserfolder(), file)

    @classmethod
    def fromrootfolderget(cls, file):
        """ Retorna una dirección absoluta desde el directorio del juego.
        """
        return cls.joinpaths(cls.getrootfolder(), file)

    @classmethod
    def getuserfolder(cls):
        """ Retorna el directorio personal del usuario.
        """
        return cls.__convertpath(cls.__USERFOLDER)

    @classmethod
    def getrootfolder(cls):
        """ Retorna el directorio donde se almacena el juego.
        """
        return cls.__convertpath(cls.__ROOTFOLDER)

    @classmethod
    def joinpaths(cls, *args):
        """ Retorna una dirección de archivo juntando todos los argumentos.
        """
        logging.debug("Se han de unir las siguientes carpetas {0}".format(args))
        path = "/".join(args)
        path = path.replace("//", "/")

        return cls.__convertpath(path)

    @classmethod
    def __convertpath(cls, whichone):
        """ Convierte y retorna direcciones de archivos de forma adecuada.

        Para cualquier dirección de archivos se usara las barras inclinadas,
        incluso para archivos dentro de Windows. Éste método se encargara
        de retornar la dirección correcta del archivo, según el sistema
        operativo en uso.
        En caso de que whichone sea una lista, se iterara la lista y se
        devolverá el mismo tipo con las direcciones corregidas."""

        if isinstance(whichone, str):
            guess = chardet.detect(whichone)
            noconvertedstring = whichone
            whichone = whichone.decode(guess["encoding"])
            logging.debug("Cadena {0} tiene codificación '{1}'".format(
                noconvertedstring, guess["encoding"]))

            if cls.__os == "nt":
                logging.debug("Convirtiendo '/' a '\\' "
                              "para compatibilidad con Windows")
                whichone = whichone.replace("/", "\\")
            else:
                logging.debug("No hay nada que convertir, "
                              "no estamos en Windows")
            return whichone

        elif isinstance(whichone, unicode):
            # Si la cadena de caracteres ya estaba como unicode
            # es estúpido convertirla a unicode nuevamente.
            if cls.__os == "nt":
                logging.debug("Convirtiendo '/' a '\\' "
                              "para compatibilidad con Windows")
                whichone = whichone.replace("/", "\\")
            else:
                logging.debug("No hay nada que convertir, "
                              "no estamos en Windows")
            return whichone

        elif isinstance(whichone, list):
            logging.debug("Hemos recibido una lista")
            pathlist = []
            logging.debug("Iterando la lista...")
            for thisone in whichone:
                logging.debug("Convirtiendo la cadena: %s..." % thisone)
                thisone = cls.__convertpath(thisone)
                logging.debug("Convertido: %s" % thisone)
                pathlist.append(thisone)
            return pathlist
        else:
            raise ValueError, "argument is not a str or list object"

    @classmethod
    def _checkconf(cls):
        """ Revisa que los datos básicos existan.

        Deben existir algunos datos básicos sobre la configuración
        los cuales los juegos necesitan para funcionar de forma apropiada.
        En caso de faltar algún valor, el juego DEBERÍA cerrarse y notificar
        al usuario."""

        # Variables que contienen la ubicación de los archivos audiovisuales
        if cls.__parsed.has_section("DATA_PATH"):
            for opcion in ["root_path", "common_data"]:
                if not cls.__parsed.has_option("DATA_PATH", opcion):
                    raise TAConfOptionException, ("{0} no existe en "
                                                  "DATA_PATH".format(opcion))
        else:
            raise TAConfSectionException, ("La sección DATA_PATH no existe"
                                           " en la configuración")

        # Variables que contienen la distribución básica de los botones del
        # control del jugador.
        if cls.__parsed.has_section("CONTROLLER"):
            for opcion in ["action_button", "cancel_button", "pause_button",
                           "up_button", "down_button", "left_button",
                           "right_button", "keyboard_or_joystick"]:
                if not cls.__parsed.has_option("CONTROLLER", opcion):
                    raise TAConfOptionException, ("{0} no existe en "
                                                  "CONTROLLER".format(opcion))
        else:
            raise TAConfSectionException, ("La sección CONTROLLER no existe"
                                           " en la configuración")

        # Variables que contienen los valores de configuración de visualización
        # del juego.
        if cls.__parsed.has_section("DISPLAY"):
            for opcion in ["screen_size", "window_title"]:
                if not cls.__parsed.has_option("DISPLAY", opcion):
                    raise TAConfOptionException, ("{0} no existe en "
                                                  "DISPLAY".format(opcion))
        else:
            raise TAConfSectionException, ("La sección DISPLAY no existe"
                                           " en la configuración")

    @classmethod
    def getosname(cls):
        """ Retorna el nombre del sistema operativo.

        nt: para cualquier sistema operativo Windows.
        posix: para cualquier sistema operativo
        derivado de Unix (GNU/Linux, *BSD)"""
        return cls.__os

    @classmethod
    def getscreensize(cls):
        """ Retorna una tupla con las dimensiones de la pantalla del juego.
        """
        sizestring = cls.__parsed.get("DISPLAY", "screen_size")
        # partimos la cadena, convertimos a entero y ponemos todo en una tupla
        # es de esperar que las dimensiones de la pantalla se expresen como
        # 320x240 por ejemplo.
        sizex, sizey = int(sizestring.split("x")[0]), int(sizestring.split("x")[1])
        return sizex, sizey

    @classmethod
    def setscreensize(cls, (width, height)):
        """ Guarda el nuevo tamaño de la pantalla del juego.

        Este dato no sera guardado en un archivo de configuración hasta llamar
        al método saveconf().
        """
        sizestring = "{w}x{h}".format(w=width, h=height)
        cls.__parsed.set("DISPLAY", "screen_size", sizestring)

    @classmethod
    def getscreentitle(cls):
        """ Retorna el texto a mostrar en la barra de titulo del juego.
        """
        return cls.__parsed.get("DISPLAY", "window_title").decode("utf-8")

    @classmethod
    def setscreentitle(cls, title):
        """ Guarda el nuevo texto de la barra de titulo del juego
        """
        cls.__parsed.set("DISPLAY", "window_title", title)

    @classmethod
    def getcontrollerbutton(cls, button):
        """ Retorna el código SFML de la tecla perteneciente al botón especifico

        el argumento button puede ser cualquier cosa, aunque usualmente puede
        pedirse las teclas asignadas para action_button, cancel_button,
        pause_button, etc.
        """
        return cls.__parsed.getint("CONTROLLER", str(button))

    @classmethod
    def setcontrollerbutton(cls, button, code):
        """ Guarda un botón con su respectivo código numérico.

        Este dato no sera guardado en un archivo de configuración hasta llamar
        al método saveconf().
        """
        cls.__parsed.set("CONTROLLER", str(button), str(code))

    @classmethod
    def usingkeyboard(cls):
        """ Retorna verdadero si se esta usando el teclado.
        """
        if cls.__parsed.getboolean("CONTROLLER", "keyboard_or_joystick"):
            return True
        else:
            return False

    @classmethod
    def usingjoystick(cls):
        """ Retorna verdadero si se esta usando un joystick
        """
        if cls.__parsed.getboolean("CONTROLLER", "keyboard_or_joystick"):
            return False
        else:
            return True

    @classmethod
    def alternatecontrollertype(cls):
        """ Alterna entre el tipo de controlador a usar por el usuario.

        los tipos son:
          · Keyboard & Mouse
          · Joystick"""

        actualvalue = cls.__parsed.getboolean("CONTROLLER",
                                               "keyboard_or_joystick")
        cls.__parsed.set("CONTROLLER", "keyboard_or_joystick",
                          str(int(not actualvalue)))

if __name__ != "__main__":
    ### NO MODIFICAR ###
    ROOTCONFPATH = "/".join([os.path.dirname(__file__), "gameconf.ini"])
    ### FIN DE LA "PROHIBICIÓN" ###
    Conf.loadconf("thomas-aquinas", ROOTCONFPATH)
