import time

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

def start():
    """
    开始截图并侦测
    """
    while True:
        try:
            fps = 60
            img = wss.run()    # 截图
            dk.run(img)    # 自动拖击杀窗口
            # dt.run(img0)
            time.sleep(1/fps)
        except:
            print('出错了')


def on_press(key):
    # 当按下esc，结束监听
    if key == Key.esc:
        print(f"你按下了esc，监听结束")
        return False
    elif key == Key.f7:
        pydirectinput.press('f6')
        time.sleep(0.2)
        for _ in range(5):
            pos = match(wss.img, 'huoquzuobiao.jpg', threshold=0.95)
            if pos == 0:
                pass
            else:
                op.click(pos)
                time.sleep(0.2)
                break
        pydirectinput.press('f6')
        pydirectinput.press('f5')
    elif key == Key.f12:
        pass

    # print(f"你按下了{key.char if hasattr(key, 'char') else key.name}键")
    print(f"你按下了{key}键")

def on_release(key):
    pass
    # print(f"你按下了{key.char if hasattr(key, 'char') else key.name}键")
    # print(f"你松开了{key}键")


# 主要全局变量
continue_click = 0


if __name__ == "__main__":
    # 初始化~~~~~~
    wss = WindScreenShot('新缘起墨香二区友情提醒:注意保护账号及装备安全,谨慎交易!(Ctrl+W隐藏/显示游戏)[R复活窗口][E洗恶]', 'pyqt')
    dk = DragKill(wss.hwnd, wss.rect)
    op = Operate(wss.hwnd)

    shot_detect_thread = threading.Thread(target=start)
    shot_detect_thread.start()
    # dt = detect()
    # detect = threading.Thread(target=start)    # 创建持续获取图片并侦测的线程
    # detect.start()
    # 启动键盘监听
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # while True:
    #     img0 = wss.run()
    #     dt.run(img0)
    #     # img = cv2.imread('E:\\yolov5\\images\\detect_img.jpg')
    #     # cv2.imshow('pre', img)
    #     # cv2.waitKey(0)  # 1 millisecond