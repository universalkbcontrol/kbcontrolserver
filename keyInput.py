import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

hexKeyMapping = {'esc': 0x01, '1': 0x02, '2': 0x03, '3': 0x04, '4': 0x05, '5': 0x06, '6': 0x07, 
                '7': 0x08, '8': 0x09, '9': 0x0A, '0': 0x0B, '-': 0x0C, '=': 0x0D, 'Back': 0x0E, 
                'Tab': 0x0F, 'Q': 0x10, 'W': 0x11, 'E': 0x12, 'R': 0x13, 'T': 0x14, 'Y': 0x15, 
                'U': 0x16, 'I': 0x17, 'O': 0x18, 'P': 0x19, '[': 0x1A, ']': 0x1B, 'Enter': 0x1C, 
                'LCtrl': 0x1D, 'A': 0x1E, 'S': 0x1F, 'D': 0x20, 'F': 0x21, 'G': 0x22, 'H': 0x23, 
                'J': 0x24, 'K': 0x25, 'L': 0x26, ';': 0x27, "'": 0x28, '`': 0x29, 'LShift': 0x2A, 
                "\\": 0x2B, 'Z': 0x2C, 'X': 0x2D, 'C': 0x2E, 'V': 0x2F, 'B': 0x30, 'N': 0x31, 'M': 0x32, ',': 0x33, 
                '.': 0x34, '/': 0x35, 'RShift': 0x36, 'Num*': 0x37, 'LAlt': 0x38, 'Space': 0x39, 'Caps': 0x3A, 
                'F1': 0x3B, 'F2': 0x3C, 'F3': 0x3D, 'F4': 0x3E, 'F5': 0x3F, 'F6': 0x40, 'F7': 0x41, 
                'F8': 0x42, 'F9': 0x43, 'F10': 0x44, 'NumLock': 0x45, 'Scroll': 0x46, 'Num7': 0x47, 'Num8': 0x48, 
                'Num9': 0x49, 'Num-': 0x4A, 'Num4': 0x4B, 'Num5': 0x4C, 'Num6': 0x4D, 'Num+': 0x4E, 
                'Num1': 0x4F, 'Num2': 0x50, 'Num3': 0x51, 'Num0': 0x52, 'Num.': 0x53, 'F11': 0x57, 'F12': 0x58, 
                'F13': 0x64, 'F14': 0x65, 'F15': 0x66, 'Kana': 0x70, 'Convert': 0x79, 'No Convert': 0x7B, 'Yen': 0x7D, 
                'Num=': 0x8D, '^': 0x90, '@': 0x91, ':': 0x92, '_': 0x93, 'Kanji': 0x94, 'Stop': 0x95, 
                'Ax': 0x96, 'Unlabel': 0x97, 'NumEnter': 0x9C, 'RCtrl': 0x9D, 'Num,': 0xB3, 'Num/': 0xB5, 
                'Sys RQ': 0xB7, 'RAlt': 0xB8, 'Pause': 0xC5, 'Home': 0xC7, 'Up': 0xC8, 'Page Up': 0xC9, 'Left': 0xCB, 'Right': 0xCD, 
                'End': 0xCF, 'Down': 0xD0, 'Page Down': 0xD1, 'Insert': 0xD2, 'Del': 0xD3, 'LWin': 0xDB, 'RWin': 0xDC, 'Apps': 0xDD, 
                'Power': 0xDE, 'Sleep': 0xDF}

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def keyOperation(command):
    
    if type(command) == list:

        holder = hexKeyMapping[command[0]]
        key = hexKeyMapping[command[1]]

        PressKey(holder) 
        PressKey(key)
        time.sleep(0.1)
        ReleaseKey(key) 
        ReleaseKey(holder) 
    
    elif type(command) == str:

        key = hexKeyMapping[command]

        PressKey(key)
        time.sleep(0.1)
        ReleaseKey(key) 