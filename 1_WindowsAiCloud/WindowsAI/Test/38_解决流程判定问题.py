# 此文件是为了解决流程判定问题而提出的新思想的实践
import subprocess

# C:\Windows\System32 64位

if __name__ == '__main__':
    # 执行程序
    subprocess.run(r'C:\Windows\System32\UserAccountControlSettings.exe')
    # 怎么让机器知道这个按钮可以点击呢
    # 针对设置是不是可以用YOLO把所有情况都训练一遍，给个标签——感觉这个方便些——不需要整个截取，仅需需要的部分即可，label对应1234
    # 点击尽量还是用视觉去做吧，按键毕竟局限性太大

    # 一个控件识别模型用来判定是输入框还是按钮——区分按钮是一种不好的行为，应该使用OCR识别文本，术业有专攻——OCR 与 YOLO 同步进行
    # TODO 一个控制器模型用于标记控制器中可以点击的地方
    # TODO 一个结果分析模型用于判定点的对不对——这个模型的参数可能会非常多——遇到问题了，感觉不如OCR加YOLO（注意先后顺序）

    # 因为训练YOLO还是比较简单的，所以可以试试

    # NewCLass(type=Button,text=确认)
    # 总会有进度的...

    # YOLO居然比OCR快，离谱
