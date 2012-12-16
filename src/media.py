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
import os
import common

try:
    import sfml
except ImportError:
    logging.fatal("No se puede importar SFML, no existe en el sistema")
    raise

def loadmedia(mediafile, mediatype=None, toram=True):
    """ Retorna un objeto SFML.

    Cargamos un archivo audiovisual (sea una imagen, sonido o cancion) y
    retornamos el objeto SFML apropiado.
    el argumento 'mediatype' sirve para identificar de una vez el tipo de
    archivo multimedia (img para imagen, snd para sonido o msc para musica)
    Si dicho argumento esta en None, la funcion tratara de cargar el audio-
    visual de forma automatica (no recomendado para archivos de sonido y/o
    musicales. Por defecto tratara de devolver un objeto de sonido).

    'toram' nos indica si debemos cargar los archivos de imagen a la memoria
    RAM o a la memoria de la tarjeta de video. Si es True, cargara a la RAM"""
    mediapath = common.conf.fromrootfolderget(mediafile)
    extension = os.path.splitext(mediapath)[-1]

    # Tratamos de cargar el audiovisual segun
    # su tipo de archivo.

    if extension in ["bmp", "png", "tga", "jpg", "gif", "psd", "hdr", "pic"]:
        try:
            if toram:
                sfmlobject = sfml.Image.load_from_file(mediapath)
            else:
                sfmlobject = sfml.Texture.load_from_file(mediapath)
        except IOError:
            logging.exception("El archivo {arch} tiene una "
                          "extension incorrecta".format(arch=mediapath))
            raise
        except sfml.SFMLException as e:
            logging.exception("No se pudo cargar el archivo de imagen"
                              "{arch}, razón: {e}".format(arch=arch, e=e))

    elif extension in [".ogg", ".oga", ".mp3", ".flac", ".wav"]:
        try:
            if mediatype == "snd" or mediatype == None:
                soundbuffer = sfml.SoundBuffer.load_from_file(mediapath)
                sfmlobject = sfml.Sound(soundbuffer)
            elif mediatype == "msc":
                sfmlobject = sfml.Music.open_from_file(mediapath)
        except IOError:
            logging.error("El archivo {arch} tiene una "
                          "extension incorrecta".format(arch=mediapath))
            raise

    # copiar objetos no es necesario para objetos de SFML
    return sfmlobject

    def loadsong(mediafile):
        """ Retorna un objeto SFML para la música dado un archivo.
        """
        mediapath = common.conf.fromrootfolderget(mediafile)
        try:
            sfmlobject = sfml.Music.open_from_file(mediapath)
            return sfmlobject
        except IOError:
            logging.error("El archivo {arch} tiene una "
                          "extension incorrecta".format(arch=mediapath))
            raise

    def loadsound(mediafile):
        """ Retorna un objeto SFML para el sonido dado un archivo.
        """
        mediapath = common.conf.fromrootfolderget(mediafile)
        try:
            soundbuffer = sfml.SoundBuffer.load_from_file(mediapath)
            sfmlobject = sfml.Sound(soundbuffer)
            return sfmlobject
        except IOError:
            logging.error("El archivo {arch} tiene una "
                          "extension incorrecta".format(arch=mediapath))
            raise
