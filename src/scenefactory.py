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
from src.spritefactory import Entity
from thirdparty.pytmx import tmxloader
from itertools import product, chain, izip_longest
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
        self.__vertexarraylist = []
        # Para cambiar una escena puede hacer lo siguiente:
        #     self.scenemanager.changescene(nuevaescena)
        # Y eso es todo :)

    def updatesprites(self, event):
        """ Se actualiza el estado de todos los sprites.
        
        Aqui se actualizara todaas las entidades pertenecientes a la escena.
        Cada una recibe el mismo evento sacado de windw.events para hacer
        algo con su controlador que quizas quiera algo más que las propiedades
        de la entidad.
        """
        for entity in chain.from_iterable(self.sprites):
            entity.on_update(event)

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
            self.tmxmapdata = tmxloader.load_tmx(self.__tmxmapfile)
            
            heightlist = []
            widthlist = []
            tilesets = []

            # estos vertexarray llevaran los vertices visibles unicamente,
            # por capa.
            self.__vertexarraytodraw = []
            for i in xrange(0, len(self.tmxmapdata.tilelayers)):
                self.__vertexarraytodraw.append(
                    sfml.VertexArray(sfml.PrimitiveType.QUADS))
            # Agregamos una lista de listas vacias para colocar a los sprites
            # cada lista vacia representa una capa del scenario.            
            self.sprites = []
            for i in xrange(0, len(self.tmxmapdata.tilelayers)):
                self.sprites.append([])

            logging.info("Cargando las baldosas del escenario...")
            # carga todas las baldosas del set de baldosas
            # basado en el código escrito por bitcraft, del proyecto
            # pytmx. Revisar el método load_images_pygame del archivo
            # pytmx/tmxloader.py. fragmento de código bajo LGPL 3.
            self.tmxmapdata.images = [0] * self.tmxmapdata.maxgid
            self.tmxmapdata.objectgids = [0] * self.tmxmapdata.maxgid

            objgid = [obj.gid for obj in self.tmxmapdata.getObjects()]
            for gid in objgid:
                while objgid.count(gid) > 1:
                    objgid.remove(gid)
            objgid.remove(0)
            
            for firstgid, tile in sorted((tile.firstgid, tile) for tile in \
                                      self.tmxmapdata.tilesets):
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
                    
                    gids = self.tmxmapdata.mapGID(real_gid)
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
                    
                    # este GID es usado en alguna parte del escenario?
                    if real_gid in objgid:
                        # Este GID pertenece a un objeto que sera dibujado
                        # dentro del escenario.

                        texpos = sfml.Vector2(float(x), float(y + totalheight))
                        texsize = sfml.Vector2(tile_size[0], tile_size[1])
                        objimgrect = sfml.Rectangle(texpos, texsize)
                        # sfml.Rectangle(
                        #     (x, y + totalheight),
                        #     (tile_size[0],
                        #      totalheight + tile_size[1]))
                        # almacenamos el rectangulo del objeto
                        self.tmxmapdata.objectgids[real_gid] = objimgrect
                    if gids == []: continue # Este GID no se usa para nada.

                    # Este GID se usa como baldosa para el mapa
                    # se usan cuatro Vertexs, uno como cada esquina de un plano
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
                        self.tmxmapdata.images[gid] = quad
                        
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
                        # CARGAMOS LOS OBJETOS DEL MAPA
            self.__loadsceneobjects()
            # POSICONANDO LOS TILES #
            self.__posvertexs()
            # PREPARANDO SOLAMENTE LOS TILES VISIBLES #
            self.__refreshvisibletiles(self.scenemanager.window.view)
            logging.info("Carga de baldosas exitosa!")
        else:
            self.__tmxmapfile = None
            self.sprites = [[]]

    def __loadsceneobjects(self):
        """ Carga todos los objetos del escenario comos sprites.

        No tengo ni la menor idea sobre como identificar en qué capa
        estaban estos objetos... sencillamente pytmx no nos puede decir!

        Una posible solucion es buscar por una propiedad en una capa de
        patrones y poner todos los sprites al nivel de esa capa para que se
        dibujen **despues** de la capa de patrones.

        Este metodo debe ser llamado despues de haber cargado las balsodas
        ya que necesitamos los gid de cada una de ellas para armar nuestro
        objeto.
        """
        ## Cada grupo de objetos contiene la propiedad 'drawbefore'
        ## cuyo valor es el nombre de la capa de patrones.
        # repasamos los grupos de objetos
        for objectgroup in self.tmxmapdata.objectgroups:
            layerindex = -1
            if hasattr(objectgroup, "drawbefore"):
                # Recuperamos la capa con ese nombre
                tilelayer = self.tmxmapdata.getTileLayerByName(
                    objectgroup.drawbefore)
                # miramos en qué indice esta la capa de patrones
                layerindex = self.tmxmapdata.tilelayers.index(tilelayer)
                tilewidth, tileheight = (self.tmxmapdata.tilewidth,
                                         self.tmxmapdata.tileheight)
            # repasamos el grupo de objetos
            for entity in objectgroup:
                # todas las entidades cuyo tipo sea None, son objetos del
                # juego.
                if not entity.type:
                    entityimgrect = self.tmxmapdata.objectgids[entity.gid]
                    entityobj = Entity(
                        "obj_{0}".format(
                            len(self.sprites[layerindex]) if not entity.name else entity.name),
                        self.scenetileset,
                        self.scenemanager.window,
                        None,
                        entityimgrect)
                    entityobj.sprite.position = sfml.Vector2(entity.x, entity.y)
                    entityobj.setzindex(layerindex)
                    # es solida la entidad?
                    if hasattr(entity, "solid"):
                        setattr(entityobj, "solid", entity.solid)
                    self.addsprite(entityobj)

    def __refreshvisibletiles(self, currentview):
        """ Revisa cuales baldoas son visibles para el jugador.

        Aunque este metodo sea llamado, la revision de baldosas se realizara
        unicamente si la diferencia entre el centro del view viejo y el view
        actual es mayor al ancho y alto de una baldosa (en los ejes positivos
        y negativos).
        """
        try:
            assert self.__oldviewcenter
        except AttributeError:
            # FIRST time!
            logging.debug("La propiedad '__oldviewcenter'"
                          " no existe, creandola...")
            self.__oldviewcenter = currentview.center
            self.__oldviewcenter += sfml.Vector2(1000.0, 1000.0)

        # obtenemos la diferencia entre los centros de cada view
        currentdiff = self.__oldviewcenter - currentview.center
            
        tileheight, tilewidth = (self.tmxmapdata.tileheight,
                                 self.tmxmapdata.tilewidth)
        
        if ((tilewidth <= currentdiff.x) or
            (-tilewidth >= currentdiff.x)) or ((tileheight <= currentdiff.y) or
                                               (-tileheight >= currentdiff.y)):
            logging.debug("El centro del view de Window"
                          " a cambiado, diferencia: {0}".format(currentdiff))
            # sencillamente limpiamos de vertexs cada vertexarray
            for vertexarray in self.__vertexarraytodraw:
                vertexarray.clear()
            # Sí se ha movido el centro de forma significativa!
            self.__oldviewcenter = currentview.center
            # Creamos un rectangulo que representa la zona visible del escenario
            rect = sfml.Rectangle(currentview.center - currentview.size / 2.0,
                                  currentview.size + sfml.Vector2(tilewidth,
                                                                  tileheight)
                                  )
            
            logging.debug("Recreando baldosas visibles...")
            for array, arrayindex, xarrayrange in self.__vertexarrayranges:
                for vertex in xarrayrange:
                    if (rect.contains(array[vertex].position) or
                        rect.contains(array[vertex + 1].position) or
                        rect.contains(array[vertex + 2].position) or
                        rect.contains(array[vertex + 3].position)):
                        # Esta baldosa existe!
                        self.__vertexarraytodraw[arrayindex].append(
                            array[vertex])
                        self.__vertexarraytodraw[arrayindex].append(
                            array[vertex + 1])
                        self.__vertexarraytodraw[arrayindex].append(
                            array[vertex + 2])
                        self.__vertexarraytodraw[arrayindex].append(
                            array[vertex + 3])
            
    def __posvertexs(self):
        """ Posiciona los vertices y los guarda en la lista de VertexArrays.

        Lo ideal es llamar a esta funcion una vez luego de cargado el mapa.
        Así tendremos posicionados todos los vertices dentro de sus vertexarrays
        """
        # Obtenemos el alto y ancho de las baldosas
        height, width = (self.tmxmapdata.tileheight,
                         self.tmxmapdata.tilewidth)
        tiles = product(
            xrange(len(self.tmxmapdata.tilelayers)),
            xrange(self.tmxmapdata.width),
            xrange(self.tmxmapdata.height - 1, -1, -1) \
                if self.tmxmapdata.orientation == "isometric"\
                else xrange(self.tmxmapdata.height))
        
        vertexarraylist = []
        for i in xrange(0, len(self.tmxmapdata.tilelayers)):
            vertexarraylist.append(
                sfml.VertexArray(sfml.PrimitiveType.QUADS))
        
        for layer, x, y in tiles:
            quad = self.tmxmapdata.getTileImage(x, y, layer)
            if quad:
                # Tenemos dos formas de dibujar la baldosa
                # si es ortografica, entonces se coloca de
                # la siguiente forma: (x * width, y * height)
                # Si es isometrica, entonces de la siguiente
                # forma: ((x * width / 2) + (y * width / 2), 
                # (y * height / 2) - (x * height /2))

                # Desempacamos los Vertexs
                v1, v2, v3, v4 = quad
                if self.tmxmapdata.orientation == "isometric":
                    v1.position = sfml.Vector2(
                        float((x * width / 2) + (y * width / 2)),
                        float((y * height / 2) - (y * height / 2)))
                    v2.position = sfml.Vector2(
                        v1.position.x + width, v1.position.y)
                    v3.position = sfml.Vector2(
                        v1.position.x + width, v1.position.y + height)
                    v4.position = sfml.Vector2(
                        v1.position.x, v1.position.y + height)
                else:
                    v1.position = sfml.Vector2(
                        float(x * width), float(y * height))
                    v2.position = sfml.Vector2(v1.position.x + width,
                                               v1.position.y)
                    v3.position = sfml.Vector2(v1.position.x + width,
                                               v1.position.y + height)
                    v4.position = sfml.Vector2(v1.position.x,
                                               v1.position.y + height)

                vertexarraylist[layer].append(v1)
                vertexarraylist[layer].append(v2)
                vertexarraylist[layer].append(v3)
                vertexarraylist[layer].append(v4)

        # Generamos una comprension de lista, necesitaremos
        # una de estas porque van a ser accedida muchas veces
        # durante la visualizacion del escenario.
        self.__vertexarrayranges = [(array,
                                     vertexarraylist.index(array),
                                     xrange(0, len(array), 4))
                                    for array in
                                    vertexarraylist]
        
    def addsprite(self, entity):
        """ Agrega un sprite para ser dibujado en el escenario.

        Cada sprite es acomodado en una lista que representa la capa
        según su zindex, así, si el zindex de un sprite es 2, se colocara
        en la lista 2. el zindex de un  sprite no puede ser menor de 0 y
        mayor a la cantidad de capas en el escenario, de otro modo, se
        agregaran a la ultima lista que representa la ultima capa
        del esceneario.
        """
        # verificamos el zindex de la entidad
        if not hasattr(entity, "zindex"):
            raise TypeError, "El parametro recibido no es una entidad valida."

        if entity.zindex < 0:
            entity.zindex = 0 # Corregimos numeros negativos
        if entity.zindex > len(self.sprites) - 1:
            # Si el zindex del sprite es mayor a las capas existentes
            # sencillamente se agrega arriba de la lista. En este
            # caso no corregimos su zindex.
            self.sprites[-1].append(entity)
        else:
            # En caso contrario, se agrega el sprite a la capa
            # correspondiente
            self.sprites[entity.zindex].append(entity)

    def findsprite(self, spriteid):
        """ Busca a un determinado sprite.

        este metodo retorna la lista e indice en la
        cual se ubica el sprite.

        FIXME: mejorar transversion de la lista para
        cantidades enormes de sprites y cuidar el rendimiento
        de busqueda.
        """
        for layer in self.sprites:
            for sprite in layer:
                if sprite.id == str(spriteid):
                    return (self.sprites.index(layer),
                          layer.index(sprite))

    def draw(self, target, states):
        """ Dibuja el mapa del escenario.
        
        se usa el argumento *sprites para pasar grupos de sprites que deban
        ser dibujados en encontrar la capa sprite. Éste grupo de sprites
        deberá de tener un método on_draw que llamara al método on_draw
        de cada uno de los sprites dentro del grupo.
        """
        if self.__tmxmapfile:
            self.__refreshvisibletiles(self.scenemanager.window.view)
            states.texture = self.scenetileset
            drawables = chain.from_iterable(
                izip_longest(self.__vertexarraytodraw, self.sprites))
            for drawable in drawables:
                if isinstance(drawable, list):
                    drawable.sort(key=lambda entity: entity.sprite.position.y)
                    for entity in drawable:
                        entity.on_draw()
                        target.draw(entity.sprite, states)
                elif isinstance(drawable, sfml.VertexArray):
                    target.draw(drawable, states)
        else:
            target.clear(sfml.Color.WHITE)
            self.sprites[-1].sort(key=lambda entity: entity.sprite.position.y)
            logging.debug("Dibujando {0} entidade(s)".format(
                    len(drawable)))
            for entity in self.sprites[-1]:
                entity.on_draw()
                target.draw(entity.sprite, states)
                
    def getmappixelsize(self):
        """Retorna las dimensiones del mapa en pixeles.
        """
        width = self.tmxmapdata.width * self.tmxmapdata.tilewidth
        height = self.tmxmapdata.height * self.tmxmapdata.tileheight
        return (width, height)
    
    def getmaptilesize(self):
        """Retorna las dimensiones del mapa en baldosas.
        """
        return (self.tmxmapdata.width, self.tmxmapdata.height)
    
    def gettilesize(self):
        """Retorna las dimensiones en pixeles de un baldosa.
        """
        return (self.tmxmapdata.tilewidth, self.tmxmapdata.tileheight)
    
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
