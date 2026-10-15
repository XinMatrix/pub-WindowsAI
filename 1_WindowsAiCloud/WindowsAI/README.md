# WindowsAI——前期自动化可以先做Windows设置，让投资人看到效果

    启动Paddle OCR与RWKV即可

    注意 每种程序的下载链接是会动态变化的，以后考虑使用Python每天爬取下载链接

    先做几个软件的安装，再总结抽象

# Tips

    (python38) C:\Users\USER>yolo detect export model=C:\Users\USER\PycharmProjects\WindowsAI\TrainModel\v1.pt format=tflite
    (python38) C:\Users\USER>yolo export model=C:\Users\USER\PycharmProjects\WindowsAI\TrainModel\v1.pt format=tflite
    conda activate python38
    pip install pyinput -i https://pypi.tuna.tsinghua.edu.cn/simple/

    需要以管理员运行PyCharm才行，不然无法点击IDE外

    左上、右上、右下、左下
    position = text_info['position']

    pyautogui.hotkey('win', 'r')
    pyautogui.hotkey('enter')

    测试应使用不常用或较小软件而非QQ    

    综合考虑，我个人倾向于第一种方法，即使用subprocess.Popen()来启动CMD程序，因为它更直接、稳定，不依赖于模拟用户输入

    COY准则: CODE > Image Strong > OCR > YOLO

    wmic WindowsCMD命令控制 wmic service get /?

    小爱最近也在搞——但是还很初级，只能处理已适配程序

# TODO

    操作分为：
        OCR文字处理-信息获取、相似度计算
        模拟输入处理-模拟输入，定义函数
        CV图像处理-硬编码匹配、区块分类(待测试)
        错误检测-XX(待完成)

    最大的问题是训练什么，怎么训练，我想让机器理解这个页面并做出动作
    https://github.com/HughChi/Image-Caption?tab=readme-ov-file

    测试盲目性

    强化学习好像还用不太到
    强化学习可以帮到我吗？可以处理安装时的文字点击顺序——还是有必要一试的

    人工智能领域有多种类型的神经网络，常见的几种包括：
    前馈神经网络（Feedforward Neural Networks）：最基本的神经网络结构，信息在网络中单向传播，没有循环连接。常用于分类和回归任务。
    卷积神经网络（Convolutional Neural Networks，CNN）：主要用于处理图像和视频数据，通过卷积层、池化层和全连接层来提取特征并进行分类。
    循环神经网络（Recurrent Neural Networks，RNN）：具有循环连接的神经网络结构，适用于处理序列数据，如自然语言处理和时间序列预测。
    长短时记忆网络（Long Short-Term Memory，LSTM）：一种特殊的RNN结构，能够更好地捕捉长期依赖关系，广泛应用于语音识别、机器翻译等任务。
    生成对抗网络（Generative Adversarial Networks，GAN）：由生成器和判别器组成的对抗学习框架，用于生成逼真的数据样本。
    强化学习网络（Reinforcement Learning Networks）：与环境交互学习如何通过行为序列来实现某个目标，常用于游戏、机器人控制等领域。
    除了以上几种，还有一些变种和衍生的神经网络结构，如注意力机制（Attention Mechanism）、转移学习（Transfer Learning）等，每种网络类型都有各自的优势和适用场景。根据具体任务需求和数据特点，选择合适的神经网络结构非常重要。

    Snipate是怎么实现识别窗口的

    核心任务：怎么让机器理解一个画面——搜一搜
    我能看懂一张图片是因为
    1.我能对它的文字进行分类——如果全部是乱码我也不能确定功能——能否通过文字相关性判断adapter
    2.我能通过它的图标获取相关文字释义
    3.背景和前景颜色不同，我能知道它在哪里
    色块图
    怎么让一个没用过Windows的小孩知道怎么操作Windows——或者先教会ta再让它操作
    尝试运行GAN网络

    尝试使用中文标签——好像不行，会乱码
    是每一种操作对应一种model还是汇总一个model——答案应该是前者，因为后者会很大且产生许多无用信息，复杂度过高可能也导致模型效果较差
    多种图像识别模型，逐步调用使用，先获取图像分割信息，再获取图像识别信息
    怎么让机器理解一张复杂的图像
    真的复杂，因为人类很多潜意识的内容是不太好直接找到的

    尝试自行搭建深度学习模型

    Paddle OCR还需要优化，我需要知道每个具体的字的坐标

    SavedModel file does not exist at: v1_saved_model\{saved_model.pbtxt|saved_model.pb}

    遇到问题——识别是以句子识别，能不能以单字识别，这样能提高准确率，或者直接计算前两个的距离(需要修正量)
    https://github.com/fanqie03/char-detection/tree/main
    有库，但是比较麻烦，优先使用算法解决

    Listary貌似不能通过crul下载，尝试使用wget——尝试使用传统网页下载——尝试requests

    有机会重写Yaml文件，重头训练——yolov8-p6.yaml
    
    最终需要生成式AI来生成解决办法（投喂数据）

# Finished

    git.ignore *.exe *.mp4 *.pt *.onnx
    WindowsAPI有哪些
    转移所有代码到PyCharm，重置仓库，每次复制转移代码后gitee
    要不试试TK，屏幕上实时显示结果——很令人兴奋
    尝试测试Raw_3——测试成功，准备换软件试试
    自动化测试工具效果堪忧，网页下载链接都爬不到
    继续测试Raw_3，这会应该可以正常结束了——不错
    QQ下载完成，准备测试Listary
    运行完没停止
    Ctrl V 没贴上
    按Esc结束即可
    重建文件夹，按功能分类
    逐个抽象封装
    推理时间怎么突然这么长
