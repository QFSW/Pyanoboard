import pygame, os, math, sys
from pygame import midi
from pygame.locals import *

class MIDI:
    Keys = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    Dynamics = [[16,"ppp"],[33,"pp"],[49,"p"],[64,"mp"],[80,"mf"],[96,"f"],[112,"ff"],[127,"fff"]]
    Pedals = [[64, "Sustain"]]
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

    def ReturnNote(MIDIEvent):
        NoteNum = MIDIEvent[1] - 24
        Octave = math.floor(NoteNum/12)
        NoteNum-=12*Octave
        return str(MIDI.Keys[NoteNum])+str(Octave)

    def ReturnNoteDynamic(MIDIEvent):
        NoteLoudness = MIDIEvent[2]
        DynamicName=""
        if NoteLoudness == 0:
            DynamicName="OFF"
        else:
            for Dynamic in MIDI.Dynamics:
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
        for Pedal in MIDI.Pedals:
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
            
