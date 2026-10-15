import io
import os
import sys
import cv2
import json
import time
import logging
from copy import deepcopy

import numpy as np
from PIL import Image
from flask import request
from paddle.utils import try_import
from ppocr.utils.utility import get_image_file_list, check_and_read
from ppocr.utils.logging import get_logger
from ppocr.utils.visual import draw_ser_results, draw_re_results
from tools.infer.predict_system import TextSystem
from layout.predict_layout import LayoutPredictor
from table.predict_table import TableSystem, to_excel
from utility import parse_args, draw_structure_result, cal_ocr_word_box

logger = get_logger()

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, "../")))

os.environ["FLAGS_allocator_strategy"] = "auto_growth"


class StructureSystem(object):
    def __init__(self, temp_args):
        self.mode = temp_args.mode
        self.recovery = temp_args.recovery

        self.image_orientation_predictor = None
        self.layout_predictor = None
        self.text_system = None
        self.table_system = None

        self.layout_predictor = LayoutPredictor(temp_args)
        self.text_system = TextSystem(temp_args)
        self.table_system = TableSystem(temp_args, self.text_system.text_detector, self.text_system.text_recognizer)
        self.return_word_box = temp_args.return_word_box

    def __call__(self, img):
        layout_res, elapse = self.layout_predictor(img)
        text_res, ocr_time_dict = self._predict_text(img)

        region = layout_res[0]
        x1, y1, x2, y2 = region["bbox"]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        bbox = [x1, y1, x2, y2]
        return self._filter_text_res(text_res, bbox)

    def _predict_text(self, img):
        filter_boxes, filter_rec_res, ocr_time_dict = self.text_system(img)

        # remove style char,
        # when using the recognition model trained on the PubtabNet dataset,
        # it will recognize the text format in the table, such as <b>
        style_token = [
            "<strike>",
            "<strike>",
            "<sup>",
            "</sub>",
            "<b>",
            "</b>",
            "<sub>",
            "</sup>",
            "<overline>",
            "</overline>",
            "<underline>",
            "</underline>",
            "<i>",
            "</i>",
        ]
        res = []
        for box, rec_res in zip(filter_boxes, filter_rec_res):
            rec_str, rec_conf = rec_res[0], rec_res[1]
            for token in style_token:
                if token in rec_str:
                    rec_str = rec_str.replace(token, "")
            if self.return_word_box:
                word_box_content_list, word_box_list = cal_ocr_word_box(
                    rec_str, box, rec_res[2]
                )
                res.append(
                    {
                        "text": rec_str,
                        "confidence": float(rec_conf),
                        "text_region": box.tolist(),
                        "text_word": word_box_content_list,
                        "text_word_region": word_box_list,
                    }
                )
            else:
                res.append(
                    {
                        "text": rec_str,
                        "confidence": float(rec_conf),
                        "text_region": box.tolist(),
                    }
                )
        return res, ocr_time_dict

    def _filter_text_res(self, text_res, bbox):
        res = []
        for r in text_res:
            box = r["text_region"]
            rect = box[0][0], box[0][1], box[2][0], box[2][1]
            if self._has_intersection(bbox, rect):
                res.append(r)
        return res

    def _has_intersection(self, rect1, rect2):
        x_min1, y_min1, x_max1, y_max1 = rect1
        x_min2, y_min2, x_max2, y_max2 = rect2
        if x_min1 > x_max2 or x_max1 < x_min2:
            return False
        if y_min1 > y_max2 or y_max1 < y_min2:
            return False
        return True


def main(in_args):
    # FIXME 前置参数——以后应该可以放全局变量里
    args.det_model_dir = 'other/ch_PP-OCRv3_det_infer'
    args.rec_model_dir = 'other/ch_PP-OCRv3_rec_infer'
    args.rec_char_dict_path = 'other/ppocr_keys_v1.txt'
    args.table_model_dir = 'other/ch_ppstructure_mobile_v2.0_SLANet_infer'
    args.table_char_dict_path = 'other/table_structure_dict_ch.txt'
    args.layout_model_dir = 'other/picodet_lcnet_x1_0_fgd_layout_cdla_infer'
    args.layout_dict_path = 'other/layout_cdla_dict.txt'
    args.return_word_box = True

    structure_sys = StructureSystem(in_args)
    img = cv2.imread(in_args.image_dir)
    res = structure_sys(img)  # TODO 检查输出内容
    print(res)
    # return jsonify(text_info_list)


if __name__ == "__main__":
    # 我想简单的获取结果，输出即可
    # Conda环境已配置成功
    # 部署为后台服务，直接返回数据，可以查看txt生成的地方

    # image_file = request.files['image']
    # image_stream = image_file.stream
    # image = Image.open(io.BytesIO(image_stream.read()))
    # image_np = np.array(image)

    args = parse_args()
    args.image_dir = '1.jpg'  # 这里控制文件
    main(args)

# 想部署到后台，但是发现它过于复杂，我需要把他封装成函数，传参、处理、返回结果，如同OCR_Service

# TODO 下一步，处理数据
