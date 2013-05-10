# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

# this test is not adecuate for autotest, so no testinfo added
tags = "audio SDL"

import summa
from summa.director import director
from summa.audio.effect import Effect

def main():
    director.init(audio_backend='sdl')
    effect = Effect('powerup.wav')
    effect.play()
    import time
    time.sleep(2)

if __name__ == '__main__':
    main()
