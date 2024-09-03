# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run inference on images, videos, directories, streams, etc.

Usage:
    $ python path/to/detect.py --source path/to/img.jpg --weights yolov5s.pt --img 640
"""

import argparse
import os
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
from torch.jit import annotate
# import mydata

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.experimental import attempt_load
from utils.datasets import LoadImages, LoadStreams
from utils.general import apply_classifier, check_img_size, check_imshow, check_requirements, check_suffix, colorstr, \
    increment_path, non_max_suppression, print_args, scale_coords, set_logging, \
    strip_optimizer, xyxy2xywh
from backup.general import save_one_box
from utils.plots import Annotator, colors
from utils.torch_utils import load_classifier, select_device, time_sync
from utils.augmentations import Albumentations, augment_hsv, copy_paste, letterbox

class detect():
    class_name = {
        0:'人鱼',
        1:'女神',
        2:'大象',
        3:'蝶龙',
        4:'商人',
        5:'人鱼血条',
        6:'大象血条',
        7:'蝶龙血条',
        8:'商人血条',
        9:'女神血条',
        10:'蓝龙出现',
        11:'巨人',
        12:'巨人血条',
        13:'红名敌人',
        14:'和包袱商人交易',
        15:'蚩牛出现',
        16:'赤龙出现'

    }
    def __init__(self):
        self.number = None
        self.ta_names = []
        self.ta_xy = []

    @torch.no_grad()
    def run(self, img, weights='E:\\yolov5\\yolodetect\\runs\\train\\exp2\\weights\\best.pt',  # model.pt path(s)
            save_conf=True,  # save confidences in --save-txt labels
            half=False,  # use FP16 half-precision inference
            ):

        # Load model
        device = select_device('cuda:0')
        w = str(weights[0] if isinstance(weights, list) else weights)
        classify, suffix, suffixes = False, Path(w).suffix.lower(), ['.pt', '.onnx', '.tflite', '.pb', '']
        check_suffix(w, suffixes)  # check weights have acceptable suffix
        pt, onnx, tflite, pb, saved_model = (suffix == x for x in suffixes)  # backend booleans
        stride, names = 64, [f'class{i}' for i in range(1000)]  # assign defaults
        if pt:
            model = torch.jit.load(w) if 'torchscript' in w else attempt_load(weights, map_location=device)
            stride = int(model.stride.max())  # model stride
            names = model.module.names if hasattr(model, 'yolodetect') else model.names  # get class names
            if half:
                model.half()  # to FP16
            if classify:  # second-stage classifier
                modelc = load_classifier(name='resnet50', n=2)  # initialize
                modelc.load_state_dict(torch.load('resnet50.pt', map_location=device)['model']).to(device).eval()

        # Run inference
        img0 = img
        # Padded resize
        img = letterbox(img0, (640, 640), stride=32, auto=True)[0]

        # Convert
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img = img / 255.0  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim

        # Inference
        pred = model(img, augment=False, visualize=False)[0]

        # NMS
        pred = non_max_suppression(pred, conf_thres=0.6, iou_thres=0.45, classes=None, max_det=1000)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            # 归一化
            # gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imgc = img0.copy()
            annotator = Annotator(img0, line_width=2, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

                # Write results
                self.number = 0
                for *xyxy, conf, cls in reversed(det):
                    # 将xyxy（左上角+右下角）格式转化为xywh（中心点+宽长）格式，并除上w，h做归一化，转化为列表再保存
                    # xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()  # normalized xywh
                    line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                    xy = (int(xywh[0]), int(xywh[1]))
                    # save img
                    c = int(cls)  # integer class
                    label = self.class_name[c]
                    self.ta_names.append(label)
                    self.ta_xy.append(xy)
                    # label = '%s %.2f' % (names[int(cls)], conf)
                    # print(label)
                    annotator.box_label(xyxy, label, color=colors(c, True))
                    c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                    label = '%s %.2f' % (self.class_name[int(cls)], conf)
                    # print(label + " (" + str(c1[0]) + "," + str(c1[1]) + "," + str(c2[0]) + "," + str(c2[1]) + ")")
                    # save_one_box(xyxy, imgc, file='E:\\yolov5\\images\\detect_img.jpg', BGR=True)
                    img0 = annotator.result()
                    cv2.imwrite('E:\\yolov5\\images\\detect_img.jpg', img0)
                    self.number += 1
if __name__ == "__main__":
    dt = detect()
    dt.run()
    print(f'检测到{dt.number}个目标, 分别是{dt.ta_names}, 中心点坐标分别为{dt.ta_xy}')
