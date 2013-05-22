# coding: utf-8
testinfo = "s, t 4, s, t 8, s, t 10.1, s, q"
tags = "Accelerate"

from summa.layer import Layer
from summa.director import director
from summa.actions import Accelerate, Rotate
from summa.sprite import Sprite
import customstuff
import pyglet
import os

pyglet.resource.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__))))
pyglet.resource.reindex()


class TestLayer(Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x, y = director.get_window_size()

        self.sprite = Sprite( 'grossini.png',  (x/2, y/2)  )
        self.add( self.sprite )
        self.sprite.do( Accelerate( Rotate( 360, 10 ), 4 ) )

def test_accelerate():
    director.init()
    test_layer = TestLayer()
    main_scene = customstuff.TimedScene(test_layer)
    director.run(main_scene)
