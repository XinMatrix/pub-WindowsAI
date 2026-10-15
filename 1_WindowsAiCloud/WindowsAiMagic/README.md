# WindowsAi Magic(而非Mini)

# Hyper-V——原来通过命令就可以启动Hyper-V。。。。。。。。。。——以后还是优先考虑命令形式吧

    Win+X A ->
    Get-Service -Name vmms
    Start-Service -Name vmms

# 说明

    https://api.v3.cm/panel

    function call的更进一步

    # cd 是为了调用代码时不用输入完整路径
    cd C:\Users\USER\Desktop\WindowsAi\1_WindowsAiCloud\WindowsAiMagic\Program
    C:\Users\USER\.conda\envs\python38\Scripts\pyarmor.exe obfuscate -O build/srv -r C:\Users\USER\Desktop\WindowsAi\1_WindowsAiCloud\WindowsAiMagic\Program
    pyinstaller --paths=./build/srv/ --clean --onefile --add-data "e6e6e6_bot.png;." --add-data "e6e6e6_user.png;." main.py

    新增WindowsAi Magic水印？

# 功能更新

    气泡长短问题
    换行问题，Shift+Enter

    企业面试题考察基础知识与企业特色技术相关问题

    写Linux版本？

    把这个文件夹下的视频分类，依据是视频名称相似度，输出文件大小并绘制饼图，C:\jianpianDownload
    视频压缩，要手动下载 ffmpeg-python与ffmpeg包并添加环境变量

    二段任务如何解决，先读取再识别

    B站搜视频脚本怎么写
    视频最后加一个正片可以提高完播率

    WindowsAi可以做一种新产品——让机器根据文字和目的选择点击屏幕上的文字——快速产生智能

    如何才能让GPT回答的代码一次就正确——如何准确的让用户说清楚自己想做什么，可以先给用户示例，让用户模仿是最快的方式

# 挑战常用功能——最后记得给用户一个示例文档，快速模仿，做成游戏一样的PK画面，对比时间，效率，便捷性，情节跌宕起伏，能吸引用户的注意力

## 欢迎页

    你可以做什么？
        我可以帮助你解决编程问题、生成代码、绘制图表以及提供各种技术支持。如果你有具体需求，请告诉我！

## 功能一：Excel表格处理

    生成Excel随机数据
        随机生成1000条数据，保存到文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Data.xlsx
    读取Excel表格
        读取文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Data.xlsx，并找出Category为A的数值，另存为Excel文件

    应用案例
        随机生成100条商品价格数据，保存到文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Data 2.xlsx
        随机生成100条商品价格数据，保存到文件 C:\Users\USER\Desktop\程序及相关素材\Sample Data.xlsx
        帮我计算Price一共是多少
        以一百为单位绘制饼图，看每个区间的占比

## 功能二：Word文档处理

    读取Word文档
        读取文件 C:\Users\USER\Desktop\WindowsAi Magic\视频脚本.docx，使用docx库
        解释内容
    识别Word表格
        读取文件中的表格 C:\Users\USER\Desktop\WindowsAi Magic功能测试\2025届预计毕业生图像信息采集时间安排及告知书.docx
        总结所有导员联系方式并生成Excel保存到桌面
    提取Word图片——可能会遗漏
        读取文件中的图片并新建文件夹另存到桌面 C:\Users\USER\Desktop\WindowsAi Magic功能测试\2025届预计毕业生图像信息采集时间安排及告知书.docx

## 功能三：PowerPoint演示文稿处理

    生成PPT，使用ChatPPT的API，看来聊天程序得新增选择了
        Ai未来的方向
    读取PPT文档
        读取文件内容 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Ai未来的方向.pptx
        解释它
    提取PPT图片——可能会遗漏，怎么办
        读取文件中的图片并新建文件夹另存到桌面 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Ai未来的方向.pptx

## 功能四：数据分析应用（神经网络、线性拟合等）——SK-Learn

    线性拟合
        随机生成一些线性拟合数据并保存到桌面
        随机生成一些线性拟合数据并保存到 C:\Users\USER\Desktop\程序及相关素材
        使用3D图查看它
        进行线性拟合测算并绘制结果

## 功能五：格式工厂文件格式转换

    移动 my_ffmpeg 文件夹到 C:\Program Files\
    添加Path系统环境变量 C:\Program Files\my_ffmpeg\bin

    （这个需要FFMPEG库，如同视频，下载地址：https://www.gyan.dev/ffmpeg/builds/ 下载教程：https://www.bilibili.com/video/BV1qw4m1d7hx/?share_source=copy_web
    （添加Path系统变量

    图片格式转换：WEBP、JPG、PNG、ICO、BMP、GIF、TIF、TGA、PDF（这里可以用RAP说的很快塑造娱乐氛围）
        将文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Photo.jpg 转化为以下格式并新建文件夹保存：WEBP、JPG、PNG、ICO、BMP、GIF、TIF、TGA、PDF
        将文件 C:\Users\USER\Desktop\程序及相关素材\原始图像素材.jpg 转化为以下格式并新建文件夹保存：WEBP、JPG、PNG、ICO、BMP、GIF、TIF、TGA、PDF
    音频格式转换：MP3、WAV、OGG、FLAC
        将文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Music.mp3 转化为以下格式并新建文件夹保存：MP3、WAV、OGG、FLAC
    文字生成音频
        文字转化为音频并保存到 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Text2Audio.mp3：你好，欢迎使用WindowsAi Magic
    音频转文字
        将音频 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Music.mp3 转化为文字并保存
    视频格式转换：MP4、AVI、MKV、WMV、MOV、FLV、RMVB、3GP、MPEG等
        将文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Video.mp4 转化为以下格式并新建文件夹保存：MP4、AVI、MKV、WMV、MOV、FLV、RMVB、3GP、MPEG
    视频提取音频
        将文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Video.mp4 提取音频并保存

## 功能六：Photoshop简单图像处理

    图像处理：裁剪、旋转、锐化、模糊、灰度、反色、浮雕、马赛克、对比度、饱和度、亮度
        将文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Photo.jpg 以以下形式处理并新建文件夹保存：裁剪、旋转、锐化、模糊、灰度、反色、浮雕、马赛克、对比度、饱和度、亮度
        将文件 C:\Users\USER\Desktop\程序及相关素材\原始图像素材.jpg 以以下形式处理并新建文件夹保存：裁剪、旋转、锐化、模糊、灰度、反色、浮雕、马赛克、对比度、饱和度、亮度

## 功能七：PremierePro简单视频处理

    视频裁剪
        将文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Video.mp4 裁剪为800*800并保存，使用ffmpeg库
    视频剪辑
        将文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Video.mp4 裁剪前一分钟视频，使用ffmpeg库
    视频拼接
        按顺序拼接视频，使用ffmpeg库：C:\Users\USER\Desktop\WindowsAi Magic功能测试\倒计时 3.mp4，C:\Users\USER\Desktop\WindowsAi Magic功能测试\倒计时 2.mp4，C:\Users\USER\Desktop\WindowsAi Magic功能测试\倒计时 1.mp4
        按顺序拼接视频并保存，使用ffmpeg库：C:\Users\USER\Desktop\程序及相关素材\原始视频合并素材 3.mp4，C:\Users\USER\Desktop\程序及相关素材\原始视频合并素材 2.mp4，C:\Users\USER\Desktop\程序及相关素材\原始视频合并素材 1.mp4
    视频压缩
        将文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Video.mp4 压缩为720p并保存，使用ffmpeg库
        将文件 C:\Users\USER\Desktop\程序及相关素材\原始视频素材.mp4 压缩为720p并保存，使用ffmpeg库
    视频添加字幕
        将文件 C:\Users\USER\Desktop\WindowsAi Magic功能测试\Sample Video.mp4 添加字幕‘这里是字幕’，持续三秒并保存，使用ffmpeg库

## 功能八：Windows系统设置

    查看修改环境变量
        查看系统Path环境变量并保存为Excel表格
        在系统环境变量Path中添加永久性路径，使用管理员身份：E:\jianpianDownload
    查看系统启动项
        输出系统启动项到Excel表格
    启用或关闭Windows功能
        打开启用或关闭Windows功能页面，使用subprocess
    连接MySQL服务
        连接本地MySQL，帐户root，密码000000，查看有哪些数据库

## 功能九：Windows系统文件批处理——感觉这个并不痛，可以往后放

    创建、修改、删除文件夹
        在桌面创建十个文件夹，名称分别是 你好呀
        改名为 你也是
        删除改名后的文件夹
    批量重命名文件
        按格式重命名文件夹下MP3文件，如 Music_01.mp3：C:\Users\USER\Desktop\MusicDownload
    批量压缩解压缩文件
        压缩文件夹：C:\Users\USER\Desktop\MusicDownload
        解压缩文件夹并删除原文件：C:\Users\USER\Desktop\MusicDownload_zip

## 其他功能

    读取、分析文档内容，快速总结

    MD文件转PDF，C:\Users\USER\Desktop\WindowsAi\1_WindowsAiCloud\WindowsAiMagic\README.md
    将Word转化为PDF C:\Users\USER\Desktop\YOUR_NAME 自动化测试岗 简历.docx

    我可以看插件有什么功能，我模仿

# 打包

    还要补充PaddleOCR——等等，是不是这个功能没必要，好像不常用，等用户说明吧，而且示例功能也没有
    cd C:\Users\USER\Desktop\WindowsAi\1_WindowsAiCloud\WindowsAiMagic\Program
    pyinstaller --onefile --add-data "e6e6e6_bot.png;." --add-data "e6e6e6_user.png;."  main.py

# TODO

    import matplotlib.pyplot as plt 为什么使用这个库会卡柱，没有多线程吗

    空结果问题

    虚拟机重新测试所有功能，要求给出精准语言描述，尝试去除Prompt定义，并绘制思维导图

    警告消息暂时没法去除

    新增系统空间占用排序

    定义工作场景，体现产品优势，有些广告也是这么做的

    虚拟机是为了测试包的可用性

    主要功能是excel处理，次要功能是其他办公软件，辅助功能是其他

    要不要开源WindowsAi
    新增简历编写功能，给用户详细示例——感觉好像有点难
    自动发货平台很方便

    给一个说明PDF或者Word
    建议非必要时重置对话，避免Token消耗过快
    
    后期可以把国外的API改为国内的，这样会方便很多——会员可以使用更多功能——面向API编程

    尝试接入图像音频视频处理，但是会贵一点，可以返回Token——有计费就可以做，整合到一起——很贵，慎用

    免费音乐：https://www.free-stock-music.com/
    生成字幕：https://jianwai.youdao.com/

    pyautogui.locateCenterOnScreen()——直接定位图标并点击

    能不能让Ai帮我改Bug并测试，使用OCR与GPT API——用户稳定性

    能不能训练模型识别图文教程
    把图文教程转化为描述性文字
    再把描述性文字转换为代码

    讲好用户故事，重塑开发方式

    应该使用会员制，参考绿钻、网易云会员，本质其实没变

    赚钱是目的，看看网页领先者是怎么做的
    WindowsAi Mini——针对办公场景小助手，处理办公三大件和一些小操作如处理图片、表格、文档等
    WindowsAi Local——针对计算机操作，如配置开发环境、安装驱动、安装软件等
    WindowsAi Mix——Local与Mini的混合，但是受众会很奇怪
    得出结论：应该先搞WindowsAi Mini，然后是WindowsAi Local，不搞WindowsAi Mix

# FINISH

    重新排序功能再测试
    为什么没有日志了——原来有输出，但是没有在控制台输出而已——加了一行代码，莫名其妙
    我想的是如果报错就应该重新输入Prompt与报错信息，尝试三次均失败后才确认失败，找到报错源，并内部重试——现在的问题是返回不正确
    更改环境变量后记得重启IDE，不然识别不到
    连续对话问题，新增NewChat按钮
    复制提示——点击按钮后文字变为已复制
    话说为什么要在虚拟机中测试呀，直接用不行吗？
    为什么执行就崩输出去除回车问题溃，还没有任何报错信息？——改为Exception处理，输出报错信息，之前是只检测语法错误
    新增Copy按键
    按上箭头可以重复之前的指令
    聊天框应该是深色，与背景区分
    发布的话就用Key和加密吧，虽然免费，但安全第一
    怎么直接输出代码运行成功了，我需要结果——还是得要 print
    去除 ```
    申请软著
    是否应该直接过滤 ``` 而非直接删除，确实，只截取```之间的内容，会稳定很多
    清空WindowsAI仓库，分为WindowsAiCloud（云端版）、WindowsAiLocal（本地版）、WindowsAiForBlueKing（蓝鲸定制）、WindowsAiBase（API版）
    Doc -> Docx?——默认给出识别转换
    为什么有时候报错 Document 没有定义呢——因为我打开了文件
    包是运行时下载还是提前下载好，因为用的其实就那么多——现在先提前下好吧，毕竟多一些不确定性是不好的，对，可以在用户运行前就统一下载好，打包为程序

# 更好的提示词工程

    提示词工程：https://mp.weixin.qq.com/s/OWLyGaokV8yRsrP1sMWOBw
    1. 引导模型得出解法
    2. 添加相关的语境
    3. 指令要明确
    4. 让它提供多种选项
    5. 设定角色
    6. 给它例子，不要光解释
    7. 声明想要的输出格式
    8. 实验，实验，再实验——LLM可以回应情绪性的信息。很多网友都发现，如果再指令中加入一些短语例如“深呼吸一下——这事对我的职业生涯很重要”或是“我会给好答案200块小费”等，可以提高回复的质量。

# 其他

    飞浆NB

    Ai最应该应用在现有成本巨大的耗费上

    NeRF——神经渲染方程，用于渲染复杂的3D物体，可以用于虚拟现实、增强现实等领域
    以后可能会从Transformer架构转为RNN架构，因为Transformer的计算量太大，而RNN的计算量很小，所以速度更快

    史巍：现在应该确认发展方向，案例cad读图工业需求，toc不好做不是刚需，营销要团队做个人不行

    国内开发者现状：懂技术不懂产业，懂产业不懂技术，鸡同鸭讲——我的话是 拿着最锋利的刀，却找不到心脏的位置，本质还是信息差

    别忘了我的域名，http://windowsai.top
