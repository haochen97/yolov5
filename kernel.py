import cv2
import numpy as np
import win32api, win32con, win32gui


def process_path(filename:str, task:int=0):
    '''
    处理文件路径.
    @param
    filename:文件名，字符串形式。
    task:是否为任务图片，默认为0.
    '''

    path = f'E:\\Projects\\mxtest\\img\\{filename}.png'
    return path


def match(template_picture: str, gray=1, imshow=0, multiple=0, sequence=0, threshold=0.7):
    """
    @param
    base：作为模板匹配的底图文件名
    template:模板图片文件名
    gray:默认为1,表示将BGR图像转为GRAY图;如果为0，则不转为GRAY；如果为2，则在转为GRAY后进行二值化。
    imshow：是否显示图像，默认为0不显示。
    multiple:匹配多个目标，默认为0不开机，如果为1则开启。
    sequence:当多目标匹配时，返回从上至下的某个值，默认为0返回最上方的。
    threshold:匹配阈值，默认为0.9
    @return
    返回搜索到的模板图片中心点坐标(x，y)
    """

    # 读取底图和模板图片
    src = cv2.imread('E:\\Projects\\mxtest\\img\\img0\\img0.jpg')
    template = cv2.imread(process_path(template_picture))
    
    # 读取模板图片的高和宽
    h, w = template.shape[:2]

    # 是否灰度处理
    if gray == 1:
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        while imshow == 1:
            key = cv2.waitKey(1)
            cv2.imshow('src', src)
            cv2.imshow('template', template)
            # 停止显示
            if key & 0xFF == 27:      # 按esc键退出
                break
    elif gray == 2:
        src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        res, src = cv2.threshold(src, 203, 255, cv2.THRESH_BINARY)
        res, template = cv2.threshold(src, 203, 255, cv2.THRESH_BINARY)
        while imshow == 1:
            key = cv2.waitKey(1)
            cv2.imshow('src', src)
            cv2.imshow('template', template)
            # 停止显示
            if key & 0xFF == 27:      # 按esc键退出
                break
    elif gray == 0:
         while imshow == 1:
            key = cv2.waitKey(1)
            cv2.imshow('src', src)
            cv2.imshow('template', template)
            # 停止显示
            if key & 0xFF == 27:      # 按esc键退出
                break
    
    # 是否为多目标匹配
    march_res = cv2.matchTemplate(src, template, cv2.TM_CCOEFF_NORMED)
    if multiple == 0:
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(march_res)
        if maxVal > threshold:
            (x1, y1) = maxLoc
            x2 = x1 + template.shape[1]
            y2 = y1 + template.shape[0]

            center_x = int((x2 - x1)/ 2 + x1)
            center_y = int((y2 - y1)/ 2 + y1)
            return [center_x, center_y]
        else:
            return 0
    elif multiple == 1:
        # np.where返回的坐标值(x,y)是(h,w)，注意h,w的顺序
        loc = np.where(march_res >= threshold)
        center = []
        for pt in zip(*loc[::]):
            xy = (pt[1]+w/2, pt[0]+h/2)
            center.append(xy)
        if center == []:
            return 0
        else:
            return center[sequence]

def search(template_filename:str, multiple=0, sequence=0):
    '''
    增加模板匹配的容错机制
    @param
    template_filename:模板图片文件名。
    click:默认为1，启动点击；为0则不点击。
    multiple:匹配多个目标，默认为0不开机，如果为1则开启。
    sequence:当多目标匹配时，返回从上至下的某个值，默认为0返回最上方的。
    '''
    # 获取模板图片所在位置的中心点坐标
    if multiple == 0:
        center = match(template_filename)
    else:
        center = match(template_filename, multiple=1,sequence=sequence)
    
    # 如果未检测到模板，执行一个等待机制
    i = 0 
    while center == 0:
        center = match(template_filename)
        i += 1
        if i > 30:
            print(f'未匹配到{template_filename}的目标')
            return 0
        continue
    if center != 0:
        #center = coord_trans(center)
        return center
    else:
        return 0

hwnd = 0x0041136C

def coord_trans(center):
    (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
    x = center[0] + left
    y = center[1] + top
    return[x, y]

if __name__ == "__main__":
    pass