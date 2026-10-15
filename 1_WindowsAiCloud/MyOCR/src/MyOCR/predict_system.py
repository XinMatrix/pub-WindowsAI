import os
import sys
import cv2
import json
import time
import logging
from copy import deepcopy

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
    def __init__(self, args):
        self.mode = args.mode
        self.recovery = args.recovery

        self.image_orientation_predictor = None
        if args.image_orientation:
            import paddleclas

            self.image_orientation_predictor = paddleclas.PaddleClas(
                model_name="text_image_orientation"
            )

        if self.mode == "structure":
            if not args.show_log:
                logger.setLevel(logging.INFO)
            if args.layout == False and args.ocr == True:
                args.ocr = False
                logger.warning(
                    "When args.layout is false, args.ocr is automatically set to false"
                )
            # init model
            self.layout_predictor = None
            self.text_system = None
            self.table_system = None
            if args.layout:
                self.layout_predictor = LayoutPredictor(args)
                if args.ocr:
                    self.text_system = TextSystem(args)
            if args.table:
                if self.text_system is not None:
                    self.table_system = TableSystem(
                        args,
                        self.text_system.text_detector,
                        self.text_system.text_recognizer,
                    )
                else:
                    self.table_system = TableSystem(args)

        elif self.mode == "kie":
            from kie.predict_kie_token_ser_re import SerRePredictor

            self.kie_predictor = SerRePredictor(args)

        self.return_word_box = args.return_word_box

    def __call__(self, img, return_ocr_result_in_table=False, img_idx=0):
        time_dict = {
            "image_orientation": 0,
            "layout": 0,
            "table": 0,
            "table_match": 0,
            "det": 0,
            "rec": 0,
            "kie": 0,
            "all": 0,
        }
        start = time.time()

        if self.image_orientation_predictor is not None:
            tic = time.time()
            cls_result = self.image_orientation_predictor.predict(input_data=img)
            cls_res = next(cls_result)
            angle = cls_res[0]["label_names"][0]
            cv_rotate_code = {
                "90": cv2.ROTATE_90_COUNTERCLOCKWISE,
                "180": cv2.ROTATE_180,
                "270": cv2.ROTATE_90_CLOCKWISE,
            }
            if angle in cv_rotate_code:
                img = cv2.rotate(img, cv_rotate_code[angle])
            toc = time.time()
            time_dict["image_orientation"] = toc - tic

        if self.mode == "structure":
            ori_im = img.copy()
            if self.layout_predictor is not None:
                layout_res, elapse = self.layout_predictor(img)
                time_dict["layout"] += elapse
            else:
                h, w = ori_im.shape[:2]
                layout_res = [dict(bbox=None, label="table")]

            # As reported in issues such as #10270 and #11665, the old
            # implementation, which recognizes texts from the layout regions,
            # has problems with OCR recognition accuracy.
            #
            # To enhance the OCR recognition accuracy, we implement a patch fix
            # that first use text_system to detect and recognize all text information
            # and then filter out relevant texts according to the layout regions.
            text_res = None
            if self.text_system is not None:
                text_res, ocr_time_dict = self._predict_text(img)
                time_dict["det"] += ocr_time_dict["det"]
                time_dict["rec"] += ocr_time_dict["rec"]

            res_list = []
            for region in layout_res:
                res = ""
                if region["bbox"] is not None:
                    x1, y1, x2, y2 = region["bbox"]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    roi_img = ori_im[y1:y2, x1:x2, :]
                else:
                    x1, y1, x2, y2 = 0, 0, w, h
                    roi_img = ori_im
                bbox = [x1, y1, x2, y2]

                if region["label"] == "table":
                    if self.table_system is not None:
                        res, table_time_dict = self.table_system(
                            roi_img, return_ocr_result_in_table
                        )
                        time_dict["table"] += table_time_dict["table"]
                        time_dict["table_match"] += table_time_dict["match"]
                        time_dict["det"] += table_time_dict["det"]
                        time_dict["rec"] += table_time_dict["rec"]
                else:
                    if text_res is not None:
                        # Filter the text results whose regions intersect with the current layout bbox.
                        res = self._filter_text_res(text_res, bbox)

                res_list.append(
                    {
                        "type": region["label"].lower(),
                        "bbox": bbox,
                        "img": roi_img,
                        "res": res,
                        "img_idx": img_idx,
                    }
                )

            end = time.time()
            time_dict["all"] = end - start
            return res_list, time_dict

        elif self.mode == "kie":
            re_res, elapse = self.kie_predictor(img)
            time_dict["kie"] = elapse
            time_dict["all"] = elapse
            return re_res[0], time_dict

        return None, None

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


def save_structure_res(res, save_folder, img_name, img_idx=0):
    excel_save_folder = os.path.join(save_folder, img_name)
    os.makedirs(excel_save_folder, exist_ok=True)
    res_cp = deepcopy(res)
    # save res
    with open(
            os.path.join(excel_save_folder, "res_{}.txt".format(img_idx)),
            "w",
            encoding="utf8",
    ) as f:
        for region in res_cp:
            roi_img = region.pop("img")
            f.write("{}\n".format(json.dumps(region)))

            if (
                    region["type"].lower() == "table"
                    and len(region["res"]) > 0
                    and "html" in region["res"]
            ):
                excel_path = os.path.join(
                    excel_save_folder, "{}_{}.xlsx".format(region["bbox"], img_idx)
                )
                to_excel(region["res"]["html"], excel_path)
            elif region["type"].lower() == "figure":
                img_path = os.path.join(
                    excel_save_folder, "{}_{}.jpg".format(region["bbox"], img_idx)
                )
                cv2.imwrite(img_path, roi_img)


def main(in_args):
    image_file_list = get_image_file_list(in_args.image_dir)
    image_file_list = image_file_list
    image_file_list = image_file_list[in_args.process_id:: in_args.total_process_num]

    if not in_args.use_pdf2docx_api:
        structure_sys = StructureSystem(in_args)
        save_folder = os.path.join(in_args.output, structure_sys.mode)
        os.makedirs(save_folder, exist_ok=True)
    img_num = len(image_file_list)

    for i, image_file in enumerate(image_file_list):
        logger.info("[{}/{}] {}".format(i, img_num, image_file))
        img, flag_gif, flag_pdf = check_and_read(image_file)
        img_name = os.path.basename(image_file).split(".")[0]

        if in_args.recovery and in_args.use_pdf2docx_api and flag_pdf:
            try_import("pdf2docx")
            from pdf2docx.converter import Converter

            os.makedirs(in_args.output, exist_ok=True)
            docx_file = os.path.join(in_args.output, "{}_api.docx".format(img_name))
            cv = Converter(image_file)
            cv.convert(docx_file)
            cv.close()
            logger.info("docx save to {}".format(docx_file))
            continue

        if not flag_gif and not flag_pdf:
            img = cv2.imread(image_file)

        if not flag_pdf:
            if img is None:
                logger.error("error in loading image:{}".format(image_file))
                continue
            imgs = [img]
        else:
            imgs = img

        all_res = []
        for index, img in enumerate(imgs):
            res, time_dict = structure_sys(img, img_idx=index)
            img_save_path = os.path.join(
                save_folder, img_name, "show_{}.jpg".format(index)
            )
            os.makedirs(os.path.join(save_folder, img_name), exist_ok=True)
            if structure_sys.mode == "structure" and res != []:
                draw_img = draw_structure_result(img, res, in_args.vis_font_path)
                save_structure_res(res, save_folder, img_name, index)
            elif structure_sys.mode == "kie":
                if structure_sys.kie_predictor.predictor is not None:
                    draw_img = draw_re_results(img, res, font_path=in_args.vis_font_path)
                else:
                    draw_img = draw_ser_results(img, res, font_path=in_args.vis_font_path)

                with open(
                        os.path.join(save_folder, img_name, "res_{}_kie.txt".format(index)),
                        "w",
                        encoding="utf8",
                ) as f:
                    res_str = "{}\t{}\n".format(
                        image_file, json.dumps({"ocr_info": res}, ensure_ascii=False)
                    )
                    f.write(res_str)
            if res != []:
                cv2.imwrite(img_save_path, draw_img)
                logger.info("result save to {}".format(img_save_path))
            if in_args.recovery and res != []:
                from recovery.recovery_to_doc import (
                    sorted_layout_boxes,
                    convert_info_docx,
                )

                h, w, _ = img.shape
                res = sorted_layout_boxes(res, w)
                all_res += res

        if in_args.recovery and all_res != []:
            try:
                convert_info_docx(img, all_res, save_folder, img_name)
            except Exception as ex:
                logger.error(
                    "error in layout recovery image:{}, err msg: {}".format(
                        image_file, ex
                    )
                )
                continue
        logger.info("Predict time : {:.3f}s".format(time_dict["all"]))


if __name__ == "__main__":
    # 我想简单的获取结果，输出即可
    # Conda环境已配置成功
    # 部署为后台服务，直接返回数据，可以查看txt生成的地方

    args = parse_args()
    args.image_dir = '../img/5.jpg'  # 这里控制文件
    args.det_model_dir = 'other/ch_PP-OCRv3_det_infer'
    args.rec_model_dir = 'other/ch_PP-OCRv3_rec_infer'
    args.rec_char_dict_path = 'other/ppocr_keys_v1.txt'
    args.table_model_dir = 'other/ch_ppstructure_mobile_v2.0_SLANet_infer'
    args.table_char_dict_path = 'other/table_structure_dict_ch.txt'
    args.layout_model_dir = 'other/picodet_lcnet_x1_0_fgd_layout_cdla_infer'
    args.layout_dict_path = 'other/layout_cdla_dict.txt'
    args.vis_font_path = 'other/chinese_cht.ttf'
    args.return_word_box = True
    main(args)

# 想部署到后台，但是发现它过于复杂，我需要把他封装成函数，传参、处理、返回结果，如同OCR_Service

# TODO 下一步，处理数据
