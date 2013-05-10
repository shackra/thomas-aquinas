# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 0.49, s, t 0.51, s, t 2.49, s, t 2.51, s, t 2.99, s, t 3.1, s, q"
tags = "ShuffleTiles, Reverse"

import pyglet
import summa
from summa.director import director
import summa.actions as ac
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

    action1 = ac.ShuffleTiles( grid=(16,8), seed=2, duration=3 )
    action1 = ac.Reverse(action1)
    
    # In real code after a sequence of grid actions the StopGrid() action
    # should be called. Omited here to stay in the last grid action render
    main_scene.do( action1 )
    director.run (main_scene)

if __name__ == '__main__':
    main()
