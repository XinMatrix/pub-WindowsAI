import io

import numpy as np
from PIL import Image
from flask import request, Flask, jsonify
from src.MyOCR.layout.predict_layout import LayoutPredictor
from src.MyOCR.table.predict_table import TableSystem
from src.MyOCR.tools.infer.predict_system import TextSystem
from src.MyOCR.utility import parse_args, cal_ocr_word_box

app = Flask(__name__)

structure_sys = None


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
        # print('layout_res = ', layout_res)  # FIXME 为什么这个东西会为空呢
        if layout_res:
            region = layout_res[0]
            x1, y1, x2, y2 = region["bbox"]
        else:
            x1, y1, x2, y2 = [0, 0, 0, 0]
        bbox = [int(x1), int(y1), int(x2), int(y2)]
        return self._filter_text_res(text_res, bbox)

    def _predict_text(self, img):
        filter_boxes, filter_rec_res, ocr_time_dict = self.text_system(img)
        res = []
        for box, rec_res in zip(filter_boxes, filter_rec_res):
            rec_str, rec_conf = rec_res[0], rec_res[1]
            word_box_content_list, word_box_list = cal_ocr_word_box(rec_str, box, rec_res[2])
            print(rec_str)
            res.append({
                "text": rec_str,
                "confidence": round(float(rec_conf), 2),
                "text_region": box.tolist(),
                "text_word": word_box_content_list,
                "text_word_region": word_box_list,
            })
        return res, ocr_time_dict

    def _filter_text_res(self, text_res, bbox):
        res = []
        for r in text_res:
            box = r["text_region"]
            rect = box[0][0], box[0][1], box[2][0], box[2][1]
            if self._has_intersection(bbox, rect):
                res.append(r)
        return res

    @staticmethod
    def _has_intersection(rect1, rect2):
        x_min1, y_min1, x_max1, y_max1 = rect1
        x_min2, y_min2, x_max2, y_max2 = rect2
        if x_min1 > x_max2 or x_max1 < x_min2:
            return False
        if y_min1 > y_max2 or y_max1 < y_min2:
            return False
        return True


@app.route('/ocr_accuracy', methods=['POST'])
def process_image():
    image_file = request.files['image']
    image_stream = image_file.stream
    image = Image.open(io.BytesIO(image_stream.read()))
    image_np = np.array(image)
    result = structure_sys(image_np)
    return jsonify(result)


@app.route('/', methods=['GET'])
def showHello():
    return 'Hello,This is Accurate OCR'


if __name__ == "__main__":
    # 感觉精准OCR就够用了，一整个句子的好像还不需要
    args = parse_args()
    args.det_model_dir = 'MyOCR/other/ch_PP-OCRv3_det_infer'
    args.rec_model_dir = 'MyOCR/other/ch_PP-OCRv3_rec_infer'
    args.rec_char_dict_path = 'MyOCR/other/ppocr_keys_v1.txt'
    args.table_model_dir = 'MyOCR/other/ch_ppstructure_mobile_v2.0_SLANet_infer'
    args.table_char_dict_path = 'MyOCR/other/table_structure_dict_ch.txt'
    args.layout_model_dir = 'MyOCR/other/picodet_lcnet_x1_0_fgd_layout_cdla_infer'
    args.layout_dict_path = 'MyOCR/other/layout_cdla_dict.txt'
    args.return_word_box = True
    structure_sys = StructureSystem(args)

    app.run('0.0.0.0', port=5001)
