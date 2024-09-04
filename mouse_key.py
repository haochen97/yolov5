import random
import time
import win32api, win32con, win32gui
import cv2
from screenshot import WindScreenShot
from kernel import match
from ctypes import windll
from ctypes.wintypes import HWND
import string
import time
import sys
import pydirectinput


class Operate:
    PostMessageW = windll.user32.PostMessageW
    MapVirtualKeyW = windll.user32.MapVirtualKeyW
    VkKeyScanA = windll.user32.VkKeyScanA
    WM_KEYDOWN = 0x100
    WM_KEYUP = 0x101
    # https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
    VkCode = {
        "back": 0x08,
        "tab": 0x09,
        "return": 0x0D,
        "shift": 0x10,
        "control": 0x11,
        "menu": 0x12,
        "pause": 0x13,
        "capital": 0x14,
        "escape": 0x1B,
        "space": 0x20,
        "end": 0x23,
        "home": 0x24,
        "left": 0x25,
        "up": 0x26,
        "right": 0x27,
        "down": 0x28,
        "print": 0x2A,
        "snapshot": 0x2C,
        "insert": 0x2D,
        "delete": 0x2E,
        "lwin": 0x5B,
        "rwin": 0x5C,
        "numpad0": 0x60,
        "numpad1": 0x61,
        "numpad2": 0x62,
        "numpad3": 0x63,
        "numpad4": 0x64,
        "numpad5": 0x65,
        "numpad6": 0x66,
        "numpad7": 0x67,
        "numpad8": 0x68,
        "numpad9": 0x69,
        "multiply": 0x6A,
        "add": 0x6B,
        "separator": 0x6C,
        "subtract": 0x6D,
        "decimal": 0x6E,
        "divide": 0x6F,
        "f1": 0x70,
        "f2": 0x71,
        "f3": 0x72,
        "f4": 0x73,
        "f5": 0x74,
        "f6": 0x75,
        "f7": 0x76,
        "f8": 0x77,
        "f9": 0x78,
        "f10": 0x79,
        "f11": 0x7A,
        "f12": 0x7B,
        "numlock": 0x90,
        "scroll": 0x91,
        "lshift": 0xA0,
        "rshift": 0xA1,
        "lcontrol": 0xA2,
        "rcontrol": 0xA3,
        "lmenu": 0xA4,
        "rmenu": 0XA5
    }

    def __init__(self, hwnd):
        self.hwnd = hwnd

    def move(self, pos:tuple):
        x = pos[0]
        y = pos[1]
        wparam = 0
        '''
        wparam:
        MK_CONTROL	如果CTRL键关闭，请设置。
        MK_LBUTTON	设置鼠标左键是否关闭。
        MK_MBUTTON	设置中间的鼠标按钮是否关闭。
        MK_RBUTTON	设置鼠标右键是否关闭。
        MK_SHIFT	设置SHIFT键是否关闭。
        '''
        #将输入坐标放到pos的高低位，低位为x，高位为y
        pos = win32api.MAKELONG(x, y)
        win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, wparam, pos)

    def click(self, pos, flags1 = 0, flags2 = 1):
        '''
        flags1: 0-左键（默认）,1-右键,2-中键
        flags2: 1-单击(默认),2-双击,3-三击,N-N击
        '''
        #将输入坐标放到pos的高低位，低位为x，高位为y
        x = pos[0]
        y = pos[1]
        pos = win32api.MAKELONG(x, y)
        #构建点击次数集
        f2 = range(flags2)

        #判断点击次数
        for x in f2:
            if flags1 == 0:
                win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, pos)
                win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, pos)
            elif flags1 == 1:
                win32gui.SendMessage(self.hwnd, win32con.WM_RBUTTONDOWN, 0, pos)
                win32gui.SendMessage(self.hwnd, win32con.WM_RBUTTONUP, 0, pos)
            else:
                win32gui.SendMessage(self.hwnd, win32con.WM_MBUTTONDOWN, 0, pos)
                win32gui.SendMessage(self.hwnd, win32con.WM_MBUTTONUP, 0, pos)

    def drag(self, pos1: tuple, pos2: tuple, flags1=0):
        '''
        按住鼠标移至目标点
        （x1.y1）起始点，（x2,y2）目标点
        flags1: 0-左键（默认）,1-右键,2-中键
        右键和中键一般用不到
        '''

        #取出输入坐标
        x1 = pos1[0]
        y1 = pos1[1]
        x2 = pos2[0]
        y2 = pos2[1]

        #计算移动距离
        x_len = x2 - x1
        if x_len == 0:
            x2 = x2 + 10
        #计算直线方程
        x = x1
        y = int((x - x1) / (x2 - x1) * (y2 -y1) + y1)
        pos = win32api.MAKELONG(x, y)
        #设置步长
        x_step  = 1

        #操作
        if flags1 == 0:
                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
                if x_len < 0:
                    x_len = -x_len
                    x_step = -1
                for i in range(x_len):
                    print(i)
                    x = x + x_step
                    y = int((x - x1) / (x2 - x1) * (y2 -y1) + y1)
                    pos2 = win32api.MAKELONG(x, y)
                    if i < x_len-1:
                        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, pos2)
                    else:
                        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, pos2)
                # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1, 0)
                # win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, pos)
                # win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, pos)
                # win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
                # win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, pos)

    def drag2(self, pos1: tuple, pos2: tuple):

        '''
        按住鼠标移至目标点
        （x1.y1）起始点，（x2,y2）目标点
        flags1: 0-左键（默认）,1-右键,2-中键
        右键和中键一般用不到
        '''

        # 取出输入坐标
        x1 = pos1[0]
        y1 = pos1[1]
        x2 = pos2[0]
        y2 = pos2[1]
        pos1 = win32api.MAKELONG(x1, y1)
        pos2 = win32api.MAKELONG(x2, y2)

        # .SetForegroundWindow(self.hwnd)
        # time.sleep(random.randint(40, 100) / 1000)
        win32gui.SendMessage(self.hwnd, win32con.WM_NCLBUTTONDOWN, 0, pos1)  # 起始点按住
        # ime.sleep(random.randint(40, 100) / 1000)
        win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, pos2)  # 移动到终点
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, pos2)  # 松开

    def get_virtual_keycode(self, key: str):
        """根据按键名获取虚拟按键码

        Args:
            key (str): 按键名

        Returns:
            int: 虚拟按键码
        """
        if len(key) == 1 and key in string.printable:
            # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
            return self.VkKeyScanA(ord(key)) & 0xff
        else:
            return self.VkCode[key]

    def key_down(self, key: str):
        """按下指定按键

        Args:
            handle (HWND): 窗口句柄
            key (str): 按键名
        """
        vk_code = self.get_virtual_keycode(key)
        scan_code = self.MapVirtualKeyW(vk_code, 0)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
        wparam = vk_code
        lparam = (scan_code << 16) | 1
        # self.PostMessageW(self.hwnd, self.WM_KEYDOWN, wparam, lparam)
        win32gui.PostMessage(self.hwnd, self.WM_KEYDOWN, wparam, lparam)
    def key_up(self, key: str):
        """放开指定按键

        Args:
            handle (HWND): 窗口句柄
            key (str): 按键名
        """
        vk_code = self.get_virtual_keycode(key)
        scan_code = self.MapVirtualKeyW(vk_code, 0)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
        wparam = vk_code
        lparam = (scan_code << 16) | 0XC0000001
        # self.PostMessageW(self.hwnd, self.WM_KEYUP, wparam, lparam)
        win32gui.PostMessage(self.hwnd, self.WM_KEYUP, wparam, lparam)
    def key_press(self, key: str, interval=0.01):
        self.key_down(key)
        # time.sleep(interval)
        self.key_up(key)


if __name__ == '__main__':
    if not windll.shell32.IsUserAnAdmin():
        # 不是管理员就提权
        windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
    wss = WindScreenShot('新缘起墨香二区友情提醒:注意保护账号及装备安全,谨慎交易!(Ctrl+W隐藏/显示游戏)[R复活窗口][E洗恶]', 'pyqt')
    img = wss.run()
    print(wss.hwnd)
    op = Operate(wss.hwnd)
    op.key_press('f6')
    pos = match(img, 'icon_wuping.png')
    print(pos)
    op.click(pos)