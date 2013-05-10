# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 0.5, s, t 1, s, t 1.5, s, t 2.1, s, q"
tags = "FadeUpTransition"

import summa
from summa.director import director
from summa.actions import *
from summa.layer import *
from summa.scenes import *
from summa.sprite import *
import pyglet
from pyglet.gl import *

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
    scene1 = summa.scene.Scene()
    scene2 = summa.scene.Scene()

    colorl = ColorLayer(32,32,255,255)
    sprite = Sprite( 'grossini.png', (320,240) )
    colorl.add( sprite )

    scene1.add( BackgroundLayer(), z=0 )
    scene2.add( colorl, z=0 )

    director.run( FadeUpTransition( scene1, 2, scene2) )

if __name__ == '__main__':
    main()
