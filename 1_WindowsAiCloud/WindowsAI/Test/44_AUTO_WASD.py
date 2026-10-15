import ctypes
import time

# 定义常量和数据结构
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput)
    ]


class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]


# 定义常量
INPUT_KEYBOARD = 1
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
VK_W = 0x57
VK_A = 0x41
VK_S = 0x53
VK_D = 0x44

# 函数声明
SendInput = ctypes.windll.user32.SendInput
SendInput.argtypes = [ctypes.c_uint, ctypes.POINTER(Input), ctypes.c_int]
SendInput.restype = ctypes.c_uint


# 辅助函数：模拟按键事件
def press_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0x48, KEYEVENTF_KEYDOWN, 0, ctypes.pointer(extra))
    x = Input(INPUT_KEYBOARD, ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0x48, KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
    x = Input(INPUT_KEYBOARD, ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

time.sleep(2)
# 示例使用：按下WASD键一段时间，然后释放
press_key(VK_W)
# press_key(VK_A)
# press_key(VK_S)
# press_key(VK_D)

time.sleep(1)  # 模拟按下一段时间

release_key(VK_W)
# release_key(VK_A)
# release_key(VK_S)
# release_key(VK_D)
