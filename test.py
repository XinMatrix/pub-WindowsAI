import os
import paddle2onnx
import onnxruntime as ort
import numpy as np


def convert_ocr_final():
    # 配置信息
    tasks = [
        {
            "name": "检测模型 (Det)",
            "dir": r"E:\my_paddle_models\ch_PP-OCRv4_det_infer",
            "out": r"E:\my_paddle_models\ch_PP-OCRv4_det_infer\det_v4.onnx",
            "shape": [1, 3, 1088, 1920]
        },
        {
            "name": "识别模型 (Rec)",
            "dir": r"E:\my_paddle_models\ch_PP-OCRv4_rec_infer",
            "out": r"E:\my_paddle_models\ch_PP-OCRv4_rec_infer\rec_v4.onnx",
            "shape": [1, 3, 48, 320]
        }
    ]

    for task in tasks:
        print(f"\n>>> 正在处理: {task['name']}")

        model_file = os.path.join(task['dir'], "inference.pdmodel")
        params_file = os.path.join(task['dir'], "inference.pdiparams")

        try:
            # 根据你打印的 dir 结果，直接调用 paddle2onnx.export
            # 1.x 版本的 export 接口通常接受这些参数
            success = paddle2onnx.export(
                model_file,
                params_file,
                save_file=task['out'],
                opset_version=12,
                enable_onnx_checker=True
            )

            # 检查文件是否生成
            if os.path.exists(task['out']):
                print(f" [OK] 转换成功！已保存至: {task['out']}")

                # 验证加载
                session = ort.InferenceSession(task['out'], providers=['CPUExecutionProvider'])
                input_node = session.get_inputs()[0]

                # 模拟推理测试
                # 注意：OCR检测模型输入通常叫 'x'
                dummy_input = np.random.random(task['shape']).astype(np.float32)
                outputs = session.run(None, {input_node.name: dummy_input})
                print(f" [OK] 测试成功！输入节点: {input_node.name}, 输出形状: {outputs[0].shape}")
            else:
                print(f" [Error] 转换失败，未生成文件。返回值: {success}")

        except Exception as e:
            print(f" [Error] 运行出错: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    convert_ocr_final()