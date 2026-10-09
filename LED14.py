'''
Class to support use of Adafruit 14-segment LED display.
'''

import board
import time

import adafruit_ht16k33.segments



class display():
    '''Wrapper for 16-segment display'''

    def __init__(self, intial_text):
        print(f"{__name__}.__init()__")
        # option from constructor?
        i2c = board.STEMMA_I2C()

        self._display = adafruit_ht16k33.segments.Seg14x4(i2c)
        self._text = intial_text

    def set_text(self, text):
        pass

    def update_scroll(self):
        self._display.marquee(self._text, loop=False)

    def test():
        d = display("Testing 1,2,3,4....   ")
        for i in range(100):
            time.sleep(.01)
            d.update_scroll()
