# coding: utf-8

testinfo = "s, t 0.77, s, q"
tags = "animation"


from nose.tools import nottest
import summa
from summa.director import director
from summa.sprite import Sprite
import pyglet

from customstuff import TimedScene
import os

pyglet.resource.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__))))
pyglet.resource.reindex()


class TestLayer(summa.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()

        x,y = director.get_window_size()

        self.sprite = Sprite(pyglet.resource.animation('dinosaur.gif'))
        self.sprite.position = x/2, y/2
        self.add(self.sprite)

# esta causando fallos de segmentación en la prueba
@nottest
def test_animation():
    director.init()
    test_layer = TestLayer()
    main_scene = TimedScene(test_layer)
    director.run(main_scene)
