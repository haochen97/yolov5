from screenshot import shot
from kernel import match
from mouse_key import Operate

if __name__ == '__main__':
    sh = shot('pyqt', '新缘起墨香二区友情提醒:注意保护账号及装备安全,谨慎交易!(Ctrl+W隐藏/显示游戏)[R复活窗口][E洗恶]')
    opt = Operate(sh.hwnd)
    sh.run()
    pos = match('icon_wuping')
    print(pos)
    opt.click(pos)
    pos = match('zidongshoulie')
    print(pos)
    opt.drag2(pos, (1599, 899))