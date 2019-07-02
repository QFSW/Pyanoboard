import json
import emulator
import keys


def parse_key(key_str):
    upper_str = key_str.upper()
    upper_concat1 = "KEY_" + upper_str
    upper_concat2 = "VK_" + upper_str

    for attempt in [upper_str, upper_concat1, upper_concat2]:
        result = getattr(keys, attempt, None)
        if result is not None and isinstance(result, int):
            return result

    return int(key_str)


def load(config_path):
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
