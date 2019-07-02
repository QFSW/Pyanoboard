import pygame, os, math, sys
from pygame import midi
from pygame.locals import *

OCTAVE_SIZE = 12
C1_SEMITONE = 2 * OCTAVE_SIZE
KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
DYNAMICS = [
    (16, "ppp"),
    (33, "pp"),
    (49, "p"),
    (64, "mp"),
    (80, "mf"),
    (96, "f"),
    (112, "ff"),
    (127, "fff")
]
PEDALS = [
    (64, "Sustain")
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


def get_note_tone(note_event):
    raw_semitone = note_event[1]
    offset_semitone = raw_semitone - C1_SEMITONE  # center notes to be around C1
    octave = math.floor(offset_semitone / OCTAVE_SIZE)
    note_index = offset_semitone % OCTAVE_SIZE
    return KEYS[note_index] + str(octave)


def get_note_dynamic(note_event):
    loudness = note_event[2]
    if loudness == 0:
        return "OFF"
    else:
        for (value, name) in DYNAMICS:
            if loudness <= value:
                return name
        return "N/A"


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
