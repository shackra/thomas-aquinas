# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 1, s, t 2, s, t 3, s, t 4.1, s, q"
tags = "ScaleBy"

import summa
from summa.director import director
from summa.actions import ScaleBy
from summa.sprite import Sprite
import pyglet

class TestLayer(summa.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.sprite = Sprite( 'grossini.png', (x/2,y/2), scale = 0.1 )
        self.add( self.sprite )
        self.sprite.do( ScaleBy( 10, 2 ) + ScaleBy( 0.1, 2 )  )

def main():
    director.init()
    test_layer = TestLayer ()
    main_scene = summa.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
