import pygame
import os
import midi
import key_handling
import keys
from pygame import midi as pygame_midi
from pygame.locals import *


def init_pygame():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.midi.init()


class Binding:
    def __init__(self, note_name, keyboard_key):
        self.note = note_name
        self.key = keyboard_key
        self.is_pressed = False

    def press(self):
        print(self.key)
        self.is_pressed = True
        key_input = key_handling.new_key_input(self.key)
        key_handling.send_input(key_input)

    def unpress(self):
        self.is_pressed = False
        key_input = key_handling.new_key_input(self.key, keys.KEYEVENTF_KEYUP)
        key_handling.send_input(key_input)


class Emulator:
    def __init__(self, midi_device_id, bindings):
        self.midi_device_id = midi_device_id
        self.midi_device = pygame.midi.Input(midi_device_id)
        self.bindings = bindings

    def unpress_all(self):
        for binding in self.bindings:
            binding.un_press()

    def run(self):
        while True:
            if self.midi_device.poll():
                MIDIEvents = self.midi_device.read(10)
                if MIDIEvents[0][0][1] != 0:
                    for (event, timestamp) in MIDIEvents:
                        event_type = midi.get_event_type(event)
                        if event_type == midi.EventType.PEDAL:
                            if MIDI.MIDI.ReturnPedal(Event[0])[1] == True:
                                for Key in NoteMaps:
                                    Key.UnPress()
                        elif event_type == midi.EventType.NOTE:
                            (note, dynamic) = midi.get_note(event)
                            for binding in self.bindings:
                                if binding.note == note:
                                    if dynamic == "OFF":
                                        binding.unpress()
                                    else:
                                        binding.press()


KeyMaps = [
    Binding("C2", keys.KEY_S),
    Binding("C#2", keys.KEY_W),
    Binding("B1", keys.KEY_A),
    Binding("D2", keys.KEY_D),
    Binding("C3", keys.KEY_G),
    Binding("C#3", keys.KEY_T),
    Binding("B2", keys.KEY_F),
    Binding("D3", keys.KEY_H),
    Binding("C4", keys.KEY_L),
    Binding("C#4", keys.KEY_O),
    Binding("B3", keys.KEY_K),
    Binding("D4", keys.KEY_R),
    Binding("D#4", keys.KEY_P),
    Binding("F4", keys.KEY_Z)
]

init_pygame()
emulator = Emulator(1, KeyMaps)
emulator.run()

