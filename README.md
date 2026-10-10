# USBtoDIN
Microcontroller project to adapt a USB-based MIDI controller to a DIN-based MIDI device.

# Purpose
I have a DM6 electronic drum kit that a) has lame sounds built in, and b) has a noisy output.
But I also have nice SR16 and SR18 drum modules that make way better sounds.... but use
DIN MIDI connectors, whereas the DM6 uses USB MIDI, so I can't just hook them together.

Hence this project: Plug the the two devices into this thingamajig, and MIDI notes are 
magically transported from the DM6 to the SR16/18!

As of early October, I finally have this project actually working! The proof-of-concept
show here works fine. I need to figure out exactly how I want to house this device,
and what, if any, user interface it will have.


# Requirements
* Adafruit Feather RP2040 USB Host
* Adafruit MIDI Featherwing
* Display of some sort:
  * Adafruit 16-segment LED, or
  * Adafruit 128x64 OLED display
* Breadboard or Adafruit "doubler"?
* Developed with CircuitPython 11 alpha, so far.


# Things to Do
(See also the GitHub repo, https://github.com/RobCranfill/USBtoDIN/issues)
* Error handling: what to wrap, where, so as to keep going forever?
* MIDI questions:
  * Should I send NoteOff messages? Or NoteOn(velocity=0)? Or neither?
    * Currently passing *all* MIDI messages, which seems to work find and makes the most sense.
* What user interface? It kinda doesn't need one at all, if everything works as intended.
  * I *really* don't like using an OLED for the display: it suffers from burn-in, and for
a device like this that may just stay on indefinitly, that ain't good.
* (maybe?) If no Host MIDI, fail over to the built-in USB MIDI (what do you call that? The one that comes in on the power cable.)
  * This would be mainly just for testing; useful otherwise?

# Notes
## MIDI mapping
This isn't really pertinent to this task, I'm just trying to figure out 
what I did to the SR18.

 | DM6 pad   | sends MIDI note | SR18 pad |
 |-----------|-----  |-----|
 | Kick      | 36  | 1: Kick
 | Snare     | 38  | 2: Snare1
 | Rimshot   | 40  | 3: Snare2
 | Tom 1     | 48  | 7: Tom1
 | Tom 2     | 45  | 8: Tom2
 | Tom 3     | 43  | 9: Tom3
 | HH        | 46  | 4: HH?
 | Crash     | 49  | 10: Crash
 | Ride      | 51  | 11: Ride
 | Hat ctl   | 44  ? preceeded by CC 4? |


Currently, mapping works for snare, rimshot, t1, t2, t3, crash, ride, kick

Not sure how to handle High Hat closed or open

*** Fix in SR18: System Setup Page 4 - Note Map

