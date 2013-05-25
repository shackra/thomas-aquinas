# coding: utf-8
testinfo = "s, t 1.0, s, t 2.1, s, q"
tags = "transform_anchor, Rotate"

import summa
from summa.director import director
from summa.sprite import Sprite
from summa import actions

from customstuff import TimedScene

class CustomLayer(summa.layer.Layer):
    def __init__(self):
        super( CustomLayer, self ).__init__()

        x, y = director.get_window_size()

        sprite1 = Sprite('grossini.png')
        sprite1.position = x/4, y/2
        self.add(sprite1)

        sprite2 = Sprite('grossini.png')
        sprite2.position = x/4, y/2
        self.add(sprite2, z=2)
        sprite2.scale = 0.3

        sprite2.do( actions.RotateBy(duration=2, angle=360) )
        sprite1.do( actions.RotateBy(duration=2, angle=-360) )

        sprite1.transform_anchor = 0, 0

        sprite3 = Sprite('grossini.png')
        sprite3.position = 3*x/4, y/2
        self.add(sprite3)

        sprite4 = Sprite('grossini.png')
        sprite4.position = 3*x/4, y/2
        self.add(sprite4, z=2)
        sprite4.scale = 0.3

        sprite3.do( actions.RotateBy(duration=2, angle=360) )
        sprite4.do( actions.RotateBy(duration=2, angle=-360) )

        sprite3.transform_anchor = sprite3.image.width/2, sprite3.image.height/2

def test_anchor_sprites():
    director.init()
    test_layer = CustomLayer()
    main_scene = TimedScene(test_layer)
    director.run (main_scene)
