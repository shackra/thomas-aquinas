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
from sfml import Sprite

class AbstractSprite(Sprite):
    """ Clase extendida para crear sprites.
    
    Esta clase debe contener un numero razonable de características
    que hagan más fácil ciertas tareas de programación con respecto
    a los sprites. El numero de características puede decrecer o
    incrementar, de cualquier forma, es preferible revisar los cambios
    en la tarea reportada acá:
        https://bitbucket.org/shackra/thomas-aquinas/issue/9
    """
    def __init__(self, xmlspritefile):
        Sprite.__init__(self)
        self.__machinestate = None
        
        
    def on_update(self):
        "Actualiza la lógica del sprite, por ejemplo, su IA"
        raise NotImplemented("Implemente el método on_update.")
    
    def on_draw(self):
        "Dibuja al sprite"
        pass
    
    def changestate(self):
        """cambia el estado del sprite.
        
        Con estado, nos referimos a una maquina de estados finito.
        esta técnica es muy útil para definir ciertos comportamientos
        para nuestro Sprite
        """
        pass
    
    
