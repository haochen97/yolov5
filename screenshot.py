import time

import dxcam
import numpy as np
from PyQt5.QtWidgets import QApplication
import win32gui
import sys
import cv2

class WindScreenShot:
    """
    获取指定窗口图像，实例化时需要传入窗口标题
    """

    def __init__(self, windowname, way) -> None:
        self.img = None
        self.way = way
        self.hwnd = self.find_fuzzy_top_window_hwnd(windowname)[0][1]
        self.rect = self.get_window_rect()
        self.app = QApplication(sys.argv)
        print(self.rect)
        if way == 'dxcam':
            self.camera = dxcam.create()

    def run(self):
        if self.way == 'pyqt':
            self.rect = self.get_window_rect()
            img = self.get_img_pyqt()
            return img
        if self.way == 'dxcam':
            self.rect = self.get_window_rect()
            img = self.get_img_dxcam()
            return img

    def show_window_attr(self, hwnd):
        """
        显示窗口的属性
        :param hwnd: 窗口句柄（十进制）
        :return: 所有的属性
        WindowName: 窗口标题
        ClassName: 窗口类名
        HwndPy: 窗口句柄（十进制）
        HwndSpy: 窗口句柄（十六进制）
        """
        if not hwnd:
            return
        window_name = win32gui.GetWindowText(hwnd)
        # class_name = win32gui.GetClassName(hwnd)
        # hwnd_py = hwnd
        # hwnd_spy = hex(hwnd)
        return (window_name, hwnd)

    def show_top_windows(self):
        hwnd_list = []
        win32gui.EnumWindows(
            lambda hwnd, param: param.append(self.show_window_attr(hwnd)), hwnd_list
        )
        return hwnd_list

    def find_fuzzy_top_window_hwnd(self, windowname):
        """
        根据标题模糊查找全部符合条件的主窗体
        :param FuzzyWindowName: 窗口标题部分文字
        :return:
        """

        all_windows = self.show_top_windows()
        result = []
        for window in all_windows:
            if windowname in window[0]:
                result.append(window)
        return result

    def get_window_rect(self):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        return left, top, right, bottom

    def convert_format_2mat(self, img):
        """
        Converts a QImage into an opencv MAT format
        """
        # Format_RGB32 = 4,存入格式为B,G,R,A 对应 0,1,2,3
        # RGB32图像每个像素用32比特位表示，占4个字节，
        # R，G，B分量分别用8个bit表示，存储顺序为B，G，R，最后8个字节保留
        img = img.convertToFormat(4)
        width = img.width()
        height = img.height()

        ptr = img.bits()
        ptr.setsize(img.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
        # arr为BGRA，4通道图片
        return arr

    def get_img_dxcam(self) :
        # 根据句柄截图
        img = self.camera.grab(self.rect)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        cv2.imwrite('images/window.jpg', img)
        # self.img = img
        return img

    def get_img_pyqt(self):
        # app = QApplication(sys.argv)
        screen = QApplication.primaryScreen()
        img = screen.grabWindow(self.hwnd).toImage()
        img = self.convert_format_2mat(img)
        cv2.imwrite('images/window.jpg', img)
        # img.save('images/window.jpg')
        # self.img = img
        return img


if __name__ == "__main__":
    wss = WindScreenShot('缘起墨香', 'pyqt')
    while True:
       wss.run()
       time.sleep(0.1)

