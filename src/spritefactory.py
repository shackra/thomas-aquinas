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
import sfml
from math import sqrt
import cjson as json


class AbstractSprite(sfml.Sprite):
    """ Clase extendida para crear sprites.
    
    Esta clase debe contener un numero razonable de características
    que hagan más fácil ciertas tareas de programación con respecto
    a los sprites. El numero de características puede decrecer o
    incrementar, de cualquier forma, es preferible revisar los cambios
    en la tarea reportada acá:
    https://bitbucket.org/shackra/thomas-aquinas/issue/9
    
    Cada sprite debe poseer un archivo de configuración que defina
    sus propiedades. Las dos más importantes, hasta el momento, son
    'animation' y 'rectangles'. Ambas son diccionarios.
    
    Animation DEBE poseer una animación para cada estado finito, enumarado
    desde el 0 hasta donde el programador lo necesite. Cada uno de estos
    estados finitos deben a su vez tener enumerado del 0 hasta donde
    necesiten cada uno de los rectángulos que indican que parte de la textura
    mostrar en el sprite.
    
    Rectangles posee dentro de sí una serie de diccionarios. El "key" de cada
    diccionario indica el nombre del rectángulo y su valor es las coordenadas y
    dimensiones de susodicho rectángulo. La palabra clave rectangle DEBE ser
    incluida en la definición de las propiedades del sprite
    incluso si no existen rectángulos que definir.
    
    FIXME: En la comprobasion de coliciones/contacto puede que el uso de bucles
    ```for``` no sea para nada conveniente por el overhead que puede producir.
    ¿Debemos usar un sistema de señales y slots alà Qt? ¿Que tal
    itertools de python?
        """
    def __init__(self, texture, near, window, spritedatafile):
        Sprite.__init__(texture)
        self.clock = sfml.Clock()
        self.__machinestate = None
        self.__actualanimmachinestate = None
        self.__actualframe = 0
        self.__property = {}
        self.__window = window
        self.__spritedata = self.__loadspritedata(spritedatafile)
        self.__spritedatafile.close()
        self.__detectnearat = near
        
    def __loadspritedata(self, filepath):
        """ Carga los datos del sprite desde un archivo con formato JSON.
        
        Este metodo devuelve un diccionario con todos los objetos python
        correspondientes.
        """
        with open(common.settings.fromrootfolderget(filepath)) as fileopen:
            tmpdict = json.decode(fileopen.read())
            finaldict = {"animation": {}}
            for key in tmpdict["animation"].keys():
                finaldict["animation"][int(key)] = {}
                
                for frame in tmpdict["animation"][key].keys():
                    jsonframe = tmpdict["animation"][key][frame]
                    tupleframe = tuple(jsonframe[0]), tuple(jsonframe[1]) 
                    finaldict["animation"][int(key)][int(frame)] = tupleframe
                    
            return finaldict
                
    def __animate(self):
        """ Anima al sprite.
        
        self.__spritedata debe de poseer un subdiccionario
        llamado 'animation' con los rectangulos que representan
        cada fotograma de animacion. Los rectangulos indican
        que fragmento del spritesheet mostrar.
        
        Este metodo queda subornidado al atributo de la maquina de
        estados del sprite, para cambiar la animacion, se debe cambiar
        el estado del sprite. Excelente idea ¿no lo cree?
        
        Para simplicar, cada estado del sprite tendra una animacion
        asociada.
        """
        if self.clock.restart().milliseconds <= 60.0:
            # FIXME: la cantidad de cuadros por seguno
            # debe ser especificada en la configuracion del
            # juego. Para efectos de animacion, deberia de contarse
            # con un offset que agregue o quite milisegundo de temporizado
            # para hacer lucir la animación más lenta o más veloz.
            
            # TODO: soportar tipos de ciclos de animacion, como linear
            # ciclico, ping pong.
            # Linear: al finalizar, la animacion se queda en el ultimo cuadro.
            # Ciclico: La animacion al finalizar vuelve a comenzar
            #          desde el primer cuadro.
            # Ping pong: La animacion va de un lado al otro de los extremos
            #            de la animacion pasando por todos
            #            los cuadros intermedios.
            
            # el estado del sprite a cambiado?
            if self.__actualmachinestate != self.__machinestate:
                self.__actualmachinestate = self.__machinestate
                self.__actualframe = 0
                
            self.settexture(None,
                            self.__spritedata["animation"][\
                    self.__actualmachinestate][self.__actualframe])
            
            self.__actualframe += 1
            
            if not self.__spritedata["animation"][\
                self.__actualmachinestate].has_key(self.__actualframe):
                # Ese frame no existe!
                self.__actualframe = 0
                
    def settexture(self, texture, texture_rectangle):
        """ Asigna que textura usar para el sprite.
        """
        if texture:
            self.texture = texture
        if texture_rectangle:
            self.texture_rectangle = texture_rectangle
            
    def on_update(self):
        "Actualiza la lógica del sprite, por ejemplo, su IA"
        raise NotImplemented("Implemente el método on_update.")
    
    def on_draw(self):
        "Dibuja al sprite"
        self.__animate() # Es correcto colocar la llamada al metodo acá?
        self.__window.draw(self)
        
    def addrectangle(self, name, size, position):
        """ Agrega un rectangulo en determinada posicion.
        
        La posicion es relativa a las dimensiones del sprite.
        util para definir pequeñas areas del sprite que el desarrollador
        quizas desee saber si chocan o interactuan con elementos del juego.
        Si un rectangulo ya existia, se modificara sus parametros de area y
        posicion. para evitar modificar uno de los dos, se puede usar argumentos
        del tipo None.
        """
        if self.__spritedata["rectangles"].has_key(name):
            # Si este rectangulo ya existe, cambiamos sus atributos.
            if position:
                self.__spritedata["rectangles"][str(name)].position = position
            if size:
                self.__spritedata["rectangles"][str(name)].size = size
            else:
                # de lo contrario, lo creamos.
                if position:
                    self.__spritedata["rectangles"][str(name)] = sfml.Rectangle(
                        position, size)
                else:
                    # sin posicion? entonces colocamos el rectangulo en donde
                    # se encuentre el sprite
                    self.__spritedata["rectangles"][str(name)] = sfml.Rectangle(
                        self.position, size)
                
                
    def delrectangle(self, name):
        """ Remueve un rectanguo del sprite.
        """
        if self.__spritedata["rectangles"].has_key(str(name)):
            del(self.__spritedata["rectangles"][str(name)])
            
    def _moverectangles(self, offset):
        """ Mueve todos los rectangulos del sprite.
        
        Este metodo deberia de usarse unicamente si
        el sprite a cambiado su posicion.
        """
        # FIXME: posible area de overhead
        for rect in self.__spritedata["rectangles"]:
            self.__spritedata["rectangles"][rect].position += (offset, offset)
            
    def __distance(self, sprite):
        """ Calcula la distancia entre dos pares de puntos.
        """
        return float(sqrt((sprite.position.x - self.position.x) ** 2 - \
                        (sprite.position.y - self.position.y) ** 2))
    
    def isnear(self, sprite):
        """ Retorna la distancia entre un sprite y otro.
        """
        distance = self.__distance()
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
    
