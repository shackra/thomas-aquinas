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
import common
import media
import sfml
import os

class AbstractScene:
    """Escena abstracta del juego.

    Las escenas representan partes visibles del juego, ya sea una
    pantalla de introduccion, creditos, o un campo de batalla.

    Para poder hacer escenas funcionales, debe derivar de esta clase
    cualquier escena que necesite."""

    def __init__(self):
        # self.scenemanager = scenemanager
        # Para cambiar una escena puede hacer lo siguiente:
        #     self.scenemanager.changescene(nuevaescena)
        # Y eso es todo :)
        pass

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
        """Carga el mapa de la respectiva escena.

        No es necesario reimplementar éste método.
        Todos los archivos de mapa a leer deben ser en
        formato tmx, del software Tiled Map Editor
        http://www.mapeditor.org/"""
        self.__tmxmapfile = common.settings.joinpaths(
            common.settings.getrootfolder(),
            "maps", mapfilepath)
        self.__tmxmapdata = tmxloader.load_tmx(self.__tmxmapfile)

        logging.info("Cargando las baldosas del escenario...")
        # carga todas las baldosas del set de baldosas
        # basado en el código escrito por bitcraft, del proyecto
        # pytmx. Revisar el método load_images_pygame del archivo
        # pytmx/tmxloader.py. fragmento de código bajo LGPL 3.
        self.__tmxmapdata.images = [0] * self.__tmxmapdata.maxgid

        for firstgid, tile in sorted((tile.firstgid, tile) for tile in \
                                  self.__tmxmapdata.tilesets):
            filename = os.path.basename(tile.source)
            tileset = media.loadimg("maps/tilesets/{0}".format(filename))

            w, h = tileset.size
            tile_size = (tile.tilewidth, tile.tileheight)
            real_gid = tile.firstgid - 1

            # FIXME: sfml no convierte los valores hexadecimales a valores
            # RGB de 0 a 255.
            # colorkey = None
            # if t.trans:
            #     colorkey = pygame.Color("#{0}".format(t.trans))

            # i dont agree with margins and spacing, but i'll support it anyway
            # such is life. okay.jpg
            tilewidth = tile.tilewidth + tile.spacing
            tileheight = tile.tileheight + tile.spacing
            
            # some tileset images may be slightly larger than the tile area
            # ie: may include a banner, copyright, ect. 
            # this compensates for that
            width = ((int((w-tile.margin*2) + tile.spacing) / tilewidth) \
                     * tilewidth) - tile.spacing
            height = ((int((h-tile.margin*2) + tile.spacing) / tileheight) \
                      * tileheight) - tile.spacing
            
            # using product avoids the overhead of nested loops
            p = product(xrange(tile.margin, height+tile.margin, tileheight),
                        xrange(tile.margin, width+tile.margin, tilewidth))

            for (y, x) in p:
                real_gid += 1
                gids = self.__tmxmapdata.mapGID(real_gid)
                if gids == []: continue

                # Esta operacion puede ser algo lenta...
                # creamos una textura (imagen en memoria de vídeo)
                # a partir de una imagen cargada de acuerdo a ciertas
                # coordenadas. En esté caso, "extraeremos" una baldosa
                # del set de imágenes de baldosas del respectivo mapa.
                tileimg = sfml.Texture.load_from_image(tileset, 
                                                        (x, y, 
                                                         tile_size[0], 
                                                         tile_size[1]))

                # No tengo ni la menor idea sobre que hace esté bucle for
                for gid in gids:
                    self.__tmxmapdata.images[gid] = tileimg

        logging.info("Carga de baldosas exitosa!")

    def drawmap(self, *args):
        """ Dibuja el mapa del escenario.

        se usa el argumento *args para pasar grupos de sprites que deban
        ser dibujados en encontrar la capa sprite. Éste grupo de sprites
        deberá de tener un método on_draw que llamara al método on_draw
        de cada uno de los sprites dentro del grupo.
        """
        pass

    def __str__(self):
        "Util para darle un nombre a tu escena."
        raise NotImplemented("Implemente el metodo __str__")
        # por ejemplo:
        #  return "<Scene: Escena #1, File: {0}>".format(self.__tmxmapfile)
        # o como usted más prefiera :)
