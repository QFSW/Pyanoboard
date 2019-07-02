import sys
import os
import keys
import emulator
import pygame
import json
from pygame import  midi


def print_device_info():
    for i in range(pygame.midi.get_count()):
        info = pygame.midi.get_device_info(i)
        (interface, name, input_, output, open) = info

        if input_:
            io_status = "input"
        if output:
            io_status = "output"

        print("%2i: %s: %s (%s)" %
              (i, interface, name, io_status))


def parse_key(key_str):
    upper_str = key_str.upper()
    upper_concat1 = "KEY_" + upper_str
    upper_concat2 = "VK_" + upper_str

    for attempt in [upper_str, upper_concat1, upper_concat2]:
        result = getattr(keys, attempt, None)
        if result is not None and isinstance(result, int):
            return result

    return int(key_str)


def load_config(config_path):
    file = open(config_path, "r")
    config = json.load(file)

    device_id = config["device_id"]
    raw_bindings = config["bindings"]

    bindings = []
    for raw_binding in raw_bindings:
        note = raw_binding["note"]
        raw_key = raw_binding["key"]
        key = parse_key(raw_key)
        bindings.append(emulator.Binding(note, key))

    return device_id, bindings


def main():
    emulator.init_pygame()

    args = sys.argv[1:]

    if "-devices" in args:
        print_device_info()
        sys.exit()

    verbose = "-verbose" in args

    if len(args) < 1:
        print("A config file must be supplied")
        sys.exit(-1)
    config_path = args[-1]

    (device_id, mappings) = load_config(config_path)
    em = emulator.Emulator(device_id, mappings)
    em.verbose = verbose

    em.run()


if __name__ == "__main__":
    main()
