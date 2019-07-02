import pygame, os, midi, KeyHandling, time
import key_handling, keys
from pygame import midi
from pygame.locals import *

os.environ["SDL_VIDEODRIVER"] = "dummy"

MainDir = os.path.split(os.path.abspath(__file__))[0]
pygame.init()
pygame.midi.init()

pygame.display.set_mode((1,1))
Piano = pygame.midi.Input(1)


class Binding:
    def __init__(self, note_name, keyboard_key):
        self.note = note_name
        self.key = keyboard_key
        self.is_pressed = False

    def press(self):
        self.is_pressed = True
        key_input = key_handling.new_keyboard_input(self.key)
        key_handling.send_input(key_input)

    def un_press(self):
        self.is_pressed = False
        key_input = key_handling.new_keyboard_input(self.key, keys.KEYEVENTF_KEYUP)
        key_handling.send_input(key_input)


NoteMaps = [
    Binding("C2", KeyHandling.KEY_S),
    Binding("C#2", KeyHandling.KEY_W),
    Binding("B1", KeyHandling.KEY_A),
    Binding("D2", KeyHandling.KEY_D),
    Binding("C3", KeyHandling.KEY_G),
    Binding("C#3", KeyHandling.KEY_T),
    Binding("B2", KeyHandling.KEY_F),
    Binding("D3", KeyHandling.KEY_H),
    Binding("C4", KeyHandling.KEY_L),
    Binding("C#4", KeyHandling.KEY_O),
    Binding("B3", KeyHandling.KEY_K),
    Binding("D4", KeyHandling.KEY_R),
    Binding("D#4", KeyHandling.KEY_P),
    Binding("F4", KeyHandling.KEY_Z)
]

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
                    
