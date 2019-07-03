import sys
import emulator
import debug
import config


def main():
    emulator.init_pygame()
    args = sys.argv[1:]

    if "-devices" in args:
        debug.print_device_info()
        sys.exit()

    verbose = "-verbose" in args

    if len(args) < 1:
        print("A config file must be supplied")
        sys.exit(-1)
    config_path = args[-1]

    (device_id, mappings) = config.load(config_path)

    if verbose:
        for binding in mappings:
            print("Loaded binding %s to %s" % (binding.note, binding.key))

    em = emulator.Emulator(device_id, mappings)
    em.verbose = verbose

    em.run()


if __name__ == "__main__":
    main()
