# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 2.5, s, t 5.1, s, q"
tags = "MoveBy"

import summa
from summa.director import director
from summa.sprite import Sprite
from summa.actions import *
import pyglet

def main():
    director.init()
    bg_layer = summa.layer.ColorLayer(255,0,0,255)
    translate_layer = summa.layer.Layer()
    x, y = director.get_window_size()
    translate_layer.add( bg_layer )
    translate_layer.do( MoveBy( (x/2, y/2), 5) )
    main_scene = summa.scene.Scene (translate_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
