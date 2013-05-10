# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, q"
tags = "PythonInterpreterLayer"

import summa
from summa.director import director
import pyglet

def main():
    director.init( resizable=True )
    interpreter_layer = summa.layer.PythonInterpreterLayer()
    main_scene = summa.scene.Scene(interpreter_layer)
    director.run(main_scene)

if __name__ == '__main__':
    main()
