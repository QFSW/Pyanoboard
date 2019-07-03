import pygame
from pygame import midi


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