import pyautogui
from kernel import match
from screenshot import WindScreenShot
import win32gui, win32con

class DragKill():

    def __init__(self, hwnd):
        self.hwnd = hwnd

    def run(self, img):
        try:
            mt = match('zidongshoulie.png')
        except:
            print('匹配出错了')

        if mt == 0:
            print('未找到目标')
        else:
            print(mt)
            self.show_window()


    def drag(self):
        pass

    def show_window(self):
        # 判断窗口是否置顶
        flag = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
        print(flag)
        if flag == 256:
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        else:
            print('窗口已置顶')


if __name__ == "__main__":
    wss = WindScreenShot('缘起墨香', 'pyqt')
    img = wss.run()
    dk = DragKill(wss.hwnd)
    dk.run(img)