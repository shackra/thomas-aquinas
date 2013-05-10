# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, q"
tags = "Draw, Line"

import summa
from summa.director import director
from summa import draw
import pyglet, math


class TestLayer(summa.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()
        line = draw.Line((0,0), (100,100), (255,255,255,255))
        self.add( line )

def main():
    director.init()
    test_layer = TestLayer ()
    main_scene = summa.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
