import pygame, os, math, sys
from pygame import midi
from pygame.locals import *

class MIDI:
    OCTAVE_SIZE = 12
    KEYS = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    DYNAMICS = [[16,"ppp"],[33,"pp"],[49,"p"],[64,"mp"],[80,"mf"],[96,"f"],[112,"ff"],[127,"fff"]]
    PEDALS = [[64, "Sustain"]]

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

    def GetNoteTone(MIDIEvent):
        note_num = MIDIEvent[1] - 24
        octave = math.floor(note_num / OCTAVE_SIZE)
        note_num %= OCTAVE_SIZE
        return MIDI.KEYS[note_num] + str(octave)

    def ReturnNoteDynamic(MIDIEvent):
        NoteLoudness = MIDIEvent[2]
        DynamicName=""
        if NoteLoudness == 0:
            DynamicName="OFF"
        else:
            for Dynamic in MIDI.DYNAMICS:
                if NoteLoudness <= Dynamic[0]:
                    DynamicName = Dynamic[1]
                    break
                
        return DynamicName
    
    def PrintNote(MIDIEvent):
        if MIDIEvent[2]!=0:
            String = MIDI.ReturnNote(MIDIEvent)
            String+=str(" (")+MIDI.ReturnNoteDynamic(MIDIEvent)+")"
            print(String)

    def ReturnPedal(MIDIEvent):
        PedalID = MIDIEvent[1]
        PedalVelocity = MIDIEvent[2]
        PedalName="NA"
        isDown = False
        for Pedal in MIDI.PEDALS:
            if PedalID == Pedal[0]:
                PedalName = Pedal[1]
                break
        if PedalVelocity == 127: isDown = True
        return [PedalName, isDown]

    def PrintPedal(MIDIEvent):
        PedalData = MIDI.ReturnPedal(MIDIEvent)
        String = PedalData[0]
        if PedalData[1]: String+=" Down"
        else: String+=" Up"
        print(String)
    
    def PrintEvent(MIDIEvent):
        if MIDIEvent[0] == 144:
            MIDI.PrintNote(MIDIEvent)
        elif MIDIEvent[0] == 176:
            MIDI.PrintPedal(MIDIEvent)
            
