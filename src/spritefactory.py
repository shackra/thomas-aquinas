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
import media
import json
import sfml
from math import sqrt

class AbstractSprite(sfml.Sprite):
    """ Clase extendida para crear sprites.
    
    Esta clase debe contener un numero razonable de características
    que hagan más fácil ciertas tareas de programación con respecto
    a los sprites. El numero de características puede decrecer o
    incrementar, de cualquier forma, es preferible revisar los cambios
    en la tarea reportada acá:
        https://bitbucket.org/shackra/thomas-aquinas/issue/9
        """
    def __init__(self, id, near, window, jsonfile):
        Sprite.__init__(self)
        self.__machinestate = None
        self.__property = {}
        self.__window = window
        self.__spritedatafile = open(common.settings.joinpaths(
                common.settings.fromrootget("sprites"), jsonfile))
        self.__spritedata = load(self__spritedatafile)
        self.__spritedatafile.close()
        self.__detectnearat = near
        self.areas = [customRectangle("all", ((0, 0), (1,1)))]
        
    def isnear(self, sprite):
        """ Retorna la distancia entre un sprite y otro.
        """
        distance = sqrt((sprite.position.x - self.position.x) ** 2 - \
                            (sprite.position.y - self.position.y) ** 2)
        if distance <= self.__detectnearat:
            return distance
        else:
            return False
        
    def setnear(self, distance):
        """ Asigna la distancia maxima de busqueda.
        """
        self.__detectnearat = float(distance)
        
    def getnear(self):
        """ Retorna la distancia maxima de busqueda.
        """
        return self.__detectnearat
        
    def setproperty(self, name, value):
        """ Asigna una propiedad al sprite.
        """
        self.__property[str(name)] = value
        
    def getproperty(self, name):
        """ Retorna el valor de una propiedad asignado al sprite
        """
        return self.__property[str(name)]
    
    def on_update(self):
        "Actualiza la lógica del sprite, por ejemplo, su IA"
        raise NotImplemented("Implemente el método on_update.")
    
    def on_draw(self):
        "Dibuja al sprite"
        self.__window.draw(self)
        
    def setstate(self, state):
        """cambia el estado del sprite.
        
        Con estado, nos referimos a una maquina de estados finito.
        esta técnica es muy útil para definir ciertos comportamientos
        para nuestro Sprite
        """
        if isinstance(state, int):
            self.__machinestate = state
        else:
            raise TypeError, "se esperaba un tipo int, recibido %s" % \
                type(state) 
        
    def getstate(self):
        """retorna el estado del sprite.
        
        Con estado, nos referimos a una maquina de estados finito.
        esta técnica es muy útil para definir ciertos comportamientos
        para nuestro Sprite
        """
        return self.__machinestate
    
    
class customRectangle(sfml.Rectangle):
    """ Clase heredada para detectar colisiones e intersecciones.

    Agregamos unicamente un identificador para la instancia de cualquier
    rectangulo. Así sera más facil hacer uso de listas de rectangulos y
    poder identificarlos de forma individual.
    """
    def __init__(self, name, area):
        sfml.Rectangle.__init__(area)
        self.__id = str(name)
        
    def getid(self):
        """ Retorna el nombre del rectangulo.
        """
        return self.__id
    
    def setid(self, name):
        """Asigna un nuevo nombre al rectangulo.
        """
        self.__id = str(name)
        
