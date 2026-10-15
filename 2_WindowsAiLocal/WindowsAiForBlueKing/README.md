# WindowsAi CPU 本地版——使用边缘计算

## 打包过程

    测试打包

    E:
    cd E:\WindowsAiForBlueKing\Program
    conda activate WindowsAiLocal
    pyinstaller --onefile --add-data "e6e6e6_bot.png;." --add-data "e6e6e6_user.png;." --hidden-import "requests" --hidden-import "tqdm" --hidden-import "imghdr" --hidden-import "imgaug" --hidden-import "pyclipper" --collect-data "paddle" --collect-all "paddleocr" --collect-all "scipy" --collect-all "lmdb" --collect-all "tqdm" MyPyQt.py

    加密打包

    E:
    cd E:\WindowsAiForBlueKing\Program
    conda activate WindowsAiLocal
    C:\Users\USER\.conda\envs\python38\Scripts\pyarmor.exe obfuscate -O build/srv -r E:\WindowsAiForBlueKing\Program
    pyinstaller --paths=./build/srv/ --clean --onefile --add-data "e6e6e6_bot.png;." --add-data "e6e6e6_user.png;." --hidden-import "requests" --hidden-import "tqdm" --hidden-import "imghdr" --hidden-import "imgaug" --hidden-import "pyclipper" --collect-data "paddle" --collect-all "paddleocr" --collect-all "scipy" --collect-all "lmdb" --collect-all "tqdm" MyPyQt.py

# Hyper-V——原来通过命令就可以启动Hyper-V。。。。。。。。。。——以后还是优先考虑命令形式吧

    Win+X A ->
    Get-Service -Name vmms
    Start-Service -Name vmms

# 使用过程

    【电脑成精啦，会自己动！WindowsAi自动配置腾讯蓝鲸SaaS开发环境】 https://www.bilibili.com/video/BV1f5pieUEhm/?share_source=copy_web

    信息：https://docs.qq.com/sheet/DYVpoRHdGendabFlv?tab=BB08J2

    Gitee新建仓库出问题，没有往下移动（每个人屏幕大小不一致）
    虚拟机改为强烈建议
    注意区分PyCharm安装和次配置

    好麻烦，还是直接下载到一块吧，同时分离出Hyper-V程序，然后通过某种方式传输到虚拟机中，这样最方便
    测试时假设Hyper-V已设置，说到底Hyper-V其实是可选的，用完要重启

    第一步：下载 程序 与 ISO镜像，创建虚拟机
    第二步：下载 程序 与 WindowsAi蓝鲸开发包
    第三步：将开发包中的 MyWindowsAi 放置到桌面上
    第四步：打开

    能做备份就做备份虚拟机，不要害怕空间不够
    注意 INPUT_PARAM 和 INPUT 的区别
    修改后重新加密再打包，不要直接打包，没用
    优先考虑代码命令而非 CLICK_TEXT
    先单独测试函数，再集成测试

# TODO

    问题：
    1. 信任度可能不高，应该清楚的说明功能
    2. 需求认知不足，他们可能没有意识到有多耗时（或者手动配置能更好的理解过程）
    3. 缺乏反馈渠道

    每次运行前仔细检查新写的代码，特别是函数部分，不那么直观，容易出错

    ALT+0 全选提交即可？为什么git会报错，为什么没有直接raise？为什么db还是没有成功？
    git报错是因为url不对，db成功了，但是没输出

    注意时刻优化执行策略，同步记录虚拟机状态

    明天测试最后一次，记得重启，程序，真的，明天测最后一遍

    WindowsAiChat

    写一个Flask文件传输服务器

    我怎么突然感觉应该把文件放到一块了，不然好像引用有些问题——用其他方法

    最后把蓝鲸的 MyFunClass 改到 WindowsAoLocal 即可

    LayoutLM——文档理解新时代

    应该让用户先配置Hyper-V虚拟机，然后再在虚拟机里配置开发环境

    根本性问题——可读性不强，能不能做一个开发IDE，既有提示又有较强可视化效果？

# FINISHED

    新增文件内容读取
    OCR语言检测与系统没有关系，仅仅是针对文本情况——更新了OCR识别方式，新增了函数，详见 OCR.py MyFunClass.py
    TODO!!! 转型为 后台服务器，Local发布时再测试本地化，不然工作量太大了，莫名其妙，改一次就要重启系统也太离谱了——直接从服务器拿数据就好了——好处是可以一次测完整个流程，不会被卡住
    他们怎么在虚拟机中传输文件？能不能创建一个共享文件夹？好像就是有点问题——先搜搜B站，不行再写程序

    为什么 git 还是 有问题。。。。。。。。。。。。——直接使用带账号验证的gitee指令
    不要KEY了，让用户自己输入吧，毕竟变麻烦了
    db出问题了，SCERET没有——SECRET真的很奇怪——先让用户重启吧
    应该告诉用户强制停止快捷键 Ctr+Alt+K
    Chrome默认搜索方式也给用户说一下吧
    拆开完先运行看看，不行就改为运行时导入——MyFunClass已拆解——很好，又要学Python加密打包了，或者把文件拆开
    WindowsAiChat
    程序要改名，不要用 Main.exe 容易重名
    PyCharm Gitee 启动！
    给bk加一个下载包的文件
    新增 BKPAAS_APP_ID 与 BKPAAS_APP_SECRET
    Chrome下载太慢了，直接进入虚拟机测试即可——中午和晚上网络会比较差，因为用网人多
    如果是 1 使用代码的话就不应该打开 WindowsAi 的 png 图片
    创建 Chrome 虚拟机并登录网页，直接测试第四个过程
    问题不会凭空产生，肯定是我修改了哪里，如 SET_FOCUS(Main) 问题
    18测试出现数组越界问题，纸箱命令，但是使用Powershell并没有问题，原因未知——有时候会报错，提醒用户多试几次就好了，真的——最终决定修改代码，多执行几次
    22时遇到问题，切换窗口时权限错误，不知道为什么，之前还没有SET_FOCUS(Main)——可能是还没结束就执行了
    化繁为简，不需要 SET_FOCUS(Main)
    原来修改用户帐户控制也有。。。。——不太行，权限问题很严重，看来涉及安全的就比较麻烦
    看来还是要搞两个OCR系统，指定 OCR_CH or OCR_EN——检测语言即可
    安装Git
    Hyper-V自由
