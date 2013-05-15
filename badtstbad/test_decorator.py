# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 1.1, s, q"
tags = "CallFuncS"

import summa
from summa.director import director
from summa.actions import CallFuncS, Show, Delay
from summa.sprite import Sprite
import pyglet

class TestLayer(summa.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.sprite = Sprite('grossini.png', (x/2, y/2) )
        self.sprite.visible = False
        self.add( self.sprite )

        @CallFuncS
        def make_visible( sp ):
            sp.do( Show() )
        self.sprite.do( Delay(1) + make_visible )

description = """Sprite grossini starts invisible, after 1 second will turn
visible thanks to actions CallFuncS and Show
"""

def main():
    print description
    director.init()
    test_layer = TestLayer ()
    main_scene = summa.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
