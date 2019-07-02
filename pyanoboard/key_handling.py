import ctypes

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))

class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))

class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))

def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARD = 2

def Input(structure):
    if isinstance(structure, MOUSEINPUT):
        return INPUT(INPUT_MOUSE, _INPUTunion(mi=structure))
    if isinstance(structure, KEYBDINPUT):
        return INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure))
    if isinstance(structure, HARDWAREINPUT):
        return INPUT(INPUT_HARDWARE, _INPUTunion(hi=structure))
    raise TypeError('Cannot create INPUT structure!')

WHEEL_DELTA = 120
XBUTTON1 = 0x0001
XBUTTON2 = 0x0002
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_HWHEEL = 0x01000
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_VIRTUALDESK = 0x4000
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100

def MouseInput(flags, x, y, data):
    return MOUSEINPUT(x, y, data, flags, 0, None)


KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

def KeybdInput(code, flags):
    return KEYBDINPUT(code, code, flags, 0, None)

def HardwareInput(message, parameter):
    return HARDWAREINPUT(message & 0xFFFFFFFF,
                         parameter & 0xFFFF,
                         parameter >> 16 & 0xFFFF)

def Mouse(flags, x=0, y=0, data=0):
    return Input(MouseInput(flags, x, y, data))

def Keyboard(code, flags=0):
    return Input(KeybdInput(code, flags))

def Hardware(message, parameter=0):
    return Input(HardwareInput(message, parameter))