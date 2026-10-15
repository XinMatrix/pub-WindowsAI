temp_check = {"Value": False}  # 这样可以长久记录变量

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
    # Next
    ['6',
     [['', ''],
      ['', ''],
      ]]
]

