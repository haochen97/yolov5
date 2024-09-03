import random
import time
import win32api, win32con, win32gui
import cv2


class operate():
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


if __name__ == '__main__':
    center = [248, 200]
    # click(center)