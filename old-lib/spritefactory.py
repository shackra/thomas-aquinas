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
import lib.common
from lib import media
import sfml
from math import sqrt
import cjson as json
import itertools

class Entity:
    """ Clase compuesta para crear sprites.

    Esta clase sigue la regla de composición sobre herencia,
    pero basado en la idea de entidades - controles - propiedades.

    Una entidad puede tener un numero 'ilimitado' de propiedades.
    Para añadir una propiedad a su instancia de AbstractSprite
    solamente use la función `setattr`. Para saber si una propiedad
    existe o no en determinada entidad, use `hasattr`, Si desea borrar
    Una propiedad de la entidad, use del(entidad.propiedad).
    así de fácil. De ahí que `AbstractSprite` carezca de interfaces
    para agregar o eliminar propiedades. Python ya las provee.

    Cada sprite debe poseer un archivo de configuración que defina
    sus propiedades. Las dos más importantes, hasta el momento, son
    'animation' y 'rectangles'. Ambas son diccionarios.

    Animation DEBE poseer una animación para cada estado finito, enumerado
    desde el 0 hasta donde el programador lo necesite. Cada uno de estos
    estados finitos deben a su vez tener enumerado del 0 hasta donde
    necesiten cada uno de los rectángulos que indican que parte de la textura
    mostrar en el sprite.

    Rectangles posee dentro de sí una serie de diccionarios. El "key" de cada
    diccionario indica el nombre del rectángulo y su valor es las coordenadas y
    dimensiones de susodicho rectángulo. La palabra clave rectangle DEBE ser
    incluida en la definición de las propiedades del sprite
    incluso si no existen rectángulos que definir.

    FIXME: En la comprobación de colisiones/contacto puede que el uso de bucles
    ```for``` no sea para nada conveniente por el overhead que puede producir.
    ¿Debemos usar un sistema de señales y slots alà Qt? ¿Que tal
    itertools de python?
    """
    def __init__(self, id, texture, window, spritedatafile, rectangle):
        if rectangle and not isinstance(rectangle, sfml.Rectangle):
            rectangle = self.__tupletorect(rectangle)
            self.sprite = sfml.Sprite(texture, rectangle)
        elif rectangle and isinstance(rectangle, sfml.Rectangle):
            self.sprite = sfml.Sprite(texture, rectangle)
        else:
            self.sprite = sfml.Sprite(texture)

        self.id = id
        self._sndfx = {}
        self.__listener = False
        self.__window = window
        self.clock = sfml.Clock()
        if spritedatafile:
            self.__deltatime = 0
            self.__machinestate = None
            self.__actualmachinestate = None
            self.__actualframe = 0
            self.__spritedata = self.__loadspritedata(spritedatafile)
        else:
            self.__spritedata = None
        # mantiene una instancia de itertools.cycle
        self.__actualoop = None
        self.zindex = None
        self.__controllers = {}

    def listsoundfx(self):
        """ Devuelve una lista iterable con los nombres de los efectos de sonido
        """
        return self._sndfx.iterkeys()

    def addsoundfx(self, soundfxname, soundfxobject):
        """ Asigna un efecto de sonido para la entidad.
        """
        self._sndfx[soundfxname] = soundfxobject
        entityposx, entityposy = self.sprite.position
        self._sndfx[soundname].position = sfml.Vector3(entityposx,
                                                        entityposy,
                                                        0.0)
        self._sndfx[soundname].relative_to_listener = not self.__listener

    def removesoundfx(self, soundname):
        """ Elimina un efecto de sonido de la entidad.
        """
        try:
            del(self._sndfx[soundname])
        except KeyError:
            logging.error("El sonido {0} no existe en la entidad {1}".format(
                soundname, self.id))

    def setaslistener(self, yesorno):
        """ La entidad sera el punto de escucha del jugador.
        """
        self.__listener = yesorno
        for sound in self._sndfx.itervalues():
            sound.relative_to_listener = not self.__listener

    def islistener(self):
        """ Es la entidad el punto de escucha?
        """
        return self.__listener

    def _updatesoundfxpos(self):
        """ Actualiza la posición espacial de los efectos de sonido.
        """
        entityposx, entityposy = self.sprite.position
        for sound in self._sndfx.iteritems():
            sound.position = sfml.Vector3(entityposx, entityposy, 0.0)

    def addcontroller(self, func):
        """ Agrega un controlador para la entidad.
        """
        self.__controllers[func.func_name] = func

    def delcontroller(self, funcname):
        """ Borra un controlador para la entidad.
        """
        try:
            del(self.__controllers[funcname])
        except KeyError:
            raise KeyError, ("Controlador '{0}' no existe "
                             "para entidad {1}".format(funcname, self.id))

    def setzindex(self, neworder):
        """Cambia el nivel z del sprite.
        """
        self.zindex = int(neworder)

    def getzindex(self):
        """Retorna el nivel z del sprite.
        """
        return self.zindex

    def __tupletorect(self, tupla):
        """ Devuelve una sfml.Rectangle a partir de una tupla.
        """
        if isinstance(tupla, tuple) and len(tupla) >= 2:
            rect = sfml.Rectangle(sfml.Vector2(float(tupla[0][0]),
                                               float(tupla[0][1])),
                                  sfml.Vector2(float(tupla[1][0]),
                                               float(tupla[1][1])))
            return rect
        elif isinstance(tupla, tuple) and len(tupla) == 1:
            rect = sfml.Rectangle(sfml.Vector2(float(tupla[0])),
                                  sfml.Vector2(float(tupla[1])))
            return rect
        else:
            # retorna el objeto tal y como estaba
            return tupla

    def __loadspritedata(self, filepath):
        """ Carga los datos del sprite desde un archivo con formato JSON.

        Este metodo devuelve un diccionario con todos los objetos python
        correspondientes.
        """
        with open(common.Conf.fromrootfolderget(filepath)) as fileopen:
            tmpdict = json.decode(fileopen.read())
            parsedata = {"animation": []}
            for state in tmpdict["animation"]:
                newstate = []
                for frame in state:
                    vector1 = sfml.Vector2(float(frame[0]), float(frame[1]))
                    vector2 = sfml.Vector2(float(frame[2]), float(frame[3]))
                    newstate.append(sfml.Rectangle(vector1, vector2))
                parsedata["animation"].append(newstate)

            return parsedata

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
        self.__deltatime += self.clock.restart().milliseconds

        if self.__deltatime >= 60.0:
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

            # reiniciamos un atributo del sprite
            self.__deltatime = 0

            # el estado del sprite a cambiado?
            if self.__actualmachinestate != self.__machinestate:
                logging.debug("El estado finito del sprite cambió: {0}".format(
                        self.__machinestate))
                self.__actualmachinestate = self.__machinestate
                # recuperamos la lista de frames pertinente al estado actual.
                frames = self.__spritedata["animation"][self.__actualmachinestate]
                self.__actualoop = itertools.cycle(frames)

            # retornamos el siguiente frame en la animacion
            self.sprite.texture_rectangle = self.__actualoop.next()

            # TODO: itertools.cycle puede ser una gran herramienta, aun así
            # necesitamos un control más fino sobre la animacion, en especial
            # con animacion lineales, que no pueden ser ciclicas y deben
            # finalizar en el ultimo frame de la animacion.
            # También necesitamos saber donde acaba una animacion, para hacer
            # algo, por ejemplo, con los estados de transicion es requerido
            # saber donde acaba para cambiar el estado finito del sprite.
            # Con itertools.cycle esto no es sencillo del todo

    def settexture(self, texture, texture_rectangle):
        """ Asigna que textura usar para el sprite.
        """
        if texture:
            self.sprite.texture = texture
        if texture_rectangle:
            self.sprite.texture_rectangle = texture_rectangle

    def on_update(self, event):
        """Hace funcionar todos los controladores de la entidad.
        """
        for func in self.__controllers.itervalues():
            # Le damos la propia entidad a cada controlador.
            # Por que en realidad cada controlador sabe qué
            # propiedad acceder y manipular. Y a nosotros eso
            # no nos deberia importar!
            func(self, event)

    def on_draw(self):
        "Dibuja al sprite"
        if self.__spritedata:
            self.__animate() # Es correcto colocar la llamada al metodo acá?

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
            # FIXME: Actualmente esto no sirve así como esta...
            self.__spritedata["rectangles"][rect].position += (offset, offset)

    def __distance(self, sprite):
        """ Calcula la distancia entre dos pares de puntos.
        """
        return float(sqrt((sprite.position.x - self.sprite.position.x) ** 2 - \
                              (sprite.position.y - self.sprite.position.y) ** 2))

    def setstate(self, state):
        """cambia el estado del sprite.

        Con estado, nos referimos a una maquina de estados finito.
        esta técnica es muy útil para definir ciertos comportamientos
        para nuestro Sprite
        """
        if isinstance(state, int):
            if 0 <= state <= len(self.__spritedata["animation"]) - 1:
                self.__machinestate = state
            else:
                self.__machinestate = 0

            self.__animate()
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
