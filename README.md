# Pyanoboard
_Pyanoboard_ is a simple piano to keyboard emulator. It allows you to use any MIDI enabled device as a virtual keyboard.

_Pyanoboard_ actually simulates key events rather than sending characters to be typed, which means you can use it for anything such as gaming and not just typing.

## Installation

Either

1. Clone this repository, and use `pyanoboard.py` from the `pyanoboard` directory
   - You must have `pygame` installed
2. Install the package via pip `pip install pyanoboard`

###  Prerequisites

- MIDI enabled device such as a digital piano
- MIDI to USB cable
- `python` 
- Windows

## Usage

To use this package, enter

```bash
python -m pyanoboard config
```

Where config is the path to your configuration file using the JSON format. An example configuration file has been included under `example/config.json`

_example config_

```json
{
    "device_id": 1,
    "bindings": [
        {
            "note": "C3",
            "key": "h"
        }
    ]
}
```

_pyanoboard_ can also take the following arguments

| Argument | Meaning                                                      |
| -------- | ------------------------------------------------------------ |
| -verbose | Enables verbose logging                                      |
| -devices | Shows a list of the connected MIDI devices instead of starting pyanoboard |

In order to find the `device_id` of your device, use the `-devices` argument

```bash
python -m pyanoboard -devices
```

