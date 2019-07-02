import pygame
import os
import midi
import key_handling
import key_events
from pygame import midi as pygame_midi


class Binding:
    def __init__(self, note_name, keyboard_key):
        self.note = note_name
        self.key = keyboard_key
        self.is_pressed = False

    def press(self):
        self.is_pressed = True
        key_input = key_handling.new_key_input(self.key)
        key_handling.send_input(key_input)

    def release(self):
        self.is_pressed = False
        key_input = key_handling.new_key_input(self.key, key_events.KEYEVENTF_KEYUP)
        key_handling.send_input(key_input)


class Emulator:
    def __init__(self, midi_device_id, bindings):
        self.midi_device_id = midi_device_id
        self.midi_device = pygame.midi.Input(midi_device_id)
        self.bindings = bindings
        self.verbose = False

    def release_all(self):
        for binding in self.bindings:
            binding.un_press()

    def run(self):
        while True:
            if self.midi_device.poll():
                midi_events = self.midi_device.read(10)
                for (midi_event, timestamp) in midi_events:
                    event_type = midi.get_event_type(midi_event)
                    if event_type == midi.EventType.PEDAL:
                        self.handle_pedal(midi_event)
                    elif event_type == midi.EventType.NOTE:
                        self.handle_note(midi_event)

    def handle_pedal(self, midi_event):
        (pedal, is_pressed) = midi.get_pedal(midi_event)
        if is_pressed:
            self.release_all()

    def handle_note(self, midi_event):
        (note, dynamic) = midi.get_note(midi_event)
        for binding in self.bindings:
            if binding.note == note:
                if dynamic == "OFF":
                    binding.release()
                else:
                    binding.press()


def init_pygame():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.midi.init()

