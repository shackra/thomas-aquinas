# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, t 1, s, t 1.9, s, t 2.1, s, q"
tags = "transform_anchor, scale"

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
    sub = summa.scene.Scene( bg_layer )
    sub.transform_anchor = (0, 0)    
    sub.scale = 0.5

    sub.do( MoveBy( (x/2, y/2), 2) )
    sub.do( ScaleBy( 0.5, 2) )
    main_scene = summa.scene.Scene (sub)
    director.run (main_scene)

if __name__ == '__main__':
    main()
