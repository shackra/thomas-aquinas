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
import scenefactory
from src.thirdparty.pytweener import pytweener

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
        self.tweener = pytweener.Tweener()
        self.defaulteasing = pytweener.Easing.Quad.easeOut
        self.window.framerate_limit = 60
        if icon: 
            self.window.icon = media.loadmedia(icon).pixels
            
        self.__actualscene = None
        self.__fullscreenmode = False
        self.__exitgame = False
        # revisar si hay Joysticks conectados al PC.
        self.__globalvariables = {}
        self.__camera = customView()
        # Reiniciamos la cámara al tamaño de la pantalla.
        self.__camera.reset(sfml.Rectangle((0, 0), 
                                           common.settings.getscreensize()))
        
        # Iniciamos algunas variables globales
        self.setglobalvariable("game title",
                               common.settings.getscreentitle())
        
    def __getitem__(self, item):
        return self.__globalvariables[str(item)]
    
    def __iter__(self):
        return self.__globalvariables.items()
    
    def movecamera(self, playerx, playery, withplayer=True):
        """ Mueve la cámara del juego.
        
        Esta es la forma más sencilla de realizar la técnica del
        'screen scrolling'. Nos hemos basado en los cálculos realizados
        por CodingMadeEasy y en el uso de objetos sfml.View.
        
        Para mover la cámara de acuerdo al movimiento del jugador
        Siendo que 'withplayer' sea True, este método debe ser llamado
        en algún momento dentro de una instancia de la clase AbstractScene
        con las coordenadas del sprite origen.
        """
        screensizex, screensizey = common.settings.getscreensize()
        if withplayer:
            camerax = -(screensizex / 2) + playerx
            cameray = -(screensizey / 2) + playery
            
            if camerax < 0: camerax = 0
            if cameray < 0: cameray = 0
            self.__camera.viewport = sfml.Rectangle((camerax, cameray),
                                                    (camerax + screensizex,
                                                     cameray + screensizey))
        else:
            # Creamos un par de tweeners para la camara.
            self.tweener.addTween(self.__camera, setcenterx=playerx,
                                  tweenTime=10, tweenType=self.defaulteasing)
            self.tweener.addTween(self.__camera, setcentery=playery,
                                  tweenTime=10, tweenType=self.defaulteasing)
            
    def loop(self):
        "¡El juego se pone en marcha!"
        
        clock = sfml.Clock()
        
        while not self.__exitgame:
            # actualizamos el tweener
            self.tweener.update(60 / 1000.0)
            
            # propagación de eventos
            for event in self.window.events:
                if type(event) is sfml.CloseEvent:
                    self.__exitgame = True
                    logging.info("Cerrando el programa...")
                    logging.info("Salvando la configuración...")
                    common.settings.saveconf()
                    logging.info("Configuración del juego salvada!")
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
                except AttributeError as e:
                    raise TAAttrIsNotScene, ("Sucedió un error en "
                                             "alguna parte del bucle:"
                                             " {0}".format(e))
                ## TODO:
                # Le pasamos el evento al dialogo para que haga algo
                #self.__widgetmanager.on_event(event)
                
            # actualizamos la escena
            try:
                self.__actualscene.on_update()
            except AttributeError as e:
                raise TAAttrIsNotScene, ("Sucedió un error en "
                                         "alguna parte del bucle:"
                                         " {0}".format(e))
            
            # dibujamos la escena
            self.window.clear(sfml.Color.BLACK)
            try:
                self.__actualscene.on_draw(self.window)
            except AttributeError:
                raise TAAttrIsNotScene, ("Sucedió un error en "
                                         "alguna parte del bucle:"
                                         " {0}".format(e))
            
            # Cambiamos el view de nuestra ventana por el que esta por defecto
            # Para dibujar los elementos de la UI. Puede que algunos elementos
            # de la UI necesiten ser dibujados dentro de
            # nuestro sfml.View regular
            self.window.view = self.window.default_view
            # TODO: crear un sistema de widgets personalisable
            #   con CSS.
            # TODO: Dibujamos los widgets
            # self.__widgetmanager.on_draw(self.window)
            self.window.display()
            # Restablecemos el view de nuestra ventana al sfml.View regular
            self.window.view = self.__camera
            # La aplicación ya es dormida en cada llamada a 
            # window.display(), de ahí que no necesitemos más
            # llamadas a sfml.sleep()
            
        ## GAME OVER!
        self.window.close()
        
    def changescene(self, scene):
        "Cambia la escena actual."
        
        if isinstance(scene, scenefactory.AbstractScene):
            logging.info("Cambiando de escena: {0}".format(scene))
            self.__actualscene = scene
        else:
            raise TAAttrIsNotScene, ("El objeto {0} no es instancia "
                                     "de scenefactory."
                                     "AbstractScene".format(type(scene)))
        
    def alternatefullscreenmode(self):
        "Alterna entre modo pantalla completa y modo ventana"
        
        # FIXME: existe un error al cambiar a modo pantalla
        # completa con una resolución de pantalla pequeña.
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
            
    def getcameraposition(self):
        """Retorna la posicion de la camara.
        """
        return self.__camera.getcenterxy()
            
class customView(sfml.View):
    """"Clase personalizada para el manejo de una cámara. La inexistencia
    de setters/getters en esta clase la hace difícil de usar en conjunto
    con pytweener, de ahí la necesidad de escribir esta clase.
    """
    
    def __init__(self):
        sfml.View.__init__(self)
        
    def setcenterx(self, x):
        """Establece el valor del centro de la cámara en el eje X.
        """
        self.center = sfml.Vector2(x, self.center.y)
        
    def setcentery(self, y):
        """Establece el valor del centro de la cámara en el eje Y.
        """
        self.center = sfml.Vector2(self.center.x, y)
        
    def getcenterx(self):
        """Retorna el valor del centro de la cámara en el eje X.
        """
        return self.center.x
    
    def getcentery(self):
        """Retorna el valor del centro de la cámara en el eje X.
        """
        return self.center.y
    
    def getcenterxy(self):
        """Retorna las coordenadas X y Y del centro de la camara.
        """
        return self.center
    
