import threading
import queue
from os import times
import time

import pyautogui
from kernel import match
from screenshot import WindScreenShot
import win32gui, win32con

class DragKill:

    def __init__(self, hwnd, rect):
        self.hwnd = hwnd
        self.rect = rect

    def run(self, img):
        try:
            mt = match(img, 'duoquwupin.jpg', threshold=0.95, crop=[0, 700, 0, 1600])
        except:
            mt = 0
            print('匹配出错了')
        # mt = match(img, 'duoquwupin.jpg', crop=[0, self.rect[3] - self.rect[1] - 200, 0, self.rect[2] - self.rect[0]])
        if mt == 0:
            pass
        else:
            print(f'找到匹配目标,图中坐标{mt}')
            self.drag(mt)


    def drag(self, pos):
        x = self.rect[0] + pos[0]
        y = self.rect[1] + pos[1] + 25    # 这里的25是pyqt截图时，窗口上标题栏的高度
        print(x, y)
        pyautogui.moveTo(x, y)
        pyautogui.dragTo(x, self.rect[3]-30, duration=0.18)
        pyautogui.moveTo(x, y)

# def shot(q):
#     while True:
#         try:
#             img = wss.run()
#             q.put(img)
#             time.sleep(0.03)
#         except:
#             print('截图太快出错了')
#
#
# def detect(q):
#     while True:
#         try:
#             img = q.get()
#             dk.run(img)
#             time.sleep(0.03)
#         except:
#             print('匹配太快出错了')
#         # img = q.get()
#         # dk.run(img)
#         # time.sleep(0.03)
def shot_detect():
    while True:
        img = wss.run()
        dk.run(img)
        time.sleep(0.03)

if __name__ == "__main__":
    # 初始化
    wss = WindScreenShot('缘起墨香', 'pyqt')
    dk = DragKill(wss.hwnd, wss.rect)

    # # 创建队列
    # q = queue.Queue()

    # 创建线程
    # shot_thread = threading.Thread(target=shot, args=(q,))
    # detect_thread = threading.Thread(target=detect, args=(q,))
    shot_detect_thread = threading.Thread(target=shot_detect)

    # 启动线程
    # shot_thread.start()
    # detect_thread.start()
    shot_detect_thread.start()
