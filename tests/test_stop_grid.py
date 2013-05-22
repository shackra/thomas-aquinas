#
# Cocos:
# http://code.google.com/p/los-summa/
#
# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 2, s, t 5.1, s, q"
tags = "StopGrid"

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

description = """
After a grid action the action StopGrid should be called to restore the
normal view. Here we go with a 2 seconds FlipX3D drid action, followed
by StopGrid.
"""

def main():
    print description
    director.init( resizable=True )
    main_scene = summa.scene.Scene()

    main_scene.add( BackgroundLayer(), z=0 )

    main_scene.do( FlipX3D(duration=2) + Delay(2) + StopGrid() )
    director.run (main_scene)

if __name__ == '__main__':
    main()
