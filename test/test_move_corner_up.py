# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 0.33, s, t 0.66, s, t 1.1, s, q"
tags = "MoveCornerUp"

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
    director.init( resizable=True )
    main_scene = summa.scene.Scene()

    main_scene.add( BackgroundLayer(), z=0 )

    e = MoveCornerUp( duration=1 )
    main_scene.do( e )

    director.run( main_scene )

if __name__ == '__main__':
    main()
