# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, q"
tags = "skeleton, animation"

import summa
from summa.director import director
from summa.sprite import Sprite
from summa import skeleton
import pyglet

import sample_skeleton

class TestLayer(summa.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()
        self.skin = skeleton.ColorSkin(sample_skeleton.skeleton,
                                        (255,0,0,255))
        self.add( self.skin )
        x, y = director.get_window_size()
        self.skin.position = x/2, y/2

def main():
    director.init()
    test_layer = TestLayer()
    bg_layer = summa.layer.ColorLayer(255,255,255,255)
    main_scene = summa.scene.Scene()
    main_scene.add(bg_layer, z=-10)
    main_scene.add(test_layer, z=10)
    director.run(main_scene)

if __name__ == '__main__':
    main()
