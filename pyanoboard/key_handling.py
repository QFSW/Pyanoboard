import ctypes

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2


class MouseInput(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

    def __init__(self, x, y, flags, data):
        super(MouseInput, self).__init__(x, y, data, flags, 0, None)


class KeyboardInput(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

    def __init__(self, code, flags):
        super(KeyboardInput, self).__init__(code, code, flags, 0, None)


class HardwareInput(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))

    def __init__(self, message, parameter):
        super(HardwareInput, self).__init__(message & 0xFFFFFFFF, parameter & 0xFFFF, parameter >> 16 & 0xFFFF)


class _InputUnion(ctypes.Union):
    _fields_ = (('mi', MouseInput),
                ('ki', KeyboardInput),
                ('hi', HardwareInput))


class Input(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _InputUnion))

    def __init__(self, structure):
        if isinstance(structure, MouseInput):
            super(Input, self).__init__(INPUT_MOUSE, _InputUnion(mi=structure))
        elif isinstance(structure, KeyboardInput):
            super(Input, self).__init__(INPUT_KEYBOARD, _InputUnion(ki=structure))
        elif isinstance(structure, HardwareInput):
            super(Input, self).__init__(INPUT_HARDWARE, _InputUnion(hi=structure))
        else:
            raise TypeError('Cannot create Input structure!')


def send_input(*inputs):
    n_inputs = len(inputs)
    lp_input = Input * n_inputs
    p_inputs = lp_input(*inputs)
    cb_size = ctypes.c_int(ctypes.sizeof(Input))
    return ctypes.windll.user32.SendInput(n_inputs, p_inputs, cb_size)


def new_mouse_input(flags, x=0, y=0, data=0):
    return Input(MouseInput(flags, x, y, data))


def new_key_input(code, flags=0):
    return Input(KeyboardInput(code, flags))


def new_hardware_input(message, parameter=0):
    return Input(HardwareInput(message, parameter))
