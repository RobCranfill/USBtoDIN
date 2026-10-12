'''
    Microcontroller project to adapt a USB-based MIDI controller to a DIN-based MIDI device.
    https://github.com/RobCranfill/USBtoDIN

    16-segment LED version.
'''
import board
import busio
import time
import usb.core
import usb_midi

import adafruit_midi
import adafruit_usb_host_midi


# Must import any events/objects you want to be able to handle. Weird.
# can't I just:
#   from adafruit_midi.* import *
# no. :-/
from adafruit_midi.active_sensing import *
from adafruit_midi.channel_pressure import *
from adafruit_midi.control_change import *
from adafruit_midi.control_change_values import *
from adafruit_midi.midi_continue import *
from adafruit_midi.midi_message import *
from adafruit_midi.midi_reset import *
from adafruit_midi.mtc_quarter_frame import *
from adafruit_midi.note_off import *
from adafruit_midi.note_on import *
from adafruit_midi.pitch_bend import *
from adafruit_midi.polyphonic_key_pressure import *
from adafruit_midi.program_change import *
from adafruit_midi.start import *
from adafruit_midi.stop import *
from adafruit_midi.system_exclusive import *
from adafruit_midi.timing_clock import *


PRINT = False

print(f"{__name__} starting....") if PRINT else False


# These are the human-readable channel numbers. X-1 will be sent.
MIDI_ALL_CHANNELS = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15) # range(16) # right?
MIDI_IN_CHANNEL = 1 # all?

MIDI_OUT_CHANNEL = 10 # On SR16, channel 1 is bass, 10 is drums


def panic(m):
    '''Do we need to do all channels? not really'''
    print("Turning off all MIDI notes")
    for chan in range(16):
        for note in range(128):
            m.send(NoteOff(note, chan))



# ----------------- start
print(f"\nrunning {__name__}") if PRINT else False

# Create UART first
#
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
print("UART OK") if PRINT else False


# Find MIDI device. This just assumes the first one found is appropriate.
#
print("looking for USB MIDI device...") if PRINT else False

print("Scanning USB bus...") if PRINT else False
midi_interfaces = None
for device in usb.core.find(find_all=True):
    try:
        print(f" * Found device {hex(device.idVendor)}:{hex(device.idProduct)}") if PRINT else False
        host_midi_in = adafruit_usb_host_midi.MIDI(device, timeout=0.1)
        print("Trying as MIDI device....") if PRINT else False
        try:
            midi_interfaces = adafruit_midi.MIDI(
                    midi_in=host_midi_in,
                    in_channel=MIDI_ALL_CHANNELS,
                    midi_out=uart,
                    out_channel = MIDI_OUT_CHANNEL-1
                    )
            print("  OK!") if PRINT else False
        except Exception as e:
            print(f"Not a MIDI device??? {e}") if PRINT else False
        break
    except Exception as e:
        print(f" EXCEPTION {e}") if PRINT else False
        continue

if midi_interfaces is None:
    print("CAN'T SET UP MIDI???")
else:
    print("MIDI OK!") if PRINT else False


# TODO: how? would this take place of 'panic'?
# midi_interfaces.send(Reset(MIDI_OUT_CHANNEL-1))

# panic(midi_interfaces)

# Play startup sound!
for n,v in [(48, 100), (48, 100), (49, 127)]:
    midi_interfaces.send(NoteOn(n, v))
    time.sleep(.15)

print("Ready!") if PRINT else False

# Is this all we do?
# Should we re-map anything? Filter anything?
#
# TODO: should we wrap this with try/catch somehow?
#
while True:
    msg = midi_interfaces.receive()
    if msg:

        # if isinstance(msg, ActiveSensing) or isinstance(msg, MIDIBadEvent):
        #     # print(f" ** BAD {msg}")
        #     continue

        # We pass on *every* MIDI message except the two bummers above.

        # print(f"    sending {msg} to DIN...")
        print(f"Sending to UART: {msg=}") if PRINT else False
        midi_interfaces.send(msg)
