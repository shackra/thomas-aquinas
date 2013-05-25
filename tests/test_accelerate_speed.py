# coding: utf-8

testinfo = "s, t 2, s, t 5, s, t 8, s, t 10.1, s, q"
tags = "Speed, Accelerate"

import summa
from summa.director import director
from summa.actions import Accelerate, Speed, Rotate
from summa.sprite import Sprite

from customstuff import TimedScene

class CustomLayer(summa.layer.Layer):
    def __init__(self):
        super( TestLayer, self ).__init__()
        x,y = director.get_window_size()
        self.sprite1 = Sprite( 'grossini.png', (x/4, y/2) )
        self.add( self.sprite1  )
        self.sprite2 = Sprite( 'grossini.png', ((x/4)*3, y/2)  )
        self.add( self.sprite2 )

        self.sprite1.do( Accelerate( Speed( Rotate( 360, 1 ), 0.1 ), 4)  )
        self.sprite2.do( Speed( Accelerate( Rotate( 360, 1 ), 4 ), 0.1)  )

def test_acc_speed():
    director.init()
    test_layer = CustomLayer()
    main_scene = TimedScene()
    main_scene.add(test_layer)
    director.run (main_scene)
