# USBtoDIN
Microcontroller project to adapt a USB-based MIDI controller to a DIN-based MIDI device.

# Purpose
I have a DM6 electronic drum kit that a) has lame sounds built in, and b) has a noisy output.
But I also have nice SR16 and SR18 drum modules that make way better sounds.... but use
DIN MIDI connectors, whereas the DM6 uses USB MIDI, so I can't just hook them together.

Hence this project: Plug the the two devices into this thingamajig, and MIDI notes are 
magically transported from the DM6 to the SR16/18!

# Requirements
* Adafruit Feather RP2040 USB Host
* Adafruit MIDI Featherwing
* Adafruit 128x64 OLED display (but you could use something else)
* Breadboard, a few wires.
* Developed with CircuitPython 11 alpha, so far.


# Things to Do
(See also the GitHub repo, https://github.com/RobCranfill/USBtoDIN/issues)

