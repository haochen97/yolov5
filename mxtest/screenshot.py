import win32gui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
import win32con
import win32ui
# from PIL import Image
import ctypes
from ctypes import *
import cv2
import numpy as np

class shot():
    def __init__(self, way, windowname):
        self.hwnd = win32gui.FindWindow(None, windowname)
        self.way = way
        self.windowname = windowname

    def run(self):
        if self.way == 'pyqt':
            self.get_img_pyqt()

    def get_img_pyqt(self):
        app = QApplication(sys.argv)
        screen = QApplication.primaryScreen()
        img = screen.grabWindow(self.hwnd).toImage()
        img.save("E:\\Projects\\mxtest\\img\\img0\\img0.jpg")

    def get_img_win(self, WindowName):
        hwnd = win32gui.FindWindow(None, WindowName)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        # 获取窗口图像
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, right - left, bottom - top)

        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (right - left, bottom - top), mfcDC, (0, 0), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        img.save("E:\\Projects\\baoshiqi\\img\\sh.jpg")

    def get_img_dxgi(self, WindowName):
        # 加载dll库
        dxgi = ctypes.CDLL("E:\\Projects\\dxgi4py-master\\dxgi4py.dll")
        dxgi.grab.argtypes = (POINTER(ctypes.c_ubyte), ctypes.c_int, c_int, c_int, c_int)
        dxgi.grab.restype = POINTER(c_ubyte)

        # 获取窗口hwnd
        windowTitle = WindowName
        hwnd = win32gui.FindWindow(None, windowTitle)
        print(hwnd)
        windll.user32.SetProcessDPIAware()

        # 初始化
        dxgi.init_dxgi(hwnd)

        # 指定截图区域(这里示例为截取整个窗口)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        shotLeft, shotTop = 0, 0
        height = bottom - top
        width = right - left
        shotRight, shotBottom = shotLeft + width, shotTop + height
        # 创建numpy array用于接收截图结果
        shot = np.ndarray((height, width, 4), dtype=np.uint8)
        shotPointer = shot.ctypes.data_as(POINTER(c_ubyte))
        # 截图
        buffer = dxgi.grab(shotPointer, shotLeft, shotTop, shotRight, shotBottom)
        # 获取结果
        image = np.fromiter(buffer, dtype=np.uint8, count=height * width * 4).reshape((height, width, 4))
        # 转为BGR形式
        img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        cv2.imshow('sample_pic', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # 不再使用时销毁
        dxgi.destroy()


if __name__ == '__main__':
    pass
    # get_img('DESKTOP-N9CO16J - MoonlightBlocker v1.9 - Author by BlueLife')
    # get_img('FolderView')
    # get_img('Parsec')
    # get_img_win('DESKTOP-N9CO16J - Moonlight')
    # get_img_dxgi('文字文稿4 - WPS Office')
    # get_img_PyQt('新缘起墨香二区友情提醒:注意保护账号及装备安全,谨慎交易!(Ctrl+W隐藏/显示游戏)[R复活窗口][E洗恶]')