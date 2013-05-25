# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 0.5, s, t 1, s, t 1.5, s, t 2.1, s, q"
tags = "ZoomTransition"

import summa
from summa.director import director
from summa.actions import *
from summa.layer import *
from summa.scenes import *
from summa.sprite import *
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


def change_scene():
    scene1 = summa.scene.Scene()
    scene1.add( BackgroundLayer(), z=0 )
    director.replace( ZoomTransition(scene1, 2) )

def main():
    director.init( resizable=True )
    scene2 = summa.scene.Scene()

    colorl = ColorLayer(32,32,255,255)
    sprite = Sprite( 'grossini.png', (320,240) )
    colorl.add( sprite )

    scene2.add( colorl, z=0 )
    scene2.do(Delay(0.05) + CallFunc(change_scene))
    director.run(scene2)

if __name__ == '__main__':
    main()
