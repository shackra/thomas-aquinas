# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, q"
tags = "Layer, ColorLayer, child"

import summa
from summa.director import director
from summa.sprite import Sprite
import pyglet

def main():
    director.init()
    bg_layer = summa.layer.ColorLayer(255,0,0,255)
    translate_layer = summa.layer.Layer()
    x, y = director.get_window_size()
    translate_layer.x = x/2
    translate_layer.y = y/2
    translate_layer.add( bg_layer )
    main_scene = summa.scene.Scene (translate_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
