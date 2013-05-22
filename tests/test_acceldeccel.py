# coding: utf-8
import pyglet
import summa
from summa.director import director
from summa.actions import AccelDeccel, MoveBy, Reverse, Repeat
from summa.layer import Layer
from summa.sprite import Sprite
import os

import customstuff

pyglet.resource.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__))))
pyglet.resource.reindex()

testinfo = "s, t 2.0, s, t 4.1, s, q"
tags = "AccelDeccel"

class TestLayer(Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x, y = director.get_window_size()

        self.sprite = Sprite('grossini.png', (0, y/2) )
        self.add(self.sprite)
        mov = AccelDeccel(MoveBy((x, 0 ), 4))
        self.sprite.do(Repeat(mov + Reverse(mov)))

def test_acceldeccel():
    director.init()
    test_layer = TestLayer()
    main_scene = customstuff.TimedScene(test_layer)
    director.run(main_scene)
