import dxcam
import cv2
import sys
import numpy as np
import time
import win32api, win32con, win32gui
from pkg_resources import non_empty_lines


class WindScreenShot:
    """
    获取指定窗口图像，实例化时需要传入窗口标题
    """
    app = None
    ori_img = None
    hwnd = None

    def __init__(self, fuzzy_window_name) -> None:
        self.img = None
        self.fuzzy_window_name = fuzzy_window_name
        self.fuzzy_window_attr = self.find_fuzzy_top_window()
        self.fuzzy_window_rect = self.get_window_rect()
        # print(self.fuzzy_window_rect)
        # self.screen_shot()

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

    def find_fuzzy_top_window(self):
        """
        根据标题模糊查找全部符合条件的主窗体
        :param FuzzyWindowName: 窗口标题部分文字
        :return:
        """

        all_windows = self.show_top_windows()
        result = []
        for window in all_windows:
            if self.fuzzy_window_name in window[0]:
                result.append(window)
        return result

    def get_window_rect(self):
        left, top, right, bottom = win32gui.GetWindowRect(self.fuzzy_window_attr[0][1])
        return (left, top, right, bottom)

    def run(self) :
        # 根据句柄截图
        camera = dxcam.create()
        img = camera.grab(self.fuzzy_window_rect)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        cv2.imwrite('E:\\yolov5\\images\\window.jpg', img)
        self.img = img
        return img


if __name__ == "__main__":
    window = WindScreenShot('缘起墨香')
    print(window.fuzzy_window_attr)
    print(window.fuzzy_window_rect)
