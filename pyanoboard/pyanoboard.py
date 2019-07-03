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

    config_path = None
    for i in range(len(args)):
        if not args[i][0] == '-':
            config_path = args[i]
            break

    if config_path is None:
        print("A config file must be supplied")
        sys.exit(-1)

    if verbose:
        print("Loading config file %s..." % config_path)

    (device_id, mappings) = config.load(config_path)

    if verbose:
        for binding in mappings:
            print("Loaded binding %s to %s" % (binding.note, binding.key))

    em = emulator.Emulator(device_id, mappings)
    em.verbose = verbose

    if verbose:
        print("Running emulator\n")

    em.run()


if __name__ == "__main__":
    main()
