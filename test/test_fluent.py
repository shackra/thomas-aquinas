# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, q"
tags = "CocosNode, child"

import summa
from summa.director import director
from summa.sprite import Sprite
import pyglet

def main():
    director.init()
    x,y = director.get_window_size()

    main_scene = (
        summa.scene.Scene()
            .add( summa.layer.ColorLayer( 255,255,0,255) )
            .add( summa.layer.Layer()
                .add( Sprite('grossini.png', (x/2, y/2))
            )
        )
    )
    director.run (main_scene)

if __name__ == '__main__':
    main()
