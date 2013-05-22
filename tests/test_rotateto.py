# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 1.5, s, t 3.1, s, q"
tags = "RotateTo"

import summa
from summa.director import director
from summa.sprite import Sprite
import pyglet

class TestLayer(summa.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.sprite = Sprite( 'grossini.png', (x/4, y/4), rotation=355 )
        self.add( self.sprite )
        self.sprite.do( summa.actions.RotateTo( 45, 3 ) )

        self.sprite = Sprite( 'grossini.png', (x/4*3, y/4) )
        self.add( self.sprite )
        self.sprite.do( summa.actions.RotateTo( -45, 3 ) )

        self.sprite = Sprite( 'grossini.png', (x/4, y/4*3), rotation=135 )
        self.add( self.sprite )
        self.sprite.do( summa.actions.RotateTo( 45, 3 ) )

        self.sprite = Sprite('grossini.png', (x/4*3, y/4*3), rotation=135)
        self.add( self.sprite )
        self.sprite.do( summa.actions.RotateTo( -45, 3 ) )

def main():
    director.init()
    test_layer = TestLayer ()
    main_scene = summa.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
