# open MIDI device, show messages received.
# works on all MIDI devices except DM6

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

# my code
import fw128x64OLED


print(f"{__name__} starting....")

# These are the human-readable channel numbers. X-1 will be sent.
MIDI_ALL_CHANNELS = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15) # range(16) # right?
MIDI_IN_CHANNEL = 1 # all?

MIDI_OUT_CHANNEL = 10 # On SR16, channel 1 is bass, 10 is drums


SPINNER = "|/-\\"
SPINDEX = 0

def spin(d):
    global SPINDEX, SPINNER
    SPINDEX = (SPINDEX+1) % len(SPINNER)
    d.set_text_2(SPINNER[SPINDEX])


def panic(m):
    '''Do we need to do all channels? not really'''
    print("Turning off all MIDI notes")
    for chan in range(16):
        for note in range(128):
            m.send(NoteOff(note, chan))


# ----------------- start


display = fw128x64OLED.display()
display.set_text_1(f"{__name__} starting...")
# display.set_text_2("")

print(f"\nrunning {__name__}")
print("looking for USB MIDI device...")

# I'd like to scan the USB bus for all devices,
# and find at least one that supports MIDI.
# The following code does not do that. :-/
#
display.set_text_1("No MIDI input...")


print("Scanning USB bus...")
time.sleep(1)
n_found = 0
host_midi_in = None
for device in usb.core.find(find_all=True):
    n_found += 1
    try:
        print(f"  Found device {hex(device.idVendor)}:{hex(device.idProduct)}")
        host_midi_in = adafruit_usb_host_midi.MIDI(device, timeout=0.1)
        # count number of *MIDI* devices?
        break
    except Exception as e:
        print(f" EXCEPTION {e}")
        continue
    if host_midi_in is None:
        time.sleep(1)
print(f"  Found {n_found} USB host device(s)...")

uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)

if n_found > 0:

    print("Trying as MIDI device....")
    midi_in = None
    try:
        midi = adafruit_midi.MIDI(
                midi_in=host_midi_in,
                midi_out=uart,
                in_channel=MIDI_ALL_CHANNELS,
                out_channel = MIDI_OUT_CHANNEL-1
                )
        print("  OK!")
    except Exception as e:
        print(f"Not a MIDI device??? {e}")

else:
    # Use built-in MIDI input from USB power cable?

    print("Using built-in MIDI?.....")
    midi = adafruit_midi.MIDI(

        midi_in = usb_midi.ports[0],
        midi_out = uart,

        in_channel = MIDI_ALL_CHANNELS,
        out_channel = MIDI_OUT_CHANNEL-1,

        debug = False
        )
    print("Built-in MIDI OK?")



print("ta DUM!")
midi.send(NoteOn(48, 100))
time.sleep(.5)
midi.send(NoteOn(48, 100))
time.sleep(.5)
midi.send(NoteOn(48, 100))
print("ta DUM!")
time.sleep(2)

panic(midi)


# midi_in = midi_in._midi_in 
# print(f"MIDI device: {midi_in}")
# display.set_text_1(midi_in)

print("Ready!")

while True:
    msg = midi.receive()
    if msg:
        if isinstance(msg, ActiveSensing):
            pass
        else:
            print(f"Got {msg}")
            if midi is not None:

                # msg.channel = 10
                # print(f"    sending {msg} to DIN...")
                midi.send(msg)

                # have to override the channel!
                msg2 = NoteOn(msg.note, msg.velocity, channel=MIDI_OUT_CHANNEL-1)
                print(f" >>   sending {msg2} to DIN...")
                # midi.send(msg2)

