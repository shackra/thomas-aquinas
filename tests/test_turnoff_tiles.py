# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 1, s, t 2.1, s, q"
tags = "TurnOffTiles"

import pyglet
import summa
from summa.director import director
from summa.actions import *
from summa.layer import *


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
    director.init( resizable=True, fullscreen=False )
    main_scene = summa.scene.Scene()

    main_scene.add( BackgroundLayer(), z=0 )

    e = TurnOffTiles( grid=(16,12), duration=2 )

    # In real code after a sequence of grid actions the StopGrid() action
    # should be called. Omited here to stay in the last grid action render
    main_scene.do( e )
    director.run (main_scene)

if __name__ == '__main__':
    main()
