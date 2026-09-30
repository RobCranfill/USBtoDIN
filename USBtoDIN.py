# open MIDI device, show messages received.
# works on all MIDI devices except DM6

import board
import busio
import time
import usb.core

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

import fw128x64OLED


print(f"{__name__} starting....")

MIDI_IN_CHANNEL = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15) # range(16) # right?
MIDI_OUT_CHANNEL = 10 # On SR16, channel 1 is bass, 10 is drums


SPINNER = "|/-\\"
SPINDEX = 0

def spin(d):
    global SPINDEX, SPINNER
    SPINDEX = (SPINDEX+1) % len(SPINNER)
    d.set_text_2(SPINNER[SPINDEX])

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

import usb_midi

def get_builtin_midi():
    '''Use the MIDI that comes in on the power cable?'''
    # from  https://learn.adafruit.com/qt-py-rp2040-usb-to-serial-midi-friends/coding-the-qt-py-rp2040-usb-to-serial-midi-friends

    midi = adafruit_midi.MIDI(

        midi_in=usb_midi.ports[0],
        midi_out=None,

        in_channel=MIDI_IN_CHANNEL,
        # in_channel = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),

        # out_channel=(midi_out_channel - 1),
        out_channel = None,

        debug=True
    )
    return midi


print("scanning USB bus...")
time.sleep(1)
n_found = 0
raw_midi_in = None
for device in usb.core.find(find_all=True):
    n_found += 1
    try:
        raw_midi_in = adafruit_usb_host_midi.MIDI(device, timeout=0.1)
        print(f"Found device {hex(device.idVendor)}:{hex(device.idProduct)}")
    except Exception as e:
        print(f" EXCEPTION {e}")
        continue
    if raw_midi_in is None:
        time.sleep(1)
print(f" Found {n_found} USB host devices...")

if n_found > 0:

    # TODO: wrap with try in case it doesn't work?
    print("Trying as MIDI device....")
    midi_device = adafruit_midi.MIDI(midi_in=raw_midi_in)
    # print(f"    {midi_device.__dict__=}")

else:
    print("Using built-in MIDI?.....")
    midi = adafruit_midi.MIDI(

        midi_in=usb_midi.ports[0],
        midi_out=None,

        in_channel=MIDI_IN_CHANNEL,
        # in_channel = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),

        # out_channel=(midi_out_channel - 1),
        # out_channel = None

        )
    print("Built-in MIDI OK?")

# Set up MIDI out

def panic(m):
    '''Do we need to do all channels? not really'''
    print("Turning off all MIDI notes")
    for chan in range(16):
        for note in range(128):
            m.send(NoteOff(note, chan))

uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)  # init UART

# No UART input, only output 
midi_out = adafruit_midi.MIDI(
    midi_out = uart,
    out_channel = MIDI_OUT_CHANNEL - 1,
    debug = False,
    )

panic(midi_out)


# midi_in = midi_device._midi_in 
# print(f"MIDI device: {midi_in}")
# display.set_text_1(midi_in)

while True:
    msg = midi_device.receive()
    if msg:
        if isinstance(msg, active_sensing.ActiveSensing):
            pass
        else:
            print(f"  {msg}")
