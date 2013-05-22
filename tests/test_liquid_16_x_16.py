# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 1.0, s, t 2.0"
tags = "Liquid"

import summa
from summa.director import director
from summa.actions import *
from summa.layer import *
import pyglet


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

    #main_scene.do( Liquid( waves=5, grid=(16,16), duration=10) + StopGrid() )
    main_scene.do( Liquid( waves=5, grid=(16,16), duration=10) )
    director.run (main_scene)

if __name__ == '__main__':
    main()
