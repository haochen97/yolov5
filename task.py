from kernel import match
from mouse_key import Operate
from screenshot import WindScreenShot
import time
import threading

class AutoFarm(Operate):

    # yu-堕落人鱼，xiang-大象，ju-巨人，nv-女神，long-蝶龙
    point = {
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

    def __init__(self, hwnd, location: list, monster: list, line=1):
        super().__init__(hwnd)
        self.img = None
        self.hwnd = None
        self.location = location
        self.monster = monster
        self.line = line
        
    def run(self):
        for loc in self.location:
            self.tansmit(loc)

    # 图片路径处理
    def path(self, filename):
        path = f'location/{filename}.jpg'
        return path

    # 封装兼容性更好的匹配-点击机制
    def tclick(self, name):
        """
        通过时间来限制匹配-点击流程,限定每个匹配点击的用时不超过3s
        """
        start_time = time.time()
        path = self.path(name)
        while True:
            pos = match(self.img, path)
            if pos != 0:
                self.click(pos)
                end_time = time.time()
                print(f'匹配点击：成功点击{name}，用时{int(end_time - start_time)}')
                return 1
            else:
                time_diffrence = end_time - start_time
                if time_diffrence >= 3:
                    print(f'匹配点击：点击{name}超时')
                    break
                return 0


    # 传送
    def tansmit(self, loc):
        print(f'准备传送至{loc}')
        # 生成模板图片路径

        # 点击遁点卷轴，每页的0号位置
        self.tclick('juanzhou')
        # 点击要去的位置
        loc_pos = match(self.img, path)
        if loc_pos == 0:
            page_pos = match(self.img, 'location/2page.jpg')
            self.click(page_pos)
            time.sleep(0.2)
            loc_pos = match(self.img, path)
            self.click(loc_pos)
        else:
            self.click(loc_pos)
        time.sleep(0.2)
        # 点击移动
        yidong_pos = match(self.img, 'location/yidong.jpg')
        self.click(yidong_pos)
        time.sleep(0.2)
        # 点击线路
        line_pos = match(self.img, f'location/{self.line}xian.jpg')
        self.click(yidong_pos)
        time.sleep(0.2)
        # 点击链接
        lianjie_pos = match(self.img, 'location/lianjie.jpg')
        time.sleep(0.5)
        # 等待传送5秒
        start_wait = time.time()
        while True:
            name_pos = match(self.img, 'location/name.jpg')
            end_wait = time.time()
            if name_pos != 0:
                print(f'传送成功，抵达目标地点{loc}')
                break
            else:
                sec = end_wait - start_wait
                if sec >= 5:
                    print('传送失败')
                    break

class Timer:
    def __init__(self):
        pass

def test():
    """
    开始截图并侦测
    """
    while True:
        try:
            fps = 60
            task.img = wss.run()    # 截图
            time.sleep(1/fps)
        except:
            print('出错了')

if __name__ == '__main__':
    wss = WindScreenShot(
        '新缘起墨香二区友情提醒:注意保护账号及装备安全,谨慎交易!(Ctrl+W隐藏/显示游戏)[R复活窗口][E洗恶]', 'pyqt')
    location = ['7', '5l', '1', '10', 'zhong']
    monster = ['nv', 'long', 'xiang', 'yu']
    task = AutoFarm(wss.hwnd, location, monster, line=2)
    task.hwnd = wss.hwnd
    test_thread = threading.Thread(target=test)
    test_thread.start()

    task.run()