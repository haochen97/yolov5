from operator import index
import sys

import pydirectinput
import win32gui
from pywin.Demos.cmdserver import flags
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from pywin.mfc.object import Object

from kernel import match
from mouse_key import Operate
from screenshot import WindScreenShot
import time
import threading
import queue



class AutoFarm(Operate, QObject):

    # yu-堕落人鱼，xiang-大象，ju-巨人，nv-女神，long-蝶龙
    loc_mon = {
        '12l': ['yu'],
        '12m': ['xiang', 'ju'],
        '12r': ['nv', 'yu'],
        '12b': ['yu'],
        '10': ['yu', 'ju'],
        '10r': ['yu', 'ju'],
        'zhong': ['long', 'yu'],
        'zhongxia': ['yu'],
        '9': ['nv', 'yu', 'ju'],
        '8t': ['long'],
        '8b': ['yu'],
        '1': ['long', 'yu', 'ju'],
        '3l': ['nv', 'yu'],
        '3r': ['xiang', 'ju'],
        '5': ['nv', 'long', 'ju'],
        '5l': ['xiang', 'ju'],
        '6': ['yu', 'xiang'],
        '7': ['nv', 'ju']
    }
    refresh_time = {
        'yu': 295,
        'long': 295,
        'nv': 295,
        'xiang': 295,
        'ju': 240
    }

    update_data = pyqtSignal(object)
    def __init__(self, hwnd, location: list, monster: list, line=1):
        super().__init__(hwnd)
        super(QObject, self).__init__()
        self.img = None
        self.hwnd = hwnd
        self.location = location
        self.monster = monster
        self.line = line
        self.task_queue = queue.Queue()    # 任务队列，先进先出
        self.supply_queue = queue.Queue()    # 补充队列，当task_queue队列为空时，自动填补元素
        for loc in location:
            self.task_queue.put(loc)
            self.supply_queue.put(loc)
        self.time_ctrl = []    # 时间控制队列
        self.switch_flag = True    # 程序开关


        
    def run(self):
        while self.switch_flag:
            if self.task_queue.empty():
                loc = self.supply_queue.get()    # 从补充队列里取出来一个元素
                self.task_queue.put(loc)    # 放进任务队列
                self.supply_queue.put(loc)    # 同时放进补充队列末端，保证补充队列里元素数量不变
            else:
                loc = self.task_queue.get()
                self.tansmit(loc)
                self.fight(loc)
    # 图片路径处理
    def path(self, filename):
        path = f'location/{filename}.jpg'
        return path

    # 封装兼容性更好的匹配-点击机制
    def tclick(self, name, f2=1):
        """
        通过时间来限制匹配-点击流程,限定每个匹配点击的用时不超过3s
        f2:数量是多少就点击几下
        """
        start_time = time.time()~
        path = self.path(name)
        while True:
            try:
                pos = match(template_picture=path)~
            except:~
                print("tclick:匹配错误，应该是读取屏幕截图出错了,重试")
                continue
            if pos != 0:~~
                self.click(pos, flags2=f2)
                end_time = time.time()
                print(f'匹配点击：成功点击{name}，坐标{pos},用时{int(end_time - start_time)}')~~
                return 1~
            else:
                end_time = time.time()~
                time_diffrence = end_time - start_time
                if time_diffrence >= 3:
                    print(f'匹配点击：点击{name}超时')
                    return 0

    # 传送
    def tansmit(self, loc):
        print(f'准备传送至{loc}')
        # 点击遁点卷轴，每页的0号位置
        self.tclick('juanzhou', f2=2)~
        # 点击要去的位置
        if self.tclick(loc) == 1:
            pass
        else:
            self.tclick('2page')~
            self.tclick(loc)
        # 点击移动
        self.tclick('yidong')
        # 点击线路~
        self.tclick(f'{self.line}xian')
        # 点击链接~~
        self.tclick('lianjie')~~~
        # 等待传送5秒~~
        time.sleep(2.5)~
        self.tclick('chuansong')
        time.sleep(1)
        start_wait = time.time()
        while True:~
            name_pos = match(template_picture='location/name.jpg')
            end_wait = time.time()~~
            if name_pos != 0:
                print(f'传送成功，抵达目标地点{loc}')
                self.autof5()
                break~~
            else:
                sec = end_wait - start_wait
                if sec >= 5:
                    print('传送失败')
                    break

    def fight(self, loc, max_wait_time=5):
        """

        max_wait_time = 5秒内要找到怪物，否则去下一个点位
        """
        start_time = int(time.time())
        monster_list = self.loc_mon[loc]
        print('开始寻找怪物目标')
        while True:
            for mst in monster_list:
                if mst in self.monster:    # 如果怪物属于目标怪物时进行下一步
                    if self.time_ctrl:    # 判断怪物的刷新时间，更改最大等待时长
                        for ta in self.time_ctrl:
                            if ta[0] == loc:
                                if ta[1] == mst:
                                    if int(ta[2] - time.time()) >= 6:
                                        max_wait_time = int(ta[2] - time.time())
                    try:
                        pos = match(template_picture=f'{self.path(mst)}')
                    except:
                        time.sleep(0.1)
                        print("fight任务：匹配错误159行，应该是读取屏幕截图出错了,重试")
                        continue
                    if pos != 0:
                        attack_time = time.time()
                        print(f'找到怪物：{mst},开始攻击！')
                        while True:
                            try:
                                pos = match(template_picture=f'{self.path(mst)}')
                            except:
                                continue
                                print("fight任务：正在对目标进行攻击。匹配错误，应该是读取屏幕截图出错了,重试")
                            if pos == 0:
                                dead_time = time.time()    # 怪物死亡时间
                                next_time = int(dead_time + 295)    # 下一次刷新时间
                                kill_time = int(dead_time - start_time)
                                status = 'dead'
                                sign = (loc, mst, next_time, status)    # 位置， 怪物名称， 下次刷新时间， 状态
                                # 判断time_ctrl列表中有没有该怪物的信息，如果有-更新，如果没有-新增
                                if self.time_ctrl:
                                    for ta in self.time_ctrl:
                                        if ta[0] == loc:
                                            if ta[1] == mst:
                                                self.time_ctrl[self.time_ctrl.index(ta, 0, len(self.time_ctrl) - 1)] = sign
                                            else:
                                                self.time_ctrl.append(sign)
                                        else:
                                            self.time_ctrl.append(sign)
                                else:
                                    self.time_ctrl.append(sign)    # 如果time_ctrl列表为空，直接保存下次刷新信息
                                start_time = start_time + kill_time  # 刷新fight任务的等待时间，确保不会结束
                                print(f'击杀{loc}点{mst},用时{kill_time}秒')
                                break
                            else:
                                time.sleep(0.5)
                time.sleep(0.1)
            end_time = int(time.time())
            print(f'已经寻找{int(end_time - start_time)}秒，最多{max_wait_time}')
            if end_time - start_time >= max_wait_time:
                print(f"在{loc}未发现可攻击目标，前往下个地图")
                pydirectinput.press('f5')
                time.sleep(1)
                break

    def timer(self):
        if self.time_ctrl:
            lenth_tc = len(self.time_ctrl)
            for ta in self.time_ctrl:
                if ta[3] == 'dead':
                    ta_index = self.time_ctrl.index(ta, 0)
                    distance = int(ta[2] - time.time())
                    if distance <= 10:
                        self.task_queue.put(ta[0])    # 当距离下一次还有10秒时，把目标地点放入任务队列
                        ta[3] = 'waitkill'    # 修改目标状态位等待击杀
                        self.time_ctrl[ta_index] = ta    # 更新目标状态
                else:
                    pass
            self.update_data.emit(self.time_ctrl)
        else:
            pass

    def autof5(self):
        win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(0.5)
        pydirectinput.press('f6')
        time.sleep(0.5)
        self.tclick('huoquzuobiao')
        time.sleep(0.5)
        pydirectinput.press('f6')
        pydirectinput.press('f5')

def test():
    """
    开始截图并侦测
    """
    while True:
        try:
            fps = 60
            # 共享屏幕截图资源
            wss.run()    # 截图
            time.sleep(1/fps)
        except:
            print('出错了')

def start_task():
    while True:
            ex.emitter.run()


if __name__ == '__main__':
    # 创建QApplication类的实例
    app = QApplication(sys.argv)
    wss = WindScreenShot(
        '新缘起墨香二区友情提醒:注意保护账号及装备安全,谨慎交易!(Ctrl+W隐藏/显示游戏)[R复活窗口][E洗恶]', 'pyqt')
    location = ['7', '5l', '1', '10', 'zhong']
    monster = ['nv', 'long', 'xiang', 'yu']
    # task = AutoFarm(wss.hwnd, location, monster, line=2)
    # 创建对象
    from show import QtableViewExample
    ex = QtableViewExample(wss.hwnd, location, monster, line=2)
    # 创建窗口
    ex.show()


    test_thread = threading.Thread(target=test)
    task_thread = threading.Thread(target=start_task)
    test_thread.start()
    task_thread.start()
    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
