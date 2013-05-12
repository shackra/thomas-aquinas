# coding: utf-8
# Copyright (c) 2013 Jorge Javier Araya Navarro <jorgean@lavabit.org>
#
# This file is free software: you may copy, redistribute and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#     cocos2d
#     Copyright (c) 2008-2012 Daniel Moisset, Ricardo Quesada, Rayentray Tappa,
#     Lucio Torre
#     All rights reserved.
#
#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions are met:
#
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above copyright
#         notice, this list of conditions and the following disclaimer in
#         the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of cocos2d nor the names of its
#         contributors may be used to endorse or promote products
#         derived from this software without specific prior written
#         permission.
#
#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#     "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#     LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#     FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#     COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#     INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#     BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#     LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#     ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#     POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------
"""
Scene class and subclasses
"""
__docformat__ = 'restructuredtext'

__all__ = ['Scene']

from pyglet import gl

import summa
from summa.director import director
import summa.summanode as summanode
import summa.audio.music

class EventHandlerMixin(object):
    def add(self, child, *args, **kwargs):
        super(EventHandlerMixin, self).add(child, *args, **kwargs)

        scene = self.get(Scene)
        if not scene: return

        if (    scene._handlers_enabled and
                scene.is_running and
                isinstance(child, summa.layer.Layer)
                ):
            child.push_all_handlers()


    def remove(self, child):
        super(EventHandlerMixin, self).remove(child)

        scene = self.get(Scene)
        if not scene: return

        if (    scene._handlers_enabled and
                scene.is_running and
                isinstance(child, summa.layer.Layer)
                ):
            child.remove_all_handlers()




class Scene(summanode.SummaNode, EventHandlerMixin):
    """
    """

    def __init__(self, *children):
        """
        Creates a Scene with layers and / or scenes.

        Responsibilities:
            Control the dispatching of events to its layers; and background music playback

        :Parameters:
            `children` : list of `Layer` or `Scene`
                Layers or Scenes that will be part of the scene.
                They are automatically assigned a z-level from 0 to
                num_children.
        """

        super(Scene,self).__init__()
        self._handlers_enabled = False
        for i, c in enumerate(children):
            self.add( c, z=i )

        x,y = director.get_window_size()

        self.transform_anchor_x = x/2
        self.transform_anchor_y = y/2
        self.music = None
        self.music_playing = False

    def on_enter(self):
        for c in self.get_children():
            c.parent = self
        super(Scene, self).on_enter()
        if self.music is not None:
            summa.audio.music.control.load(self.music)
        if self.music_playing:
            summa.audio.music.control.play()

    def on_exit(self):
        super(Scene, self).on_exit()
        # _apply_music after super, because is_running must be already False
        if self.music_playing:
            summa.audio.music.control.stop()


    def push_all_handlers(self):
        for child in self.get_children():
            if isinstance(child, summa.layer.Layer):
                child.push_all_handlers()

    def remove_all_handlers(self):
        for child in self.get_children():
            if isinstance(child, summa.layer.Layer):
                child.remove_all_handlers()

    def enable_handlers(self, value=True):
        """
        This function makes the scene elegible for receiving events
        """
        if value and not self._handlers_enabled and self.is_running:
            self.push_all_handlers()
        elif not value and self._handlers_enabled and self.is_running:
            self.remove_all_handlers()
        self._handlers_enabled = value


    def end(self, value=None):
        """Ends the current scene setting director.return_value with `value`

        :Parameters:
            `value` : anything
                The return value. It can be anything. A type or an instance.
        """
        director.return_value = value
        director.pop()

    def load_music(self, filename):
        """This prepares a streamed music file to be played in this scene.

        Music will be stopped after calling this (even if it was playing before).

        :Parameters:
            `filename` : fullpath
                Filename of music to load.
                Depending on installed libraries, supported formats may be
                WAV, MP3, OGG, MOD;
                You can also use 'None' to unset music
        """
        self.music = filename
        self.music_playing = False
        if self.is_running:
            if filename is not None:
                summa.audio.music.control.load(filename)
            else:
                summa.audio.music.control.stop()

    def play_music(self):
        """Enable music playback for this scene. Nothing happens if music was already playing

        Note that if you call this method on an inactive scene, the music will
        start playing back only if/when the scene gets activated.
        """
        if self.music is not None and not self.music_playing:
            self.music_playing = True
            if self.is_running:
                summa.audio.music.control.play()

    def stop_music(self):
        """Stops music playback for this scene.
        """
        self.load_music(None)
