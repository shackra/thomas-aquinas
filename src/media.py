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
import common

class TAUnknownFileFormatException(Exception): pass

try:
    import sfml
except ImportError:
    logging.fatal("No se puede importar SFML, no existe en el sistema")
    raise

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
        if mediatype == "snd" or mediatype == None:
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
    mediapath = common.settings.fromrootfolderget(mediafile)
    try:
        sfmlobject = sfml.Music.open_from_file(mediapath)
        logging.info("Cargado el archivo de musica {0}".format(mediapath))
        return sfmlobject
    except IOError:
        logging.error("El archivo {arch} tiene una "
                      "extensión incorrecta".format(arch=mediapath))
        raise

def loadsound(mediafile):
    """ Retorna un objeto SFML para el sonido dado un archivo.
    """
    mediapath = common.settings.fromrootfolderget(mediafile)
    try:
        soundbuffer = sfml.SoundBuffer.load_from_file(mediapath)
        sfmlobject = sfml.Sound(soundbuffer)
        logging.info("Cargado el archivo de sonido {0}".format(mediapath))
        return sfmlobject
    except IOError:
        logging.error("El archivo {arch} tiene una "
                      "extensión incorrecta".format(arch=mediapath))
        raise
        
def loadimg(mediafile, toram=True):
    """ Retorna un objeto imagen SFML dado un archivo.
    """
    mediapath = common.settings.fromrootfolderget(mediafile)
    try:
        img = sfml.Image.load_from_file(mediapath)
        if toram:
            logging.info("Cargado el archivo de imagen {0}".format(mediapath))
            return img
        else:
            logging.info("Cargado el archivo de imagen a"
                         " memoria de vídeo {0}".format(mediapath))
            return sfml.Texture.load_from_image(img)
    except IOError:
        logging.error("El archivo {arch} tiene una "
                      "extensión incorrecta".format(arch=mediapath))
        raise