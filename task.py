from kernel import match
from mouse_key import Operate




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

    def __init__(self, hwnd, location: list, monster: list):
        super().__init__(hwnd)

if __name__ == '__main__':
    location = ['7', '5l', '1', '10', 'zhong']
    monster = ['nv', 'long', 'xiang', 'yu']