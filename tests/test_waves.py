# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 2, s, t 5.1, s, q"
tags = "Waves"

import summa
from summa.director import director
from summa.actions import *
from summa.layer import *
import pyglet
from pyglet import gl

class BackgroundLayer(summa.layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background_image.png')

    def draw( self ):
        glColor4ub(255, 255, 255, 255)
        glPushMatrix()
        self.transform()
        self.img.blit(0,0)
        glPopMatrix()

def main():
    director.init( resizable=True )
    main_scene = summa.scene.Scene()

    main_scene.add( BackgroundLayer(), z=0 )

    # In real code after a sequence of grid actions the StopGrid() action
    # should be called. Omited here to stay in the last grid action render
    main_scene.do( Waves( waves=6, hsin=True, vsin=True,
                          grid=(16,10), duration=5) )
    director.run (main_scene)

if __name__ == '__main__':
    main()
