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

        # pass as option in constructor?
        i2c = board.STEMMA_I2C()

        self._display = adafruit_ht16k33.segments.Seg14x4(i2c)

        # TODO is this useful???
        self._text = intial_text

        self._display.print(intial_text)

    def print(self, text):
        '''Expose the simple 'print' method'''
        self._display.print(text)

    def set_text(self, text):
        pass

    
    def marquee_once(self, m_text):
        self._display.marquee(m_text, loop=False)
    
    def marquee_forever(self, m_text):
        self._display.marquee(m_text, loop=True)

    def update_scroll(self, m_text):
        self._display.marquee(m_text, loop=False)

    def set_brightness(self, brightness):
        '''Brightness 0.0 - 1.0'''
        self._display.brightness = brightness


    def test():
        d = display("Testing 1,2,3,4....   ")
        for i in range(100):
            time.sleep(.01)
            d.update_scroll()
