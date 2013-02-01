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
from itertools import product, chain
import common
import media
import sfml
import os

class TATileImageException(Exception): pass

# Extiende tu mente a esto
#  https://github.com/LaurentGomila/SFML/wiki/Source:-TileMap-Render

class AbstractScene(sfml.Drawable):
    """Escena abstracta del juego.
    
    Las escenas representan partes visibles del juego, ya sea una
    pantalla de introduccion, creditos, o un campo de batalla.
    
    Para poder hacer escenas funcionales, debe derivar de esta clase
    cualquier escena que necesite.
    
    Esta clase usa Super para inicializar a sfml.Drawable. Use super
    en sus subclases!
    """
    
    def __init__(self, scenemanager):
        sfml.Drawable.__init__(self)
        self.scenemanager = scenemanager
        self.vertexarray = sfml.VertexArray(sfml.PrimitiveType.QUADS)
        self.sprites = []
        # Para cambiar una escena puede hacer lo siguiente:
        #     self.scenemanager.changescene(nuevaescena)
        # Y eso es todo :)
        
    def on_update(self):
        "El manejador de escenas llamara este metodo para actualizar la logica."
        raise NotImplemented("Implemente el metodo on_update.")
    
    def on_event(self, event):
        "El manejador de escenas llamara este metodo cuando aya eventos."
        raise NotImplemented("Implemente el metodo on_event.")
    
    def on_draw(self):
        "El manejador de escenas llamara este metodo cuando aya que dibujar algo."
        raise NotImplemented("Implemente el metodo on_draw.")
    
    def loadmap(self, mapfilepath=None):
        """Carga el mapa de la respectiva escena.
        
        No es necesario reimplementar éste método.
        Todos los archivos de mapa a leer deben ser en
        formato tmx, del software Tiled Map Editor
        http://www.mapeditor.org/"""
        if mapfilepath:
            self.__tmxmapfile = common.settings.joinpaths(
                common.settings.getrootfolder(),
                "maps", mapfilepath)
            self.__tmxmapdata = tmxloader.load_tmx(self.__tmxmapfile)
            
            heightlist = []
            widthlist = []
            tilesets = []
            
            logging.info("Cargando las baldosas del escenario...")
            # carga todas las baldosas del set de baldosas
            # basado en el código escrito por bitcraft, del proyecto
            # pytmx. Revisar el método load_images_pygame del archivo
            # pytmx/tmxloader.py. fragmento de código bajo LGPL 3.
            self.__tmxmapdata.images = [0] * self.__tmxmapdata.maxgid
            
            for firstgid, tile in sorted((tile.firstgid, tile) for tile in \
                                      self.__tmxmapdata.tilesets):
                filename = os.path.basename(tile.source)
                tilesets.append(
                    media.loadimg("maps/tilesets/{0}".format(filename)))
                
                w, h = tilesets[-1].size
                widthlist.append(w)
                heightlist.append(h)
                tile_size = (tile.tilewidth, tile.tileheight)
                totalheight = sum(heightlist[1:], 0)
                real_gid = tile.firstgid - 1
                
                # FIXME: sfml no convierte los valores hexadecimales a valores
                # RGB de 0 a 255.
                # colorkey = None
                # if t.trans:
                #     colorkey = pygame.Color("#{0}".format(t.trans))
                tilewidth = tile.tilewidth + tile.spacing
                tileheight = tile.tileheight + tile.spacing
                
                # some tileset images may be slightly larger than the tile area
                # ie: may include a banner, copyright, ect. 
                # this compensates for that
                width = ((int((w - tile.margin * 2) + tile.spacing) / tilewidth) \
                         * tilewidth) - tile.spacing
                height = ((int((h - tile.margin * 2) + tile.spacing) / tileheight) \
                          * tileheight) - tile.spacing
                
                # using product avoids the overhead of nested loops
                p = product(xrange(tile.margin, height+tile.margin, tileheight),
                            xrange(tile.margin, width+tile.margin, tilewidth))
                
                for (y, x) in p:
                    real_gid += 1
                    # Puede que el llamado a ese metodo devuelva una tupla
                    # Sólo Dios sabe porqué...
                    gids = self.__tmxmapdata.mapGID(real_gid)
                    if gids == []: continue
                    
                    # Esta operacion puede ser algo lenta...
                    # creamos una textura (imagen en memoria de vídeo)
                    # a partir de una imagen cargada de acuerdo a ciertas
                    # coordenadas. En esté caso, "extraeremos" una baldosa
                    # del set de imágenes de baldosas del respectivo mapa.
                    
                    # se usan cuadro Vertexs, uno como cada esquina de un plano
                    # orden de coordenadas: X, Y
                    v1 = sfml.Vertex((0, 0), None, sfml.Vector2(
                            float(x), float(y + totalheight)))
                    v2 = sfml.Vertex((0, 0), None, sfml.Vector2(
                            v1.tex_coords.x + tile_size[0],
                            v1.tex_coords.y))
                    v3 = sfml.Vertex((0, 0), None, sfml.Vector2(
                            v1.tex_coords.x + tile_size[0],
                            v1.tex_coords.y + tile_size[1]))
                    v4 = sfml.Vertex((0, 0), None, sfml.Vector2(
                            v1.tex_coords.x,
                            v1.tex_coords.y + tile_size[1]))
                    quad = (v1, v2, v3, v4,)
                    logging.debug("Quad mapeado en: ({0}),"
                                  " ({1}), ({2}), ({3})".format(
                            v1.tex_coords, v2.tex_coords,
                            v3.tex_coords, v4.tex_coords))
                    # No tengo ni la menor idea sobre que hace esté bucle for
                    for gid, flag in gids:
                        logging.debug("gid: {0}, flag: {1}".format(gid, flag))
                        self.__tmxmapdata.images[gid] = quad
                        
            # Unimos todos los tiles sets en una sola imagen
            ## creamos una imagen del tamaño adecuado
                        widthlist.sort()
            logging.info("Creando imagen de {0}x{1}".format(widthlist[-1],
                                                            sum(heightlist)))
            alltilesimg = sfml.Image.create(widthlist[-1],
                                            sum(heightlist))
            previousimg = sfml.Rectangle(sfml.Vector2(0.0, 0.0),
                                         sfml.Vector2(0.0, 0.0))
            for tileset in tilesets:
                logging.debug("Bliteando imagen a una altura de {0}".format(
                        previousimg.height))
                alltilesimg.blit(tileset, (0, previousimg.height))
                previousimg.height += tileset.height
                
            # Finalmente, creamos la textura con todos los tilesets
            self.scenetileset = sfml.Texture.from_image(alltilesimg)
            
            # POSICONANDO LOS TILES #
            # creamos una referencia al metodo getTileImage
            getimage = self.__tmxmapdata.getTileImage
            # altura y anchura de la baldosa
            alto, ancho = (self.__tmxmapdata.tileheight,
                           self.__tmxmapdata.tilewidth)
            # Capas, (x) filas, (y) columnas
            # extraido de http://stackoverflow.com/a/893063
            # algoritmo para mapas isometricos:
            #
            # tile_map[][] = [[...],...]
            # for (i = 0; i < tile_map.size; i++):
            #     for (j = tile_map[i].size; j >= 0; j--):
            #         draw(
            #             tile_map[i][j],
            #             x = (j * tile_width / 2) + (i * tile_width / 2)
            #             y = (i * tile_height / 2) - (j * tile_height / 2)
            #         )
            # nos ahorramos el overhead de los bucles for anidados
            p = product(xrange(len(self.__tmxmapdata.tilelayers)),
                        xrange(self.__tmxmapdata.width),
                        xrange(self.__tmxmapdata.height - 1, -1, -1) \
                            if self.__tmxmapdata.orientation == "isometric"\
                            else xrange(self.__tmxmapdata.height))
            for layer, x, y in p:
                quad = getimage(x, y, layer)
                if quad:
                    # Tenemos dos formas de dibujar la baldosa
                    # si es ortografica, entonces se coloca de
                    # la siguiente forma: (x * ancho, y * alto)
                    # Si es isometrica, entonces de la siguiente
                    # forma: ((x * ancho / 2) + (y * ancho / 2), 
                    # (y * alto / 2) - (x * alto /2))
                    
                    # Desempacamos los Vertexs
                    v1, v2, v3, v4 = quad
                    if self.__tmxmapdata.orientation == "isometric":
                        v1.position = sfml.Vector2(
                            float((x * ancho / 2) + (y * ancho / 2)),
                            float((y * alto / 2) - (y * alto / 2)))
                        v2.position = sfml.Vector2(
                            v1.position.x + ancho, v1.position.y)
                        v3.position = sfml.Vector2(
                            v1.position.x + ancho, v1.position.y + alto)
                        v4.position = sfml.Vector2(
                            v1.position.x, v1.position.y + alto)
                    else:
                        v1.position = sfml.Vector2(
                            float(x * ancho), float(y * alto))
                        v2.position = sfml.Vector2(v1.position.x + ancho,
                                                   v1.position.y)
                        v3.position = sfml.Vector2(v1.position.x + ancho,
                                                   v1.position.y + alto)
                        v4.position = sfml.Vector2(v1.position.x,
                                                   v1.position.y + alto)
                        
                    # self.__tmxmapdata.tilelayers[layer].data[y][x] = \
                        #     (v1, v2, v3, v4,)
                    ## TODO: llamar a un metodo que refresque los vertexs
                    # a mostrar en pantalla.
                    ## Ponemos todos los vertexs dentro del array
                    for v in [v1, v2, v3, v4]:
                        self.vertexarray.append(v)
            logging.info("Carga de baldosas exitosa!")
        else:
            self.__tmxmapfile = None
            
    def draw(self, target, states):
        """ Dibuja el mapa del escenario.
        
        se usa el argumento *sprites para pasar grupos de sprites que deban
        ser dibujados en encontrar la capa sprite. Éste grupo de sprites
        deberá de tener un método on_draw que llamara al método on_draw
        de cada uno de los sprites dentro del grupo.
        """
        if self.__tmxmapfile:
            states.texture = self.scenetileset
            target.draw(self.vertexarray, states)
        else:
            target.clear(sfml.Color.WHITE)
            
        # Dibujamos los sprites que nos pasen
        for sprite in self.sprites:
            try:
                # Si es un sprite instancia de AbstractSprite
                # llamamos a su metodo on_draw antes de dibujarlo
                sprite.on_draw()
                target.draw(sprite.sprite, states)
            except AttributeError:
                # Fallback para usar con sprites derivados de sfml.Sprite
                target.draw(sprite, states)
                
    def getmappixelsize(self):
        """Retorna las dimensiones del mapa en pixeles.
        """
        width = self.__tmxmapdata.width * self.__tmxmapdata.tilewidth
        height = self.__tmxmapdata.height * self.__tmxmapdata.tileheight
        return (width, height)
    
    def getmaptilesize(self):
        """Retorna las dimensiones del mapa en baldosas.
        """
        return (self.__tmxmapdata.width, self.__tmxmapdata.height)
    
    def gettilesize(self):
        """Retorna las dimensiones en pixeles de un baldosa.
        """
        return (self.__tmxmapdata.tilewidth, self.__tmxmapdata.tileheight)
    
    def getmappixelwidth(self):
        """Retorna el ancho del mapa en pixeles.
        """
        return self.getmappixelsize()[0]
    
    def getmappixelheight(self):
        """Retorna la altura del mapa en pixeles.
        """
        return self.getmappixelsize()[1]
    
    def getmaptilewidth(self):
        """Retorna el ancho del mapa en baldosas.
        """
        return self.getmaptilesize()[0]
    
    def getmaptileheight(self):
        """Retorna la altura del mapa en baldosas.
        """
        return self.getmaptilesize()[1]
    
    def __str__(self):
        "Util para darle un nombre a tu escena."
        raise NotImplemented("Implemente el metodo __str__")
        # por ejemplo:
        #  return "<Scene: Escena #1, File: {0}>".format(self.__tmxmapfile)
        # o como usted más prefiera :)
    
    
class Tile(sfml.TransformableDrawable):
    # FIXME: no sirve.
    def __init__(self, image):
        sfml.TransformableDrawable.__init__(self)
        if isinstance(image, sfml.Texture):
            self.texture = image
        else:
            raise TATileImageException, ("Se esperaba un objeto del tipo "
                                         "sfml.Texture"
                                         " recibido {0}".format(type(image)))
        
    def draw(self, target, states):
        # states.transform = self.transform
        states.texture = self.texture
        target.draw(self.texture.copy_to_image(), states)
        
        
