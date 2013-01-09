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
    def __init__(self, window, jsonfile):
        Sprite.__init__(self)
        self.__machinestate = None
        self.__property = {}
        self.__window = window
        self.__spritedatafile = open(common.settings.joinpaths(
                common.settings.fromrootget("sprites"), jsonfile))
        self.__spritedata = load(self__spritedatafile)
        self.__spritedatafile.close()
        self.__near = sfml.Rectangle((0,0), (1, 1))
        self.area = sfml.Rectangle()
        
    def isnear(self, sprite):
        """ Retorna la distancia entre un sprite y otro.
        """
        if self.__near.contains(sprite.area):
            return sqrt((sprite.position.x - self.position.x) ** 2 - \
                            (sprite.position.y - self.position.y) ** 2)
        else:
            return False
        
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
    
    
