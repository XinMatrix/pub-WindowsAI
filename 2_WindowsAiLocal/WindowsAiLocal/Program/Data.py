from config import language

temp_check = {"Value": False}  # 这样可以长久记录变量

if language == 'zh':
    local_data = [
        # 获取所有WIFI密码
        ['0', [['', 'FUN(GET_WIFI_PASSWORD)->FINISH()']]],
        # 关闭用户帐户控制
        ['1',
         [['', 'OPEN_SYSTEM(UserAccountControlSettings)->SELECT_OCR()'],
          ['OCR(%始终通知我%)', 'KEY(TAB)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
          ['OCR(%默认%)', 'KEY(TAB)->KEY(DOWN)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
          ['OCR(%桌面%)', 'KEY(TAB)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
          ['OCR(%始终不要通知我%)', 'KEY(ESC)->FINISH()']]],
        # 恢复用户帐户控制
        ['2',
         [['', 'OPEN_SYSTEM(UserAccountControlSettings)->SELECT_OCR()'],
          ['OCR(%始终通知我%)', 'KEY(TAB)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
          ['OCR(%默认%)', 'KEY(ESC)->FINISH()'],
          ['OCR(%桌面%)', 'KEY(TAB)->KEY(UP)->KEY(TAB)->KEY(ENTER)->FINISH()'],
          ['OCR(%始终不要通知我%)', 'KEY(TAB)->KEY(UP)->KEY(UP)->KEY(TAB)->KEY(ENTER)->FINISH()']]],
        # 配置Python入门环境
        ['3',
         [['',  # 下载 Python
           'OPEN_DOWNLOADED(python-3.11.9-amd64.exe)->SET_FOCUS(Python 3.11.9 (64-bit) '
           'Setup)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(SPACE)->KEY(UP)->KEY(UP)->KEY(UP)->KEY(ENTER)->WAIT_OCR(Setup was '
           'successful)->SET_FOCUS(Python 3.11.9 (64-bit) Setup)->KEY(DOWN)->KEY(SPACE)->GOTO(1)'],
          ['1',  # 下载 PyCharm
           'OPEN_DOWNLOADED(pycharm-community-2024.2.exe)->SET_FOCUS(PyCharm '
           'Community Edition 安装)->KEY(ENTER)->INPUT_DOWNLOAD(MyPyCharm)->KEY(ENTER)->KEY(ENTER)->KEY(ENTER)->WAIT_OCR('
           '%运行%)->SET_FOCUS(PyCharm Community Edition 安装)->KEY(SPACE)->KEY(ENTER)->SET_FOCUS(PyCharm 用户协议)->KEY('
           'TAB)->KEY(SPACE)->KEY(SPACE)->SLEEP(0.5)->KEY(TAB)->KEY(TAB)->KEY(SPACE)->GOTO(2)'],
          ['2',  # 打开示例项目
           'OPEN_INSTALLED(PyCharm)->SET_FOCUS('
           'PyCharm)->KEY(TAB)->KEY(SPACE)->SLEEP(1)->INPUT_PROJECT(LearnPython)->KEY(TAB)->KEY(TAB)->KEY('
           'TAB)->KEY(SPACE)->SLEEP(0.5)->KEY(SPACE)->SLEEP(1)->HOTKEY(WIN+UP)->GOTO(3)'],
          ['3',  # 配置虚拟环境
           'SLEEP(15)->HOTKEY(CTRL+ALT+S)->SLEEP(3)->INPUT(Python Interpreter)->SLEEP(1)->KEY(TAB)->KEY(TAB)->KEY('
           'TAB)->KEY(ENTER)->KEY(ENTER)->SLEEP(1)->KEY(ENTER)->WAIT_OCR_END(Creating Virtual Environment)->KEY('
           'TAB)->KEY(ENTER)->SLEEP(1)->SET_FOCUS(Main)->FINISH()']]],
        # 配置Hyper-V环境
        ['4',
         [['',
           'FUN(CHECK_SYSTEM_VISION)->HOTKEY(WIN+Q)->SLEEP(1)->INPUT(启用或关闭 Windows 功能)->KEY(ENTER)->CLICK_TEXT(%Hyper-V%)->KEY('
           'SPACE)->KEY(TAB)->KEY(SPACE)->FINISH()'],
          ]],
        # 配置CUDA环境
        ['5',
         [['',  # 安装 CUDA Toolkit 12.6——这里需要使用中文，等等，是否可以直接检测协议内容——End User License Agreement
           'FUN(CHECK_SYSTEM_GPU)->OPEN_DOWNLOADED(cuda_12.6.0_560.76_windows.exe)->SET_FOCUS(cuda Setup Package)->KEY('
           'ENTER)->WAIT_OCR(%End User License Agreement%)->HOTKEY(ALT+A)->SLEEP(1)->HOTKEY(ALT+N)->CLICK_TEXT('
           '%understand%)->HOTKEY(Alt+N)->WAIT_OCR(Nsight Visual Studio Edition Summary)->HOTKEY(Alt+N)->KEY(ENTER)->GOTO(1)'],
          ['1',
           'MOVE_FILE(cudnn-windows-x86_64-8.9.7.29_cuda12-archive/include,C:/Program Files/NVIDIA GPU Computing '
           'Toolkit/CUDA/v12.6)->MOVE_FILE(cudnn-windows-x86_64-8.9.7.29_cuda12-archive/lib,C:/Program Files/NVIDIA GPU '
           'Computing Toolkit/CUDA/v12.6)->FINISH()']
          # 能不能想办法提高测试效率——还是有的，但是要谨慎
          ]],
        # 配置蓝鲸开发平台环境——任务量还挺大的其实
        # Hyper-V
        # Python 3.6.7
        # MySQL 5.7.39
        # Git
        # PyCharm
        # 创建git仓库
        # 创建蓝鲸项目——蓝鲸开发者中心
        # Next
        ['6',
         [['', ''],
          ['', ''],
          ]]
    ]
elif language == 'en':
    local_data = [
        # 因为没有国外系统连接WIFI，所以这个功能暂时没法测试
        # ['0', [['', 'FUN(GET_WIFI_PASSWORD)->FINISH()']]],  # 获取所有WIFI密码
        # 关闭用户帐户控制
        ['1',
         [['', 'OPEN_SYSTEM(UserAccountControlSettings)->SELECT_OCR()'],
          ['OCR(Always notify me when%)', 'KEY(TAB)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
          ['OCR(%default%)', 'KEY(TAB)->KEY(DOWN)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
          ['OCR(%dim%)', 'KEY(TAB)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
          ['OCR(Never notify me when%)', 'KEY(ESC)->FINISH()']]],
        # 恢复用户帐户控制
        ['2',
         [['', 'OPEN_SYSTEM(UserAccountControlSettings)->SELECT_OCR()'],
          ['OCR(Always notify me when%)', 'KEY(TAB)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
          ['OCR(%default%)', 'KEY(ESC)->FINISH()'],
          ['OCR(%dim%)', 'KEY(TAB)->KEY(UP)->KEY(TAB)->KEY(ENTER)->FINISH()'],
          ['OCR(Never notify me when%)', 'KEY(TAB)->KEY(UP)->KEY(UP)->KEY(TAB)->KEY(ENTER)->FINISH()']]],
        # 配置Python入门环境
        ['3',
         [['',  # 下载 Python
           'OPEN_DOWNLOADED(python-3.11.9-amd64.exe)->SET_FOCUS(Python 3.11.9 (64-bit) '
           'Setup)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(SPACE)->KEY(UP)->KEY(UP)->KEY(UP)->KEY(ENTER)->WAIT_OCR(Setup was '
           'successful)->SET_FOCUS(Python 3.11.9 (64-bit) Setup)->KEY(DOWN)->KEY(SPACE)->GOTO(1)'],
          ['1',  # 下载 PyCharm
           'OPEN_DOWNLOADED(pycharm-community-2024.2.exe)->SET_FOCUS(PyCharm '
           'Community Edition Setup)->KEY(ENTER)->INPUT_DOWNLOAD(MyPyCharm)->KEY(ENTER)->KEY(ENTER)->KEY(ENTER)->WAIT_OCR('
           'Click Finish%)->SET_FOCUS(PyCharm Community Edition Setup)->KEY(SPACE)->KEY(ENTER)->SET_FOCUS(PyCharm '
           'User Agreement)->KEY(TAB)->KEY(SPACE)->KEY(SPACE)->SLEEP(0.5)->KEY(TAB)->KEY(TAB)->KEY(SPACE)->GOTO(2)'],
          ['2',  # 打开示例项目
           'OPEN_INSTALLED(PyCharm)->SET_FOCUS('
           'PyCharm)->KEY(TAB)->KEY(SPACE)->SLEEP(1)->INPUT_PROJECT(LearnPython)->KEY(TAB)->KEY(TAB)->KEY('
           'TAB)->KEY(SPACE)->SLEEP(0.5)->KEY(SPACE)->SLEEP(1)->HOTKEY(WIN+UP)->GOTO(3)'],
          ['3',  # 配置虚拟环境
           'SLEEP(15)->HOTKEY(CTRL+ALT+S)->SLEEP(3)->INPUT(Python Interpreter)->SLEEP(1)->KEY(TAB)->KEY(TAB)->KEY('
           'TAB)->KEY(ENTER)->KEY(ENTER)->SLEEP(1)->KEY(ENTER)->WAIT_OCR_END(Creating Virtual Environment)->KEY('
           'TAB)->KEY(ENTER)->SLEEP(1)->SET_FOCUS(Main)->FINISH()']]],
        # 配置Hyper-V环境
        ['4',
         [['',  # 使用模糊匹配OCR更稳定
           'FUN(CHECK_SYSTEM_VISION)->HOTKEY(WIN+Q)->SLEEP(1)->INPUT(Turn Windows features on or off)->KEY(ENTER)->CLICK_TEXT('
           '%Hyper-V%)->KEY(SPACE)->KEY(TAB)->KEY(SPACE)->FINISH()'],
          ]],
        # 配置CUDA环境
        ['5',
         [['',  # 安装 CUDA Toolkit 12.6——这里需要使用中文，等等，是否可以直接检测协议内容——End User License Agreement
           'FUN(CHECK_SYSTEM_GPU)->OPEN_DOWNLOADED(cuda_12.6.0_560.76_windows.exe)->SET_FOCUS(cuda Setup Package)->KEY('
           'ENTER)->WAIT_OCR(%End User License Agreement%)->HOTKEY(ALT+A)->SLEEP(1)->HOTKEY(ALT+N)->CLICK_TEXT('
           '%understand%)->HOTKEY(Alt+N)->WAIT_OCR(Nsight Visual Studio Edition Summary)->HOTKEY(Alt+N)->KEY(ENTER)->GOTO(1)'],
          ['1',
           'MOVE_FILE(cudnn-windows-x86_64-8.9.7.29_cuda12-archive/include,C:/Program Files/NVIDIA GPU Computing '
           'Toolkit/CUDA/v12.6)->MOVE_FILE(cudnn-windows-x86_64-8.9.7.29_cuda12-archive/lib,C:/Program Files/NVIDIA GPU '
           'Computing Toolkit/CUDA/v12.6)->FINISH()']
          ]],
    ]
else:
    local_data = []

# CUDA - Windows 10 x64 配置——如果之前使用过请完全卸载CUDA

# 查看支持CUDA的GPU型号及其算力——已完成
#   https://developer.nvidia.cn/zh-cn/cuda-gpus

# 下载 CUDA Toolkit 12.6
#   https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local
# cuda Setup Package
# KEY(ENTER)
# NVIDIA 安装程序
# WAIT_OCR(%软件许可协议)
# KEY(ENTER)
# KEY(ENTER)
# CUDA Visual Studio Integration
# CLICK(understand) # 可能要安装VS
# HOTKEY(Alt+N)
# Nsight Visual Studio Edition Summary
# HOTKEY(Alt+N)
# KEY(ENTER)
# 安装完成，记得重启CMD

# 下载 cuDNN 8.9.7——已完成
#   https://developer.nvidia.cn/rdp/cudnn-archive

# 可选——用户可能不适用GeForce Experience
# 更新驱动版本（GeForce Experience）
# 驱动程序->检查更新文件->下载

# 安装 CUDA
# 直接安装即可——尝试，不行就按他的提示操作

# 安装 cuDNN
# 粘贴，还真的要这么搞

# CMD
# nvcc -V
# 环境变量已自动添加
