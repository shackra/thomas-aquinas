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
import codecs

LOGGING_FORMAT = "%(levelname)s - #%(lineno)d - %(funcName)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

class TAConfOptionException(Exception): pass
class TAConfSectionException(Exception): pass
class TAConfFailException(Exception): pass

class Conf:
    def __init__(self, gamefolder, configurationfiles):
        logging.info("Iniciando una instancia de la clase Conf")
        logging.debug("Cargando la configuración: %s..." % configurationfiles)
        self.__os = os.name
        self.__gamefolder = gamefolder
        self.confilepath = None
        self.__parsed = ConfigParser.SafeConfigParser()
        self.loadconf(configurationfiles)
        if self.confilepath:
            self._checkconf()
            logging.debug("Revisando que la configuración sea valida...")
            
        if self.getosname() != "nt":
            self.__USERFOLDER = self.joinpaths(os.environ["HOME"],
                                               ".{game}")
        else:
            self.__USERFOLDER = self.joinpaths(os.environ["APPDATA"],
                                               "{game}")
            
        self.__USERFOLDER = self.__USERFOLDER.format(
            game=self.__gamefolder)
        
        # verificando que la carpeta del juego exista en la carpeta
        # personal del usuario.
        if not os.path.isdir(self.__USERFOLDER):
            os.mkdir(self.__USERFOLDER)
            
    def loadconf(self, configurationfiles=None):
        """ Carga la configuración del juego y del usuario u otras.
        
        Si configurationfiles es una cadena o una lista de cadenas de texto
        los usara 
        """
        if configurationfiles:
            logging.info("Cargando configuración del juego...")
            self.confilepath = self.__parsed.read(
                self.__convertpath(configurationfiles))
            if self.confilepath:
                self._checkconf()
                logging.info("Configuración del juego "
                             "cargada de forma exitosa!")
                
                if self.__os == "posix":
                    if self.__parsed.has_option("DATA_PATH", "root_path"):
                        self.__ROOTFOLDER = self.__parsed.get("DATA_PATH",
                                                              "root_path")
                    else:
                        self.__ROOTFOLDER = "/usr/share/games/{game}"
                        
                elif self.__os == "nt":
                    if self.__parsed.has_option("DATA_PATH", "root_path"):
                        self.__ROOTFOLDER = self.__parsed.get("DATA_PATH",
                                                              "root_path")
                    else:
                        self.__ROOTFOLDER = self.joinpaths(
                            os.environ["PROGRAMFILES"], "{game}")
                        
                self.__ROOTFOLDER = self.__ROOTFOLDER.format(
                    game=self.__gamefolder)
            else:
                if self.confilepath:
                    logging.info("Recargando la configuracion...")
                    self.loadconf(self.confilepath)
                    logging.info("Recarga completada!")
                else:
                    raise TAConfFailException, ("La configuración no pudo ser"
                                                " cargada de manera exitosa")
                
    def saveconf(self, onuserfolder=True, filepath=None):
        """ Salva la configuración actual en un archivo ini.
        
        Si onuserfolder es verdadero, se guardara toda la configuración
        en la carpeta personal del usuario. De lo contrario se guardara
        en el archivo especificado por filepath.
        
        en caso de problemas de escritura en filepath, se escribirá
        el archivo de configuración en la carpeta del usuario."""
        
        confilepath = None
        
        if onuserfolder == True:
            # Guardamos la configuración en la carpeta personal
            # del usuario.
            try:
                confilepath = open(
                    self.joinpaths(self.getuserfolder(), "gameconf.ini"), "w")
            except IOError as e:
                logging.exception(e)
                raise
        else:
            # Guardamos la configuración en otra carpeta,
            # especificada por el usuario.
            if filepath and isinstance(filepath, str):
                try:
                    confilepath = open(
                    self.__convertpath(filepath), "w")
                except IOError as e:
                    logging.exception(e)
                    confilepath = open(
                        self.joinpaths(self.getuserfolder(), "gameconf.ini"),
                        "w")
            else:
                logging.error("%s no es del tipo str" % filepath)
                logging.debug("Guardando la configuración"
                              " en la carpeta personal")
                try:
                    confilepath = open(
                        self.joinpaths(self.getuserfolder(), "gameconf.ini"),
                        "w")
                except IOError as e:
                    logging.exception(e)
                    raise
                
        try:
            self.__parsed.write(confilepath)
            confilepath.close()
        except:
            logging.exception("El archivo de configuración no"
                              " pudo ser guardado en ningún "
                              "sitio, ¿Tiene el usuario espacio"
                              " en su disco duro?")
            
    def fromuserfolderget(self, file):
        """ Retorna una dirección absoluta del directorio en la carpeta personal
        """
        return self.joinpaths(self.getuserfolder(), file)
    
    def fromrootfolderget(self, file):
        """ Retorna una dirección absoluta desde el directorio del juego.
        """
        return self.joinpaths(self.getrootfolder(), file)
    
    def getuserfolder(self):
        """ Retorna el directorio personal del usuario.
        """
        return self.__convertpath(self.__USERFOLDER)
    
    def getrootfolder(self):
        """ Retorna el directorio donde se almacena el juego.
        """
        return self.__convertpath(self.__ROOTFOLDER)
    
    def joinpaths(self, *args, **kwords):
        """ Retorna una dirección de archivo juntando todos los argumentos.
        """
        logging.debug("Se han de unir las siguientes carpetas {0}".format(args))
        argspath = u""
        for arg in args:
            if arg == args[-1]:
                argspath += arg
            else:
                argspath += arg + u"/"
                
            logging.debug("Resultado hasta el"
                          " momento: {0}".format(argspath))
            # saneamos la ruta, por aquello de los dobles "/"
            argspath = argspath.replace("//", "/")
            logging.debug("Retornando el resultado "
                          "de la operación: {0}".format(argspath))
            
        return self.__convertpath(argspath)
    
    def __convertpath(self, whichone):
        """ Convierte y retorna direcciones de archivos de forma adecuada.
        
        Para cualquier dirección de archivos se usara las barras inclinadas,
        incluso para archivos dentro de Windows. Éste método se encargara
        de retornar la dirección correcta del archivo, según el sistema
        operativo en uso.
        En caso de que whichone sea una lista, se iterara la lista y se
        devolverá el mismo tipo con las direcciones corregidas."""
        
        whichoneunicode = None
        
        if isinstance(whichone, str) or isinstance(whichone, unicode):
            guess = chardet.detect(whichone)
            noconvertedstring = whichone
            whichone = whichone.decode(guess["encoding"])
            logging.debug("Cadena {0} tiene codificación '{1}'".format(
                noconvertedstring, guess["encoding"]))
            
            if self.__os == "nt":
                logging.debug("Convirtiendo '/' a '\\' "
                              "para compatibilidad con Windows")
                whichone = whichone.replace("/", "\\")
            else:
                logging.debug("No hay nada que convertir, "
                              "no estamos en Windows")
                pass
            
            return whichone
        
        elif isinstance(whichone, list):
            logging.debug("Hemos recibido una lista")
            pathlist = []
            logging.debug("Iterando la lista...")
            for thisone in whichone:
                logging.debug("Convirtiendo la cadena: %s..." % thisone)
                thisone = self.__convertpath(thisone)
                logging.debug("Convertido: %s" % thisone)
                pathlist.append(thisone)
            return pathlist
        else:
            raise ValueError, "argument is not a str or list object"
        
    def _checkconf(self):
        """ Revisa que los datos básicos existan.
        
        Deben existir algunos datos básicos sobre la configuración
        los cuales los juegos necesitan para funcionar de forma apropiada.
        En caso de faltar algún valor, el juego DEBERÍA cerrarse y notificar
        al usuario."""
        problem = None
        # Variables que contienen la ubicación de los archivos audiovisuales
        if self.__parsed.has_section("DATA_PATH"):
            for opcion in ["root_path", "common_data"]:
                if not self.__parsed.has_option("DATA_PATH", opcion):
                    raise TAConfOptionException, ("{0} no existe en "
                                                  "DATA_PATH".format(opcion))
        else:
            raise TAConfSectionException, ("La sección DATA_PATH no existe"
                                           " en la configuración")
        
        # Variables que contienen la distribución básica de los botones del
        # control del jugador.
        if self.__parsed.has_section("CONTROLLER"):
            for opcion in ["action_button", "cancel_button", "pause_button",
                           "up_button", "down_button", "left_button", 
                           "right_button", "keyboard_or_joystick"]:
                if not self.__parsed.has_option("CONTROLLER", opcion):
                    raise TAConfOptionException, ("{0} no existe en "
                                                  "CONTROLLER".format(opcion))
        else:
            raise TAConfSectionException, ("La sección CONTROLLER no existe"
                                           " en la configuración")
        
        # Variables que contienen los valores de configuración de visualización
        # del juego.
        if self.__parsed.has_section("DISPLAY"):
            for opcion in ["screen_size", "window_title"]:
                if not self.__parsed.has_option("DISPLAY", opcion):
                    raise TAConfOptionException, ("{0} no existe en "
                                                  "DISPLAY".format(opcion))
        else:
            raise TAConfSectionException, ("La sección DISPLAY no existe"
                                           " en la configuración")
        
    def getosname(self):
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
        sizex, sizey = int(sizestring.split("x")[0]), int(sizestring.split("x")[1])
        return sizex, sizey
    
    def setscreensize(self, (width, height)):
        """ Guarda el nuevo tamaño de la pantalla del juego.
        
        Este dato no sera guardado en un archivo de configuración hasta llamar
        al método saveconf().
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
        """ Retorna el código SFML de la tecla perteneciente al botón especifico
        
        el argumento button puede ser cualquier cosa, aunque usualmente puede
        pedirse las teclas asignadas para action_button, cancel_button,
        pause_button, etc.
        """
        return self.__parsed.getint("CONTROLLER", str(button))
    
    def setcontrollerbutton(self, button, code):
        """ Guarda un botón con su respectivo código numérico.
        
        Este dato no sera guardado en un archivo de configuración hasta llamar
        al método saveconf().
        """
        self.__parsed.set("CONTROLLER", str(button), str(code))
        
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
        
    def alternatecontrollertype(self):
        """ Alterna entre el tipo de controlador a usar por el usuario.
        
        los tipos son:
          · Keyboard & Mouse
          · Joystick"""
        
        self.__parsed.set("CONTROLLER", "keyboard_or_joystick", 
                          str(\
                              not self.__parsed.getboolean("CONTROLLER", 
                                                        "keyboard_or_joystick"))
        )
        
if __name__ != "__main__":
    # Esta linea a de cambiarse según el proyecto en el que se use el modulo
    settings = Conf("thomas-aquinas", None)
    ### NO MODIFICAR ###
    ROOTCONFPATH = os.path.join(os.path.dirname(__file__), "gameconf.ini")
    USERCONFPATH = settings.joinpaths(settings.getuserfolder(), "gameconf.ini")
    ### FIN DE LA "PROHIBICIÓN" ###
    # Ahora cargamos las configuraciones en la carpeta raíz del proyecto
    # como también desde la carpeta personal del usuario de el juego.
    # Si algo, comparado con la configuración original, debe modificarse
    # el orden del procesamiento de las configuraciones hará el trabajo.
    settings.loadconf([ROOTCONFPATH, USERCONFPATH])
    
    
