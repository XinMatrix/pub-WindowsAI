import yaml
import multiprocessing
from ultralytics import YOLO


def read_yaml():
    with open('data.yaml', 'r') as file:
        data = yaml.safe_load(file)
    return data.get('names', [])


def train_model(epochs=20):
    multiprocessing.freeze_support()  # Windows需要开启子线程(Jupyter中不需要)
    model = YOLO(r'C:\Users\USER\Desktop\yolov8x.pt')  # 更大的模型效果可能更好
    model.train(data='data.yaml', epochs=epochs, patience=0)  # patience=0
    model.export(format='onnx')
    # results = model.val()


def process_images():
    yaml_data = read_yaml()
    filename_list = ['images/train/1.jpg', 'images/train/2.jpg']
    temp_model = YOLO('best.onnx', task='detect')
    total_confidence = 0
    total_boxes = 0
    for filename in filename_list:
        temp_results = temp_model(filename)
        boxes = temp_results[0].boxes
        for i in range(len(boxes.xyxy)):
            center_x = (boxes.xyxy[i][0] + boxes.xyxy[i][2]) / 2
            center_y = (boxes.xyxy[i][1] + boxes.xyxy[i][3]) / 2
            confidence = round(boxes.conf[i].item(), 2)
            total_confidence += confidence
            total_boxes += 1
            print("Box {}: ".format(i + 1))
            print("  Center Point (x, y): ", (center_x.item(), center_y.item()))
            print("  Confidence: ", confidence)
            print("  Label: ", yaml_data[int(boxes.cls[i].item())])
        temp_results[0].show()

    if total_boxes > 0:
        average_confidence = total_confidence / total_boxes
        print("Average Confidence: ", average_confidence)


if __name__ == '__main__':
    # train_model(50)
    process_images()  # 准确率不高，提高epoch试试，其实感觉不需要用yolo，直接用ocr计算文本匹配度不也行？
    # YOLO的问题是要训练,后期性能开销会比较大，而且，就识别精度而言，YOLO不一定优于OCR

    # TODO 出现问题了，这条路行不通

    # 一个页面的所有信息
    # 参考样例: sample.jpg
    # 左上角图标: Windows安全中心 左上角文字: 用户帐户控制设置
    # 分析: 这些信息说明这是一个用户帐户控制设置，同时属于Windows安全中心管理
    # 右上角图标: 横杠 方框 叉
    # 解析: 标准的Windows程序窗口管理交互按钮，分别是最小化（先隐藏）、最大化（全屏显示）以及关闭（终止窗口程序）
    # 向下第一行文本: 选择何时通知你有关计算机更改的消息
    # 解析: 明确了两个对象，选择何时及有关计算机更改的消息，文本是深蓝色，同时字号最大，没有标点符号
    # 向下第二行文本: 用户帐户控制有助于预防有害程序对你的计算机进行更改。
    # 解析: 是对第一行文本的补充说明，字号较小，黑色，有标点符号，与第一行文本对齐
    # 向下第三行文本: 有关用户帐户控制设置的详细信息
    # 解析: 是对第一行文本的补充，与第二行文本对齐，蓝色，有下划线，默认选中（因为它是可以点击交互的，使用虚点方框，相隔一个像素）
    # 左侧控制器: 顶部文字: 始终通知，底部文字: 从不通知，中间由一个灰色竖条型进度条组成，其上平均分布了四个左右对称的黑色横杠
    #   有一个蓝色矩形在其中一个位置上
    # 解析: 蓝色矩形的位置说明了现在的通知设置状态，从上到下通知等级逐渐降低（由顶部与底部文字得出）
    # 右侧第一行文本: 仅当应用尝试改变我的计算机时通知我(默认)
    # 解析: 黑色加粗文字，大小属于正文，在框内左上角位置，框由较细淡灰色绘制
    # 右侧第二行文本: 当我对Windows设置进行更改时不要通知我
    # 解析: 使用列表表示信息（文字左侧黑色圆点），配合左侧选项，是对左侧选择的补充
    # 右侧第三行文本: 如果你使用常见应用和访问常见网址，则推荐使用此选项。
    # 解析: 内容由左侧图标与右侧文字组成，图标的意义是'信息'，是一种补充说明文字
    # 下方控制标线: 用于分割内容，开辟一块新区域
    # 解析:无
    # 右下方按钮: 确定
    # 解析: 按钮由图标与文字组成，表示肯定
    # 右下方按钮: 取消
    # 解析: 按钮由图标与文字组成，表示否定

    # 我的操作逻辑:
    #   先看这上面的文字是否符合我的需求，如左上角用户帐户设置，或判别主文字是否与主题强关联（字号最大、颜色最鲜艳的文字）
    #   查找设置方式: 滑动、选择、点击等，找到滑动框
    #   根据滑动框文字移动滑动块，同时对照右侧文字检查是否正确
    #   点击确定并赋权

    # 我的已知知识:
    #   文字会提供信息，操作系统上大部分信息都来自文字
    #
    #
    #
    #

    # 我的操作想法:
    #   假如我不知道要怎么才能弄好，但是我可以尝试进行可用操作，并不断检查是否正确来弄好
    #   1

    # 如果把这些信息都给计算机，它能像我一样用来处理问题吗，我是不是应该先训练一个NLP模型

    # 能不能训练一个模型，告诉它这些信息就能输出要进行的操作
    # 基本感知模型？——包含人类对事物的基本归类，理解
    # 我想要建立一套通用的认知体系，可以用在各个领域

    # Adapter

    # 汇总信息:
    # 对了，记得记录交互效果，如鼠标移至关闭按钮后关闭按钮会出现红色背景，而最小化和最大化则出现淡灰色背景（与原背景相比有区别但不大）
    # 就近划分原则？
    # 我需要交互的部分，以及为什么要这样交互（原因）
    # 键盘还是鼠标控制呢

    # 直接向下操作并没有根据当前信息计算，而仅仅是一种定性操作，无法通用
    # 前期借助GPT，后期自研模型（可以和大厂合作）
