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

import os
import logging
from lib import common
import sfml
from thirdparty.pitweener.src import PiTweener


class TAUnknownFileFormatException(Exception): pass

def loadmedia(mediafile, mediatype=None, toram=True):
    """ Retorna un objeto SFML.

    Cargamos un archivo audiovisual (sea una imagen, sonido o canción) y
    retornamos el objeto SFML apropiado.
    el argumento 'mediatype' sirve para identificar de una vez el tipo de
    archivo multimedia (img para imagen, snd para sonido o msc para musica)
    Si dicho argumento esta en None, la función tratara de cargar el audio-
    visual de forma automática (no recomendado para archivos de sonido y/o
    musicales. Por defecto tratara de devolver un objeto de sonido).

    'toram' nos indica si debemos cargar los archivos de imagen a la memoria
    RAM o a la memoria de la tarjeta de vídeo. Si es True, cargara a la RAM"""

    logging.info("Buscando por el audiovisual {0}".format(mediafile))
    extension = os.path.splitext(mediafile)[-1]
    logging.debug("Extensión del audiovisual: {0}".format(extension))

    if extension in [".bmp", ".png", ".tga", ".jpg",
                     ".gif", ".psd", ".hdr", ".pic"]:
        logging.debug("El archivo {0} es un"
                      " archivo de imagen".format(mediafile))
        return loadimg(mediafile, toram)

    elif extension in [".ogg", ".oga", ".mp3", ".flac", ".wav"]:
        logging.debug("El archivo {0} es un"
                      " archivo de audio".format(mediafile))
        if mediatype == "snd" or mediatype is None:
            return loadsound(mediafile)
        elif mediatype == "msc":
            return loadsong(mediafile)
    else:
        raise TAUnknownFileFormatException, ("formato de archivo "
                                             "{0} desconocido".format(
                                                 extension))

def loadsong(mediafile):
    """ Retorna un objeto SFML para la música dado un archivo.
    """
    mediapath = common.Conf.fromrootfolderget(mediafile)
    try:
        sfmlobject = sfml.Music.from_file(mediapath)
        logging.info("Cargado el archivo de musica {0}".format(mediapath))
        return sfmlobject
    except IOError:
        logging.error("El archivo {arch} tiene una "
                      "extensión incorrecta".format(arch=mediapath))
        raise

def loadsound(mediafile):
    """ Retorna un objeto SFML para el sonido dado un archivo.
    """
    mediapath = common.Conf.fromrootfolderget(mediafile)
    try:
        soundbuffer = sfml.SoundBuffer.from_file(mediapath)
        sfmlobject = sfml.Sound(soundbuffer)
        logging.info("Cargado el archivo de sonido {0}".format(mediapath))
        return sfmlobject
    except IOError:
        logging.error("El archivo {arch} tiene una "
                      "extensión incorrecta".format(arch=mediapath))
        raise

def loadbuffer(mediafile):
    """ Retorna un buffer de sonido SFML para uso posterior.
    """
    mediapath = common.Conf.fromrootfolderget(mediafile)
    try:
        soundbuffer = sfml.SoundBuffer.from_file(mediapath)
        logging.info("Cargado el archivo de "
                     "sonido {0} como buffer".format(mediapath))
        return soundbuffer
    except IOError:
        logging.error("El archivo {arch} tiene una "
                      "extensión incorrecta".format(arch=mediapath))
        raise

def loadimg(mediafile, toram=True):
    """ Retorna un objeto imagen SFML dado un archivo.
    """
    mediapath = common.Conf.fromrootfolderget(mediafile)
    try:
        img = sfml.Image.from_file(mediapath)
        if toram:
            logging.info("Cargado el archivo de imagen {0}".format(mediapath))
            return img
        else:
            logging.info("Cargado el archivo de imagen a"
                         " memoria de vídeo {0}".format(mediapath))
            return sfml.Texture.from_image(img)
    except IOError:
        logging.error("El archivo {arch} tiene una "
                      "extensión incorrecta".format(arch=mediapath))
        raise

class MusicManager:
    """ Esta clase se encarga de manejar la musica que sonara durante el juego.

    Esta clase no debe ser instanciada, ya que puede manejar
    varias pistas de musica a la vez.
    """
    songs = {}
    musictweener = PiTweener.Tweener()
    actualsong = None
    __nextsongtoplay = None

    def __init__(self):
        raise UserWarning, "¡No me instancies!"

    @classmethod
    def updatetweener(cls, time):
        """ Actualiza el tweener, entre otras cosas.
        """
        cls.musictweener.update(time)
        if cls.actualsong.volume == 0 and cls.__nextsongtoplay:
            songname, play_offset, loop = cls.__nextsongtoplay
            cls.actualsong.stop()
            cls.actualsong.volume = 100
            cls.playsong(songname, play_offset, loop)
            cls.__nextsongtoplay = None

    @classmethod
    def _alreadyexists(cls, filename):
        """ Ya existe esta canción que pretendemos cargar?
        """
        songname = os.path.basename(filename)
        return not cls.songs.has_key(songname)

    @classmethod
    def loadsong(cls, filename):
        """ Carga una canción para ser reproducid a demanda.
        """
        if not cls._alreadyexists(filename):
            songname = os.path.basename(filename)
            logging.info("Cargando canción: {0}".format(songname))
            cls.songs[songname] = loadsong(filename)
        else:
            logging.warning("Canción {0} ya había sido cargada".format(
                    os.path.basename(filename)))
            raise UserWarning, "Esta canción ya a sido cargada!"

    @classmethod
    def playsong(cls, songname, play_offset=0, loop=True):
        """ Reproduce determinada canción.

        'play_offset' indica la nueva posición donde comenzara a
        sonar la musica. Esto se aplica DESPUÉS de iniciar la reproducción.
        el tiempo se expresa en milisegundos.
        'loop' al ser falso, reproduce la musica una sola vez. de lo contrario
        reproducirá la canción por siempre en bucle.
        """
        if hasattr(cls.actualsong, "play"):
            # tiene el volumen en 0 la canción actual?
            if cls.actualsong == 0:
                # detenemos la canción y le restablecemos el volumen
                cls.actualsong.stop()
                cls.actualsong.volume = 100.0

        try:
            cls.actualsong = cls.songs[songname]
            cls.actualsong.loop = loop
            cls.actualsong.play()
            cls.actualsong.playing_offset = sfml.milliseconds(play_offset)
        except KeyError:
            logging.exception("Canción {0} no a "
                              "sido cargada o no existe".format(songname))

    @classmethod
    def fadeoutandplaysong(cls, fadeout, nsongname,
                           nsongplay_offset, nsong_loop):
        """ Cambia de canción de forma suave.

        'fadeout' es la cantidad de tiempo (en segundos) en la
        que se bajara el volumen de la canción actual hasta 0.
        'nsongname' es el nombre de la siguiente canción a reproducir.
        'nsongplay_offset' es el nuevo offset para el inicio de la siguiente
        canción, ver playsong() para más información.
        'nsong_loop' indica sí se desea que la siguiente canción se
        repita de forma indefinida.
        """
        cls.musictweener.add_tween(cls.actualsong,
                                   volume=0.0,
                                   tween_time=fadeout,
                                   tween_type=cls.musictweener.LINEAR,
                                   # on_complete_function = cls.playsong(
                                   # nsongname,
                                   # nsongplay_offset,
                                   # nsong_loop)
                                   )
        cls.__nextsongtoplay = [nsongname, nsongplay_offset, nsong_loop]

    @classmethod
    def pausesong(cls):
        """ Pausa la reproducción de la canción actual.
        """
        cls.actualsong.pause()

    @classmethod
    def unpausesong(cls):
        """ Continua la reproducción de la canción actual.
        """
        cls.actualsong.play()

    @classmethod
    def stopsong(cls):
        """ Detiene la reproducción de la canción actual.
        """
        cls.actualsong.stop()


class SoundFXManager:

    buffers = {}
    
    def __init__(self):
        raise UserWarning, "No me instancies!"

    @classmethod
    def _alreadyexists(cls, filename):
        """ Ya existe esta canción que pretendemos cargar?
        """
        buffername = os.path.basename(filename)
        return not cls.buffers.has_key(buffername)

    @classmethod
    def loadbuffer(cls, filename):
        """ Carga un archivo de sonido en un buffer.
        """
        buffername = os.path.basename(filename)
        if not cls._alreadyexists(filename):
            logging.info("Cargando audio a buffer: {0}".format(buffername))
            cls.buffers[buffername] = loadbuffer(filename)
        else:
            logging.warning("Audio {0} ya había "
                            "sido caragado como buffer.".format(buffername))
            raise UserWarning, "Este audio ya a sido cargado como buffer!"

    @classmethod
    def setentitysndfx(cls, entity):
        """ Establece todos los efectos de sonido que una entidad necesite.

        Las entidades que quieran efectos de sonido, deben poseer la propiedad
        entity._sndfx el cual es un diccionario. Las palabras claves del
        diccionario son los nombres de los efectos de sonido y los valores
        son objetos SFML Sound. Todos los objetos SFML Sound de cada entidad
        comparten la posición espacial de entity.sprite
        """
        if hasattr(entity, "_sndfx"):
            for soundname in entity._sndfx.iterkeys():
                try:
                    entity._sndfx[soundname] = sfml.Sound(
                        cls.buffers[soundname])
                    # Estableciendo la posición del sonido con respecto a la
                    # posición del sprite de la entidad.
                    entityposx, entityposy = entity.sprite.position
                    entity._sndfx[soundname].position = sfml.Vector3(entityposx,
                    entityposy,
                    0.0)
                except KeyError:
                    logging.error("Buffer {0} aun no a sido cargado. "
                        "No se puede crear el sonido para"
                        " la entidad {1}".format(soundname, entity.id))
                    raise UserWarning, ("No se pudo cargar un sonido"
                                    " para la entidad {0}".format(entity.id))
        else:
            logging.info("La entidad {0} no requiere de sonidos".format(
            entity.id))
