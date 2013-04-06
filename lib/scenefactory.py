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
from lib.spritefactory import Entity
from thirdparty.pytmx import tmxloader
from itertools import product, chain, izip_longest
from lib import common
import sfml


class TATileImageException(Exception): pass

# Extiende tu mente a esto
#  https://github.com/LaurentGomila/SFML/wiki/Source:-TileMap-Render

class AbstractScene(sfml.Drawable):
    """Escena abstracta del juego.

    Las escenas representan partes visibles del juego, ya sea una
    pantalla de introducción, créditos, o un campo de batalla.

    Para poder hacer escenas funcionales, debe derivar de esta clase
    cualquier escena que necesite.

    Esta clase usa Super para inicializar a sfml.Drawable. Use super
    en sus subclases!
    """

    def __init__(self, scenemanager, initialmapfile):
        sfml.Drawable.__init__(self)
        self.scenemanager = scenemanager
        if isinstance(initialmapfile, unicode) or isinstance(initialmapfile, str):
            self.tmxdata = tmxloader.load_tmx(
                       common.Conf.fromrootfolderget(initialmapfile))
            self.tmxdata.images = [0] * self.tmxdata.maxgid
            self.dontdrawtiles = False
        else:
            self.tmxdata = None
        self.sprites = []
        self.__vertexarraytodraw = []
        self.__oldviewcenter = sfml.View().center
        self.__oldviewcenter += sfml.Vector2(1000.0, 1000.0)
        # Para cambiar una escena puede hacer lo siguiente:
        #     self.scenemanager.changescene(nuevaescena)
        # Y eso es todo :)

    def drawtiles(self, status=True):
        """ Indicamos si deseamos o no dibujar las baldosas del mapa.

        Los objetos del mapa y las entidades no resultan afectados.
        """
        self.dontdrawtiles = not status

    def updatesprites(self, event):
        """ Se actualiza el estado de todos los sprites.

        Aquí se actualizara todas las entidades pertenecientes a la escena.
        Cada una recibe el mismo evento sacado de windw.events para hacer
        algo con su controlador que quizás quiera algo más que las propiedades
        de la entidad.
        """
        for entity in chain.from_iterable(self.sprites):
            entity.on_update(event)

    def on_event(self, event):
        "El manejador de escenas llamara este método cuando aya eventos."
        raise NotImplementedError("Implemente el método on_event.")

    def on_draw(self):
        "El manejador de escenas llamara este método cuando aya que dibujar algo."
        raise NotImplementedError("Implemente el método on_draw.")

    def loadanothermap(self, tmxfile, dontdrawtiles=False):
        """ Carga los datos de otro mapa.

        Algunos mapas comparten datos, como por ejemplo, las imagenes usadas
        como texturas para las baldosas.
        """
        if self.tmxdata:
            self.tmxdata.filename = common.Conf.fromrootfolderget(tmxfile)
            self.tmxdata.load()
        else:
            self.tmxdata = tmxloader.load_tmx(
                           common.Conf.fromrootfolderget(tmxfile))
        self.dontdrawtiles = dontdrawtiles

    def loadmaptiles(self):
        """ Carga los rectangulos de un mapa TMX.

        Este metodo SOLAMENTE cargara todos los rectangulos
        de cada imagen del juego. Para cargar las imagenes
        usadas en el mapa usa loadmapimages().
        """
        if not self.tmxdata:
            logging.info("Ningun mapa a sido cargado."
            " Omitiendo ejecución de {0}".format(self.loadmaptiles.func_name))
            return

        tileimgheight = 0
        self.tmxdata.images = [0] * self.tmxdata.maxgid
        logging.info("Cargando las baldosas del escenerio...")
        for firstgid, tile in sorted((tile.firstgid, tile)
                                     for tile in self.tmxdata.tilesets):
            # agregamos una lista como capa para los sprites
            self.sprites.append([])
            # agregamos un VertexArray como capa para los vertexs
            self.__vertexarraytodraw.append(sfml.VertexArray(
                    sfml.PrimitiveType.QUADS))
            realgid = tile.firstgid - 1
            logging.debug("GID del set de baldosas: {0}".format(tile.firstgid))

            tilewidth = tile.tilewidth + tile.spacing
            tileheight = tile.tileheight + tile.spacing

            # some tileset images may be slightly larger than the tile area
            # ie: may include a banner, copyright, ect.
            # this compensates for that
            width = ((int((tile.width - tile.margin * 2) + tile.spacing) /
                      tilewidth) * tilewidth) - tile.spacing
            height = ((int((tile.height - tile.margin * 2) + tile.spacing) /
                       tileheight) * tileheight) - tile.spacing

            # using product avoids the overhead of nested loops
            p = product(xrange(tile.margin, height+tile.margin, tileheight),
                        xrange(tile.margin, width+tile.margin, tilewidth))

            for (y, x) in p:
                realgid += 1
                gids = self.tmxdata.mapGID(realgid)

                if gids:
                    # Este GID pertenece a un objeto o a una baldosa que
                    # sera dibujado dentro del escenario.
                    texpos = sfml.Vector2(float(x), float(y + tileimgheight))
                    texsize = sfml.Vector2(tilewidth, tileheight)
                    quad = sfml.Rectangle(texpos, texsize)
                    # Se almacena el objeto.
                    for gid, flag in gids:
                        logging.debug("real_gid: {0}, gid:"
                                      " {1}, flag: {2}".format(realgid,
                                                               gid, flag))
                        self.tmxdata.images[gid] = quad
                        logging.debug("Rectangulo de {0} "
                                     "({2}) posicion {1}".format(gid,
                                                                 quad,
                                                                 realgid))
                elif gids is None:
                    # Este GID no se usa para nada.
                    continue

            tileimgheight += tile.height

    def loadmapimages(self):
        """ Carga a una textura las imagenes del mapa actual.

        el tamaño de la textura NO DEBE sobrepasar los 8192 pixels
        en algunas tarjetas graficas más modernas esto puede aumentar.
        En tarjetas de video viejas el limite es 512 pixeles.
        """
        if not self.tmxdata:
            logging.info("Ningun mapa a sido cargado."
            " Omitiendo ejecución de {0}".format(self.loadmapimages.func_name))
            return

        maximumsize = sfml.Texture.get_maximum_size()
        if maximumsize <= 512:
            logging.critical("La tarjeta de video es poco "
                             "potente para correr este juego,"
                             " tiene un limite de {0} pixeles".format(
                    maximumsize))
            # TODO: sacarnos del juego.

        actualimageheight = 0.0
        # FIXME: no deben tomarse en cuenta sets de baldosas
        # que no sean visibles.
        imageheight = sum(tile.height for tile in self.tmxdata.tilesets)
        imagewidth = sorted(tile.width for tile in self.tmxdata.tilesets)[-1]
        imagetmp = sfml.Image.create(imagewidth, imageheight, sfml.Color.WHITE)

        for firstgid, tile in sorted((tile.firstgid, tile)
                                     for tile in self.tmxdata.tilesets):
            tilefilepath = common.Conf.joinpaths(
                common.Conf.getrootfolder(),
                tile.source[2:]
                )
            # sfml.graphics.RenderTexture es una buena opcion.
            imagetmp.blit(sfml.Image.from_file(tilefilepath),
                          (0.0, actualimageheight))
            actualimageheight += float(tile.height)

        # Finalmente, creamos la textura con todos los tilesets
        self.scenetileset = sfml.Texture.from_image(imagetmp)

    def loadmapobjects(self):
        """ Carga todos los objetos del escenario como sprites.

        No tengo ni la menor idea sobre como identificar en qué capa
        estaban estos objetos... sencillamente pytmx no nos puede decir!

        Una posible solución es buscar por una propiedad en una capa de
        patrones y poner todos los sprites al nivel de esa capa para que se
        dibujen **después** de la capa de patrones.

        Este método debe ser llamado después de haber cargado las baldosas
        ya que necesitamos los gid de cada una de ellas para armar nuestro
        objeto.
        """
        if not self.tmxdata:
            logging.info("Ningun mapa a sido cargado."
            " Omitiendo ejecución de {0}".format(self.loadmapobjects.func_name))
            return

        ## Cada grupo de objetos contiene la propiedad 'drawbefore'
        ## cuyo valor es el nombre de la capa de patrones.
        # repasamos los grupos de objetos
        for objectgroup in self.tmxdata.objectgroups:
            layerindex = -1
            if hasattr(objectgroup, "drawbefore"):
                # Recuperamos la capa con ese nombre
                tilelayer = self.tmxdata.getTileLayerByName(
                    objectgroup.drawbefore)
                # miramos en qué indice esta la capa de patrones
                layerindex = self.tmxdata.tilelayers.index(tilelayer)
                #tilewidth, tileheight = (self.tmxdata.tilewidth,
                #                         self.tmxdata.tileheight)
            # repasamos el grupo de objetos
            for entity in objectgroup:
                # todas las entidades cuyo tipo sea None, son objetos del
                # juego.
                if not entity.type:
                    entityimgrect = self.tmxdata.images[entity.gid]
                    logging.debug("Tipo: {0}".format(type(entityimgrect)))
                    entityobj = Entity(
                        "obj_{0}".format(
                            len(self.sprites[layerindex]) if not entity.name else entity.name),
                        self.scenetileset,
                        self.scenemanager.window,
                        None,
                        entityimgrect)
                    entityobj.sprite.position = sfml.Vector2(entity.x, entity.y)
                    # el origen de los objetos en
                    # Tiled es su esquina inferior izquierda
                    originy = float(self.tmxdata.tilesets[0].tileheight)
                    entityobj.sprite.origin = sfml.Vector2(0.0, originy)
                    entityobj.setzindex(layerindex)
                    # es solida la entidad?
                    if hasattr(entity, "solid"):
                        setattr(entityobj, "solid", entity.solid)
                    self.addsprite(entityobj)

    def __refreshvisibletiles(self, currentview):
        """ Revisa cuales baldosa son visibles para el jugador.

        Aunque este método sea llamado, la revisión de baldosas se realizara
        únicamente si la diferencia entre el centro del view viejo y el view
        actual es mayor al ancho y alto de una baldosa (en los ejes positivos
        y negativos).
        """
        if not self.tmxdata:
            logging.info("Ningun mapa a sido cargado."
            " Omitiendo ejecución "
            "de {0}".format(self.____refreshvisibletiles.func_name))
            return

        # obtenemos la diferencia entre los centros de cada view
        currentdiff = self.__oldviewcenter - currentview.center

        tileheight, tilewidth = (self.tmxdata.tileheight,
                                 self.tmxdata.tilewidth)

        if (((tilewidth <= currentdiff.x) or
            (-tilewidth >= currentdiff.x)) or ((tileheight <= currentdiff.y) or
            (-tileheight >= currentdiff.y))):
                logging.debug("El centro del view de Window"
                              " a cambiado, diferencia: {0}".format(currentdiff))
                # Sí se ha movido el centro de forma significativa!
                self.__oldviewcenter = currentview.center
                # Creamos un rectángulo que representa la zona visible del escenario
                rect = sfml.Rectangle(currentview.center - currentview.size / 2.0,
                                      currentview.size + sfml.Vector2(tilewidth,
                                                                      tileheight))

                logging.debug("Recreando baldosas visibles...")
                rcoordx, rcoordy, rheight, rwidth = (rect.left, rect.top,
                                                     rect.height, rect.width)

                # normalizamos las coordenadas X y Y del rectangulo
                if rcoordx < 0:
                    rcoordx = rcoordx * -1
                elif rcoordy < 0:
                    rcoordy = rcoordy * -1

                # pasamos las coordenadas de pixeles a baldosas
                # FIXME: rwidth y rheight se pasan por dos unidades de más
                rcoordx, rwidth = (int(rcoordx / tilewidth),
                                   int(rwidth / tilewidth))
                rcoordy, rheight = (int(rcoordy / tileheight),
                                    int(rheight / tileheight))

                # creamos un producto cartesiano y nos ahorramos overhead ;)
                # FIXME: existe un desface con las baldosas desde la capa 2
                # hasta la capa n+2.
                orentation = self.tmxdata.orientation
                if orentation == "orthogonal":
                    heightxrange = xrange(rcoordy,
                        rcoordy+self.tmxdata.height)
                elif orentation == "isometric":
                    heightxrange = xrange(rheight, rcoordy+1, -1)
                elif orentation == "staggered":
                    # FIXME: usar valores correctos para esta clase de orientacion
                    heightxrange = xrange(rheight, rcoordy+1, -1)

                cartprod = product(xrange(len(self.tmxdata.tilelayers)),
                                   heightxrange,
                                   xrange(rcoordx,
                                    rcoordx+self.tmxdata.width))
                layersvisibledata = []
                for layer in xrange(len(self.tmxdata.tilelayers)):
                    layerdata = self.tmxdata.getLayerData(layer)
                    visibledata = []
                    [visibledata.extend(x[rcoordx:rwidth])
                                        for x in layerdata[rcoordy:rheight]]
                    layersvisibledata.append(visibledata)
                    self.__vertexarraytodraw[layer].clear()

                # Esto deberia juntar todas las listas (1 por capa) en un
                # sólo objeto iterable.
                layersvisibledata = chain.from_iterable(layersvisibledata)

                for layer, coordy, coordx in cartprod:
                    # obtenemos la imagen de la baldosa
                    tilegid = layersvisibledata.next()
                    tilerect = self.tmxdata.images[tilegid]
                    if isinstance(tilerect, int):
                        # Necesitamos un espacio en blanco dentro del mapa
                        continue

                    # creamos algunos vertices
                    v1, v2, v3, v4 = (sfml.Vertex(),
                                      sfml.Vertex(),
                                      sfml.Vertex(),
                                      sfml.Vertex())

                    # mapeamos correctamente el vertice en la textura
                    v1.tex_coords = (tilerect.left, tilerect.top)
                    v2.tex_coords = (tilerect.right, tilerect.top)
                    v3.tex_coords = (tilerect.right, tilerect.bottom)
                    v4.tex_coords = (tilerect.left, tilerect.bottom)

                    # posicionamos el vertice en la pantalla
                    if orentation == "isometric":
                        # FIXME: No dibuja correctamente
                        v1.position = sfml.Vector2(
                            float((coordx * tilewidth / 2) + \
                                 (coordy * tilewidth / 2)),
                            float((coordy * tileheight / 2) - \
                                 (coordy * tileheight / 2)))
                        v2.position = sfml.Vector2(
                            v1.position.x + tilewidth, v1.position.y)
                        v3.position = sfml.Vector2(
                            v1.position.x + tilewidth, v1.position.y + tileheight)
                        v4.position = sfml.Vector2(
                            v1.position.x, v1.position.y + tileheight)
                    elif orentation == "orthogonal":
                        v1.position = sfml.Vector2(
                            float(coordx * tilewidth), float(coordy * tileheight))
                        v2.position = sfml.Vector2(v1.position.x + tilewidth,
                                                   v1.position.y)
                        v3.position = sfml.Vector2(v1.position.x + tilewidth,
                                                   v1.position.y + tileheight)
                        v4.position = sfml.Vector2(v1.position.x,
                                                   v1.position.y + tileheight)
                    elif orentation == "staggered":
                        # TODO: implementar el posicionamiento de mapas isometricos
                        # escalonados.
                        pass

                    # Agregamos el vertice a su VertexArray correspondiente
                    self.__vertexarraytodraw[layer].append(v1)
                    self.__vertexarraytodraw[layer].append(v2)
                    self.__vertexarraytodraw[layer].append(v3)
                    self.__vertexarraytodraw[layer].append(v4)

    def addsprite(self, entity):
        """ Agrega un sprite para ser dibujado en el escenario.

        Cada sprite es acomodado en una lista que representa la capa
        según su zindex, así, si el zindex de un sprite es 2, se colocara
        en la lista 2. el zindex de un  sprite no puede ser menor de 0 y
        mayor a la cantidad de capas en el escenario, de otro modo, se
        agregaran a la ultima lista que representa la ultima capa
        del escenario.
        """
        # verificamos el zindex de la entidad
        if not hasattr(entity, "zindex"):
            raise TypeError, "El parámetro recibido no es una entidad valida."

        if entity.zindex < 0:
            entity.zindex = 0 # Corregimos números negativos
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

        este método retorna la lista e índice en la
        cual se ubica el sprite.

        FIXME: mejorar transversion de la lista para
        cantidades enormes de sprites y cuidar el rendimiento
        de búsqueda.
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
        if self.tmxdata:
            #if self.dontdrawtiles:
            self.__refreshvisibletiles(self.scenemanager.window.view)
            states.texture = self.scenetileset
            drawables = chain.from_iterable(
                izip_longest(self.__vertexarraytodraw, self.sprites))
            # Limpiamos la pantalla antes de dibujar nada.
            target.clear(sfml.Color.BLACK)
            for drawable in drawables:
                if isinstance(drawable, list):
                    drawable.sort(key=lambda entity: entity.sprite.position.y)
                    for entity in drawable:
                        entity.on_draw()
                        target.draw(entity.sprite, states)
                elif isinstance(drawable, sfml.VertexArray):
                    target.draw(drawable, states)
        else:
            # Ningun mapa se cargo. No se dibuja las baldosas.
            target.clear(sfml.Color.WHITE)
            if self.sprites:
                self.sprites[-1].sort(
                    key=lambda entity: entity.sprite.position.y)
                for entity in self.sprites[-1]:
                    entity.on_draw()
                    target.draw(entity.sprite, states)

    def getmappixelsize(self):
        """Retorna las dimensiones del mapa en pixeles.
        """
        width = self.tmxdata.width * self.tmxdata.tilewidth
        height = self.tmxdata.height * self.tmxdata.tileheight
        return (width, height)

    def getmaptilesize(self):
        """Retorna las dimensiones del mapa en baldosas.
        """
        return (self.tmxdata.width, self.tmxdata.height)

    def gettilesize(self):
        """Retorna las dimensiones en pixeles de un baldosa.
        """
        return (self.tmxdata.tilewidth, self.tmxdata.tileheight)

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
        "Útil para darle un nombre a tu escena."
        raise NotImplementedError("Implemente el método __str__")
        # por ejemplo:
        #  return "<Scene: Escena #1, File: {0}>".format(self.__tmxmapfile)
        # o como usted más prefiera :)
