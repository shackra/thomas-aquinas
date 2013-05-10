# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, q"
tags = "is_event_handler, on_key_press"

import summa
from summa.director import director
from summa.sprite import Sprite
import pyglet

class PrintKey(summa.layer.Layer):
    is_event_handler = True
    def on_key_press (self, key, modifiers):
        print "Key Pressed:", key, modifiers

description = """
When pressing keys the key with modifiers should print on console
"""

def main():
    print description
    director.init()
    bg_layer = summa.layer.ColorLayer(255,0,0,255)
    test_layer = PrintKey()
    main_scene = summa.scene.Scene (bg_layer, test_layer)
    director.run (main_scene)

if __name__ == '__main__':
    main()
