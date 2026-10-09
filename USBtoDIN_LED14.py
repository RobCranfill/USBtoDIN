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

# my code
# import fw128x64OLED
import LED14


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


def show_error_and_spin(led14display, error_msg):
    pass


# ----------------- start
print(f"\nrunning {__name__}")

display = LED14.display("")
display.marquee_once("USB to DIN - LED version    ")


# Create UART first
#
uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)
print("UART OK")
display.print_then_erase("U OK")


# Find MIDI device. This just assumes the first one found is appropriate.
#
print("looking for USB MIDI device...")

t = time.monotonic()
display.marquee_once("looking for USB MIDI in....    ")
print(f" toook {time.monotonic() - t} seconds")

print("Scanning USB bus...")
time.sleep(1)
midi_interfaces = None
for device in usb.core.find(find_all=True):
    try:
        print(f" * Found device {hex(device.idVendor)}:{hex(device.idProduct)}")
        host_midi_in = adafruit_usb_host_midi.MIDI(device, timeout=0.1)
        print("Trying as MIDI device....")
        try:
            midi_interfaces = adafruit_midi.MIDI(
                    midi_in=host_midi_in,
                    midi_out=uart,
                    in_channel=MIDI_ALL_CHANNELS,
                    out_channel = MIDI_OUT_CHANNEL-1
                    )
            print("  OK!")
        except Exception as e:
            print(f"Not a MIDI device??? {e}")
        break
    except Exception as e:
        print(f" EXCEPTION {e}")
        continue

test_fail = False
if (midi_interfaces is None) or test_fail:
    print("CAN'T SET UP???")
    display.show_error_and_spin("Can't find MIDI out.    ")

print("OK!")
display.print_then_erase("M OK")


# TODO: how? would this take place of 'panic'?
# midi_interfaces.send(Reset(MIDI_OUT_CHANNEL-1))

# panic(midi_interfaces)

# Play startup sound!
for n in [48, 48, 49]:
    midi_interfaces.send(NoteOn(n, 10))
    time.sleep(.15)
print("ta DUM!")


print("Ready!")

# Is this all we do?
# Should we re-map anything? Filter anything?
#
msg_count = 0

while True:
    msg = midi_interfaces.receive()
    if msg:

        if isinstance(msg, ActiveSensing):
            continue

        if isinstance(msg, MIDIBadEvent):
            # print("bad?!")
            print(f" ** BAD {msg}")
            continue

        if isinstance(msg, NoteOn):
            if msg.velocity > 0:
                msg_count += 1
                if msg_count > 9999:
                    msg_count = 0
                display.print("%4d" % msg_count)

        print(f"Got {msg}")

        # print(f"    sending {msg} to DIN...")
        midi_interfaces.send(msg)
