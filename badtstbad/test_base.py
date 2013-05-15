# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, q"
tags = "ColorLayer"

import summa
from summa.director import director
from summa.sprite import Sprite
import pyglet


def main():
    director.init()
    test_layer = summa.layer.ColorLayer(255,0,0,255)
    main_scene = summa.scene.Scene (test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
