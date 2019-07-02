import pygame, os, math, sys
from pygame import midi
from pygame.locals import *

OCTAVE_SIZE = 12
KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
DYNAMICS = [
    [16, "ppp"],
    [33, "pp"],
    [49, "p"],
    [64, "mp"],
    [80, "mf"],
    [96, "f"],
    [112, "ff"],
    [127, "fff"]
]
PEDALS = [
    [64, "Sustain"]
]


def PrintDeviceInfo():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))


def get_note_tone(MIDIEvent):
    note_num = MIDIEvent[1] - 24
    octave = math.floor(note_num / OCTAVE_SIZE)
    note_num %= OCTAVE_SIZE
    return KEYS[note_num] + str(octave)


def get_note_dynamic(MIDIEvent):
    loudness = MIDIEvent[2]
    dynamic_name = ""
    if loudness == 0:
        dynamic_name = "OFF"
    else:
        for dynamic in DYNAMICS:
            if loudness <= dynamic[0]:
                dynamic_name = dynamic[1]
                break

    return dynamic_name


def PrintNote(MIDIEvent):
    if MIDIEvent[2]!=0:
        String = get_note_tone(MIDIEvent)
        String+=str(" (")+get_note_dynamic(MIDIEvent)+")"
        print(String)


def ReturnPedal(MIDIEvent):
    PedalID = MIDIEvent[1]
    PedalVelocity = MIDIEvent[2]
    PedalName="NA"
    isDown = False
    for Pedal in PEDALS:
        if PedalID == Pedal[0]:
            PedalName = Pedal[1]
            break
    if PedalVelocity == 127: isDown = True
    return [PedalName, isDown]


def PrintPedal(MIDIEvent):
    PedalData = ReturnPedal(MIDIEvent)
    String = PedalData[0]
    if PedalData[1]: String+=" Down"
    else: String+=" Up"
    print(String)


def PrintEvent(MIDIEvent):
    if MIDIEvent[0] == 144:
        PrintNote(MIDIEvent)
    elif MIDIEvent[0] == 176:
        PrintPedal(MIDIEvent)
