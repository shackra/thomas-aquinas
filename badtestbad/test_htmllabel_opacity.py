# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 5, s, t 10.1, s, q"
tags = "HTMLLabel, text, FadeOut"

import summa
from summa.director import director
from summa.sprite import Sprite
from summa.actions import *
from summa.text import *

import pyglet

class TestLayer(summa.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.text = HTMLLabel("<font color=red>hello <i>world</i></font>", (x/2, y/2))
        self.text.do( FadeOut(10) )
        self.add( self.text  )

def main():
    director.init()
    test_layer = TestLayer ()
    main_scene = summa.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()