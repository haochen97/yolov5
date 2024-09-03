from screenshot import WindScreenShot
from yolodetect import mydetect
import cv2
import threading
from yolodetect.mydetect import detect
from pynput.keyboard import Listener, Key
from combine import DragKill


def start():
    """
    开始截图并侦测
    """
    while True:
        try:
            img0 = wss.run()
            # dt.run(img0)
        except:
            print('出错了')


def on_press(key):
    # 当按下esc，结束监听
    if key == Key.esc:
        print(f"你按下了esc，监听结束")
        return False
    print(f"你按下了{key.char if hasattr(key, 'char') else key.name}键")
    print(f"你按下了{key}键")


def on_release( key):
    print(f"你按下了{key.char if hasattr(key, 'char') else key.name}键")
    print(f"你松开了{key}键")


if __name__ == "__main__":
    # 初始化
    wss = WindScreenShot('缘起墨香', 'pyqt')
    dk = DragKill(wss)
    # dt = detect()
    # detect = threading.Thread(target=start)    # 创建持续获取图片并侦测的线程
    # detect.start()
    # # 启动键盘监听
    # with Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()

    # while True:
    #     img0 = wss.run()
    #     dt.run(img0)
    #     # img = cv2.imread('E:\\yolov5\\images\\detect_img.jpg')
    #     # cv2.imshow('pre', img)
    #     # cv2.waitKey(0)  # 1 millisecond