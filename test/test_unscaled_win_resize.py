# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 1, s, q"
tags = "director.init, do_not_scale"
autotest = 0

import summa
from summa.director import director
from summa.actions import MoveTo, Delay, CallFunc
from summa.sprite import Sprite
import pyglet

class TestLayer(summa.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.sprite = Sprite( 'grossini.png' )
        self.add( self.sprite )
        self.sprite.do( MoveTo( (x,y), 10 ) )
        if autotest:
            self.do(Delay(1) + CallFunc(self.resize))

    def resize(self):
        director.window.set_size(600, 600)

description = """
Using do_not_scale=True in director.init, content will not
be scaled on resize. Use ctrl-f to toggle fullscreen
"""

def main():
    print description
    director.init(width=300, height=300, do_not_scale=True)
    test_layer = TestLayer ()
    main_scene = summa.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
