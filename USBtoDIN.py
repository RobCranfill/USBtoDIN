# open MIDI device, show messages received.
# works on all MIDI devices except DM6

import time
import usb.core
import busio

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

raw_midi = None
ticks = 0
while raw_midi is None:
    print("scanning USB bus...")
    ticks += 1
    if ticks < 10:
        spin(display)
    else:
        display.blank_screen()

    time.sleep(.5)
    n_found = 0
    for device in usb.core.find(find_all=True):
        n_found += 1
        try:
            raw_midi = adafruit_usb_host_midi.MIDI(device, timeout=0.1)
            print(f"Found device {hex(device.idVendor)}:{hex(device.idProduct)}")
        except Exception as e:
            print(f" EXCEPTION {e}")
            continue
        if raw_midi is None:
            time.sleep(1)
    print(f" Found {n_found} USB devices...")

# Set up MIDI out

def panic(m):
    '''Do we need to do all channels? not really'''
    print("Turning off all MIDI notes")
    for chan in range(16):
        for note in range(128):
            m.send(NoteOff(note, chan))

uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)  # init UART

# No UART input, only output 
midi = adafruit_midi.MIDI(
    midi_out=uart,
    out_channel=(midi_out_cMIDI_OUT_CHANNELhannel - 1),
    debug=False,
    )

panic(midi)

# TODO: wrap with try in case it doesn't work?
print("Trying as MIDI device....")
midi_device = adafruit_midi.MIDI(midi_in=raw_midi)
# print(f"    {midi_device.__dict__=}")

m_in = midi_device._midi_in 
print(f"MIDI device: {m_in}")
display.set_text_1(m_in)

while True:
    msg = midi_device.receive()
    if msg:
        if isinstance(msg, ActiveSensing):
            pass
        else:
            print(f"  {msg}")
