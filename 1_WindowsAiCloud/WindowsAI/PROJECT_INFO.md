# 该文件用于描述整个项目

# 基本介绍

    WindowsAi是一款使用Python编程语言，借助人工智能等辅助手段开发的Windows操作系统的自动化操作助手
    WindowsAi的最终效果是用户通过文本或语音输入操作命令，程序自动进行相关操作实现用户需求
    WindowsAi的特点是完全自动化，降低用户使用成本，面向用户是全球Windows电脑使用者

    让机器人像人一样使用电脑工作，是WindowsAi的核心理念，也是WindowsAi的主要功能

# 技术概要

    通过类比人类使用电脑时的过程与仿生学原理，使用模拟输入函数模拟鼠标与键盘，使用OCR处理屏幕文字信息，还没有处理图像轮廓信息
    WindowsAi的开发过程经历了两个阶段
        1.逐渐封装过程代码，流程化操作，编写较为简单，实现过字符串转数据类，但不能处理循环操作及异常情况
        2.使用数据库编写操作，可以根据屏幕内容实时处理情况，通过预定义操作流程与通用操作前提，可以较好的处理问题
    下一阶段应该是训练流程模型，完成更为复杂的定制任务，使用GPT3.5-API进一步提升事物处理能力

# 开发流程

    Ctrl+R 替换文件内文本

    强行停止快捷键 Ctrl+Alt+K

    使用管理员方式打开PyCharm的WindowsAi项目与MyOCR项目、VMWare虚拟机，打开Windows11模拟环境
    打开Anaconda Prompt命令终端 
        切换Conda环境
            conda activate python38
        切换到开发目录 
            cd C:\Users\USER\PycharmProjects\WindowsAI\Dir_New\Program
        打包程序 pyinstaller --onefile main.py | pyinstaller --specpath=outputs/ --onefile main.py
            pyinstaller --onefile main.py
            pyinstaller --onefile GOTO_MAIN.py
            pyinstaller --onefile MyPyQt.py
            使用以下代码打包时会附带图像资源并且不会有黑色CMD窗口
            pyinstaller --onefile --add-data "e6e6e6_bot.png;." --add-data "e6e6e6_user.png;." --windowed MyPyQt.py
        如果打包很快那绝对是出问题了，终止了

        conda activate python38
        cd C:\Users\USER\PycharmProjects\WindowsAI\Dir_New\Program \
        pyinstaller --onefile main.py

    直接将打包程序粘贴到虚拟机中，并使用管理员方式打开

    使用函数获取打开应用程序的名称，可以实现代码打开关闭

    使用NLP微调把用户的输入转化为具体某项操作，再由操作名称进行输出

# 经验

    使用窗口名称检测可以避免使用OCR，提高稳定性
    
    下载操作是会阻塞线程的

    无法复制到虚拟机就重新生成一个

    关闭程序的方法
        temp = run_cmd('''wmic process where "name='Chrome.exe'" delete''').stdout  # 可以关闭浏览器

        app = application.Application() # 启动应用程序对象
        app.connect(path="chrome.exe")# 连接到 Chrome 进程
        chrome_window = app.top_window()# 找到 Chrome 的主窗口
        chrome_window.close()  # 点击关闭按钮

        # 这个需要先切换焦点
        # 获取 Chrome 窗口的位置和大小
        chrome_window = pyautogui.getWindowsWithTitle("Google Chrome")[0]
        # 计算关闭按钮的位置（大致在右上角）
        close_button_x = chrome_window.left + chrome_window.width - 15
        close_button_y = chrome_window.top + 15
        # 移动鼠标并点击关闭按钮
        pyautogui.click(close_button_x, close_button_y)

    操作应该保持原子性，一条里面应该只有一次点击实现
    不一定非得用虚拟机嘛，这样就方便多了
    GPT YYDS, OPENAI YYDS 感觉官网就是不错，历史记忆可以很长很长
    录屏软件可以隐藏鼠标。。。
    点击速度最快一秒钟，应该是代码的原因
    点击函数出问题可以直接传入坐标测试，而非使用OCR
    本地是可以识别到较小的文字的，虚拟机有时会出问题，如打开文件无法检测
    注意修改后更新数据库再打包程序
    OCR是模糊搜搜还是精准搜索——精准搜索，所以理论上我得填优化后的字符串，但是这样很麻烦
    我明明更新数据库了，为什么没有用呢——好像数据库还不能动态调整，因为pyinstaller好像是固定的XD
    OCR过时问题，有时候运行中都会无法连接，会导致运行变慢——注意OCR连接即可
    做新的自动化时还是要录屏，这样好回顾效果
    怎么数据库又连不上了——同样是因为网络原因
    怎么虚拟机又没网了——没网影响吗——重启解决不了问题的话就换NAT连接——尝试连接手机热点——还是不行——重启主机就好了，看来重启还真能解决99%的问题
    Windows系统快捷键: https://baike.baidu.com/item/Windows%E5%BF%AB%E6%8D%B7%E9%94%AE%E5%A4%A7%E5%85%A8/407192
    Kimi API https://platform.moonshot.cn/docs/intro#%E4%B8%BB%E8%A6%81%E6%A6%82%E5%BF%B5
    如果已经安装QQ了，再次安装不是出问题了吗，我应该先检测是否已安装QQ，如果安装了就直接启动 is_exe_exist(exe_name)——我需要完整的预案体系
    为什么ocr时就变成 知我默认了。。。。我是不是应该实时绘制ocr识别结果呢——其实放大图像就好了
    很多时候一个方法看似能解决问题却不是最优解，我们要避免这样的情况发生
    我现在做一遍，就能给无数电脑做无数遍
    虚拟机没网是什么情况，麻了——重启笔记本就好了
    文字加位置也是一种信息，但现在还没用到
    find_icon函数在Microoperation.py里

    # 启动MySQL
    net start mysql84(管理员模式进入——win cmd 以管理员方式运行)
    net stop mysql84
    mysql -uroot -p
        000000
    # 更改运行地址
    在my.init的mysqld下面添加一行 bind-address = 0.0.0.0

    每个项目都应该在至少3台电脑上一次性测试成功才能发行

# 其他

    如果拿不到融资就想办法做好产品给同学用，花钱做新闻

