import time
import sys
import win32api, win32con, win32gui

from screenshot import WindScreenShot
# from yolodetect import mydetect
import cv2
import threading
# from yolodetect.mydetect import detect
from pynput.keyboard import Listener, Key
from combine import DragKill
from kernel import match
import pydirectinput
import combine
from mouse_key import Operate
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QHBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem

# def start():
#     """
#     开始截图并侦测
#     """
#     while True:
#         try:
#             fps = 30
#             img = wss.run()    # 截图
#             dk.run(img)    # 自动拖击杀窗口
#             # dt.run(img0)
#             time.sleep(1/fps)
#         except:
#             print('出错了')
#
#
# def on_press(key):
#     # 当按下esc，结束监听
#     if key == Key.esc:
#         print(f"你按下了esc，监听结束")
#         return False
#     elif key == Key.f7:
#         pydirectinput.press('f6')
#         time.sleep(0.2)
#         for _ in range(5):
#             pos = match(wss.img, 'huoquzuobiao.jpg', threshold=0.95)
#             if pos == 0:
#                 pass
#             else:
#                 op.click(pos)
#                 time.sleep(0.2)
#                 break
#         pydirectinput.press('f6')
#         pydirectinput.press('f5')
#     elif key == Key.f12:
#         pass
#
#     # print(f"你按下了{key.char if hasattr(key, 'char') else key.name}键")
#     print(f"你按下了{key}键")
#
# def on_release(key):
#     pass
#     # print(f"你按下了{key.char if hasattr(key, 'char') else key.name}键")
#     # print(f"你松开了{key}键")

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        # 初始化用户界面
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('QTable View Example')
        self.resize(500, 300)

        # 创建水平布局
        h_layout = QHBoxLayout()

        # 创建一个TableView并将其放置在水平布局中
        table_view = QTableView(self)
        h_layout.addWidget(table_view)

        # 创建一个数据模型
        self.model  = QStandardItemModel(10, 4)

        # 设置数据模型的表头标签
        self.model.setHorizontalHeaderLabels(["位置", "怪物", "距离下次刷新时间", "当前状态"])


        # 将数据模型设置给TableView
        table_view.setModel(self.model)

        # 调整所有列的宽度以适应内容
        table_view.resizeColumnsToContents()

        # 调整所有行的高度以适应内容
        table_view.resizeRowsToContents()

        # 显示网格线
        table_view.showGrid()

        # 将水平布局设置为窗口的布局
        self.setLayout(h_layout)

    def proc_data(self, data):
        for row in range(len(data)):
                for column in range(4):
                    item = QStandardItem(data[row][column])
                    self.model.setItem(row, column, item)

# 主要全局变量
continue_click = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())


    # # 初始化
    # wss = WindScreenShot('新缘起墨香二区友情提醒:注意保护账号及装备安全,谨慎交易!(Ctrl+W隐藏/显示游戏)[R复活窗口][E洗恶]', 'pyqt')
    # dk = DragKill(wss.hwnd, wss.rect)
    # op = Operate(wss.hwnd)
    #
    # shot_detect_thread = threading.Thread(target=start)
    # shot_detect_thread.start()
    # # dt = detect()
    # # detect = threading.Thread(target=start)    # 创建持续获取图片并侦测的线程
    # # detect.start()
    # # 启动键盘监听
    # with Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()
    #
    # # while True:
    # #     img0 = wss.run()
    # #     dt.run(img0)
    # #     # img = cv2.imread('E:\\yolov5\\images\\detect_img.jpg')
    # #     # cv2.imshow('pre', img)
    # #     # cv2.waitKey(0)  # 1 millisecond