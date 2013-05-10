# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 4, s, t 8, s, t 10.1, s, q"
tags = "Accelerate"

import summa
from summa.director import director
from summa.actions import Accelerate, Rotate
from summa.sprite import Sprite
import pyglet

class TestLayer(summa.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.sprite = Sprite( 'grossini.png',  (x/2, y/2)  )
        self.add( self.sprite )
        self.sprite.do( Accelerate( Rotate( 360, 10 ), 4 ) )

def main():
    director.init()
    test_layer = TestLayer ()
    main_scene = summa.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
