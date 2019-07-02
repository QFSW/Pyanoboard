import math
from enum import Enum

# Tuple structures
# midi_event = (type, id, velocity)

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


class EventType(Enum):
    NONE = 0
    NOTE = 144
    PEDAL = 176


def get_note_tone(midi_event):
    raw_semitone = midi_event[1]
    offset_semitone = raw_semitone - C1_SEMITONE  # center notes to be around C1
    octave = math.floor(offset_semitone / OCTAVE_SIZE)
    note_index = offset_semitone % OCTAVE_SIZE
    return KEYS[note_index] + str(octave)


def get_note_dynamic(midi_event):
    loudness = midi_event[2]
    if loudness == 0:
        return "OFF"
    else:
        for (value, name) in DYNAMICS:
            if loudness <= value:
                return name
        return "N/A"


def get_note(midi_event):
    tone = get_note_tone(midi_event)
    dynamic = get_note_dynamic(midi_event)
    return tone, dynamic


def get_pedal(midi_event):
    pedal_id = midi_event[1]
    pedal_vel = midi_event[2]

    pedal_name = "NA"
    is_down = False

    for (id_, name) in PEDALS:
        if pedal_id == id_:
            pedal_name = name
            break

    if pedal_vel == 127:
        is_down = True
    return pedal_name, is_down


def get_event_type(midi_event):
    try:
        return EventType(midi_event[0])
    except TypeError:
        return EventType.NONE
