import pygame, os, midi, KeyHandling, time
import key_handling, keys
from pygame import midi
from pygame.locals import *

os.environ["SDL_VIDEODRIVER"] = "dummy"

MainDir = os.path.split(os.path.abspath(__file__))[0]
pygame.init()
pygame.midi.init()

MIDI.MIDI.PrintDeviceInfo()
pygame.display.set_mode((1,1))
Piano = pygame.midi.Input(1)

class NoteMap:
    def __init__(self, Note, Key):
        self.Note = Note
        self.Key = Key
        self.IsPlaying = False
        print(self.Note, self.Key)
    def Press(self):
        if not self.IsPlaying:
            KeyHandling.SendInput(KeyHandling.Keyboard(self.Key))
            self.IsPlaying = True
    def UnPress(self):
        KeyHandling.SendInput(KeyHandling.Keyboard(self.Key, KeyHandling.KEYEVENTF_KEYUP))
        self.IsPlaying = False
NoteMaps =(
[
    NoteMap("C2", KeyHandling.KEY_S),
    NoteMap("C#2", KeyHandling.KEY_W),
    NoteMap("B1", KeyHandling.KEY_A),
    NoteMap("D2", KeyHandling.KEY_D),
    NoteMap("C3", KeyHandling.KEY_G),
    NoteMap("C#3", KeyHandling.KEY_T),
    NoteMap("B2", KeyHandling.KEY_F),
    NoteMap("D3", KeyHandling.KEY_H),
    NoteMap("C4", KeyHandling.KEY_L),
    NoteMap("C#4", KeyHandling.KEY_O),
    NoteMap("B3", KeyHandling.KEY_K),
    NoteMap("D4", KeyHandling.KEY_R),
    NoteMap("D#4", KeyHandling.KEY_P),
    NoteMap("F4", KeyHandling.KEY_Z)
    ])

while True:
    if Piano.poll():
        MIDIEvents = Piano.read(10)
        if MIDIEvents[0][0][1]!=0:
            for Event in MIDIEvents:
                if Event[0][0] == 176:
                    if MIDI.MIDI.ReturnPedal(Event[0])[1] == True:
                        for Key in NoteMaps:
                            Key.UnPress()
                elif Event[0][0] == 144:
                    Note = MIDI.MIDI.ReturnNote(Event[0])
                    for Key in NoteMaps:
                        if Key.Note == Note:
                            if (MIDI.MIDI.ReturnNoteDynamic(Event[0]) == "OFF"):
                                Key.UnPress()
                            else:
                                Key.Press()
                    
