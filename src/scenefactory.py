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
from thirdparty.pytmx import tmxloader

class AbstractScene:
    """Escena abstracta del juego.

    Las escenas representan partes visibles del juego, ya sea una
    pantalla de introduccion, creditos, o un campo de batalla.

    Para poder hacer escenas funcionales, debe derivar de esta clase
    cualquier escena que necesite."""

    def __init__(self, scenemanager):
        self.scenemanager = scenemanager
        # Para cambiar una escena puede hacer lo siguiente:
        #     self.scenemanager.changescene(nuevaescena)
        # Y eso es todo :)

    def on_update(self):
        "El manejador de escenas llamara este metodo para actualizar la logica."
        raise NotImplemented("Implemente el metodo on_update.")

    def on_event(self, event):
        "El manejador de escenas llamara este metodo cuando aya eventos."
        raise NotImplemented("Implemente el metodo on_event.")

    def on_draw(self, window):
        "El manejador de escenas llamara este metodo para dibujar la escena."
        raise NotImplemented("Implemente el metodo on_draw.")

    def loadmap(self, mapfilepath):
        "Carga el mapa de la respectiva escena.

        No es necesario reimplementar éste metodo.
        Todos los archivos de mapa a leer deben ser en
        formato tmx, del software Tiled Map Editor
        http://www.mapeditor.org/"
        ## TODO: usar pytmx para cargar los mapas hechos en Tiled 
        # self.__mapscene = tmxloader.load_tmx
        ## TODO: Para saber más sobre scrolling de mapas enormes
        #   Buscar el proyecto lib2d de Bitcraft en pygame.org
        pass

    def movecamera(self, x, y):
        "Mueve la 'camara' del juego."
        # TODO: implementar screen scrolling aquí, ver comentarios en
        # el metodo loadmap().
        pass

    def __str__(self):
        "Util para darle un nombre a tu escena."
        raise NotImplemented("Implemente el metodo __str__")
        # por ejemplo:
        #     return "<Scene: Escena numero 1>"
        # o como usted más prefiera :)
