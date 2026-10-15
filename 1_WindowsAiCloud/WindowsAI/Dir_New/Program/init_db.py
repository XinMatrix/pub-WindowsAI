from dataclasses import dataclass
from typing import List
from config import db

db.drop_table('tasks')  # 清空表
db.create_table()  # 重建表


@dataclass
class ID:  # 不要使用boolean、int、直接使用str方便又好用
    depend: str  # 检测依据
    action: str  # 动作行为


@dataclass
class MDS:
    name: str
    actions: List[ID]


def insert_data(temp_task_name, action):
    db.insert(temp_task_name, action.depend, action.action)


if __name__ == '__main__':

    # start表示第一条，可以不检测
    start = 'WindowsAi'  # 第一条不需要检测
    sign = 'WindowsAi特殊标识符'

    # 次级封装
    # 暂时不适用通用检测，因为这往往涉及多个操作，后期再说
    # MDS('通用检测',
    #     [ID('建议的应用->照片->始终->仅一次', 'CLICK_TEXT(照片)->CLICK_TEXT(仅一次)', '0'),
    #      ID("选择一个应用以打开此'https'链接", 'KEY(ENTER)', '0')]),

    data_0 = [  # 零级封装——系统相关操作，直接代码实现

        # Start Depends on OCR
        MDS('获取所有WIFI密码', [ID('', 'FUN(GET_WIFI_PASSWORD)->FINISH()')]),  # 已测试 2024-7-26
        # TODO 新增系统信息，如CPU、内存、硬盘、网络、系统版本等
        # 使用数据计入Config文件
        # 此类信息计入Outputs

    ]

    # 这里还没有删除安装包
    data_1 = [  # 一级封装，原子类操作

        # 很怪哎，明明没有显示 WindowsAi 却自动执行了
        MDS('关闭用户帐户控制',  # 已测试 2024-7-29 Hyper-V ——不具备FOCUS特性，所以只能使用OCR
            [ID('', 'OPEN_SYSTEM(UserAccountControlSettings)->SELECT_OCR()'),  # 修改了，不需要加后缀
             ID('OCR(出现以下情况时始终通知我)', 'KEY(TAB)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'),
             ID('OCR(仅当应用尝试更改我的计算机时通知我%)', 'KEY(TAB)->KEY(DOWN)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'),
             ID('OCR(仅当应用尝试更改计算机时通知我不降低桌面亮度)', 'KEY(TAB)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'),
             ID('OCR(出现以下情况时始终不要通知我%)', 'KEY(ESC)->FINISH()')]),  # 忘记更新数据库了哈哈

        MDS('恢复用户帐户控制',  # 已测试 2024-7-29 Hyper-V
            [ID('', 'OPEN_SYSTEM(UserAccountControlSettings)->SELECT_OCR()'),  # 这里怎么还写了个FINISH
             ID('OCR(出现以下情况时始终通知我)', 'KEY(TAB)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'),
             ID('OCR(仅当应用尝试更改我的计算机时通知我%)', 'KEY(ESC)->FINISH()'),
             ID('OCR(仅当应用尝试更改计算机时通知我不降低桌面亮度)', 'KEY(TAB)->KEY(UP)->KEY(TAB)->KEY(ENTER)->FINISH()'),
             ID('OCR(出现以下情况时始终不要通知我%)', 'KEY(TAB)->KEY(UP)->KEY(UP)->KEY(TAB)->KEY(ENTER)->FINISH()')]),

        MDS('下载并安装Chrome',  # 已测试 2024-7-29 Hyper-V
            [ID('', 'DOWNLOAD(ChromeSetup.exe)->OPEN_DOWNLOADED(ChromeSetup.exe)->SET_FOCUS(Google Chrome)->FINISH()')]),

        MDS('卸载Chrome',  # 已测试 2024-7-29 Hyper-V
            [ID('',
                'OPEN_SYSTEM(ProgramAndFunction)->CLOSE_WINDOWS(Chrome.exe)->SET_FOCUS(程序和功能)->KEY(TAB)->KEY(TAB)->KEY('
                'TAB)->KEY(TAB)->INPUT(Google Chrome)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY('
                'DOWN)->KEY(UP)->KEY(ALT)->KEY(U)->SLEEP(2)->KEY(ENTER)->FINISH()'),  # 这里没有使用OCR是因为这个比较稳定，不太需要
             ]),

        MDS('下载并安装Python3.11.9-amd64',  # 已测试 2024-7-29 Hyper-V
            [ID('',
                'DOWNLOAD(python-3.11.9-amd64.exe)->OPEN_DOWNLOADED(python-3.11.9-amd64.exe)->SET_FOCUS(Python 3.11.9 (64-bit) '
                'Setup)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(SPACE)->KEY(UP)->KEY(UP)->KEY(UP)->KEY(ENTER)->WAIT_OCR(Setup was '
                'successful)->SET_FOCUS(Python 3.11.9 (64-bit) Setup)->KEY(DOWN)->KEY(SPACE)->FINISH()'),
             ]),

        # 这个后期可以使用自己的项目集，给出示例和基本开发流程
        MDS('下载并安装Pycharm-community-2024.1.4',  # 已测试 2024-7-29 Hyper-V
            [ID('',
                'DOWNLOAD(pycharm-community-2024.1.4.exe)->OPEN_DOWNLOADED(pycharm-community-2024.1.4.exe)->SET_FOCUS(PyCharm '
                'Community Edition 安装)->KEY(ENTER)->INPUT_DOWNLOAD(MyPyCharm)->KEY(ENTER)->KEY(ENTER)->KEY(ENTER)->WAIT_OCR('
                '%运行%)->SET_FOCUS(PyCharm Community Edition 安装)->KEY(SPACE)->KEY(ENTER)->SET_FOCUS(PyCharm 用户协议)->KEY('
                'TAB)->KEY(SPACE)->KEY(SPACE)->SLEEP(0.5)->KEY(TAB)->KEY(TAB)->KEY(SPACE)->FINISH()'),
             ]),

        # 新建项目里面其实蕴含了新建文件的操作——分解，要不要算二级封装呢
        # 内联参数怎么确定，文件重名问题怎么办
        # 项目名称好像还是有问题，要不要用OCR呢，怎么就变Python示例项目了
        MDS('PyCharm新建示例项目',  # 已测试 2024-7-29 Hyper-V
            [ID('',
                'OPEN_INSTALLED(PyCharm)->SET_FOCUS(PyCharm)->KEY(SPACE)->SLEEP(1)->KEY(TAB)->INPUT('
                'NewProject)->KEY(TAB)->INPUT_PROJECT(PyCharmProject)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY('
                'TAB)->KEY(SPACE)->SET_FOCUS(NewProject)->HOTKEY(WIN+UP)->HOTKEY(ALT+INSERT)->KEY('
                'DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(ENTER)->INPUT(main)->KEY(ENTER)->FINISH()'),
             ]),

    ]

    data_2 = [  # 二级封装——前期只是简单的复制，后期再考虑深度融合，甚至直接GPT训练生成，不需要改

        MDS('配置YOLOv8开发环境',
            # 开始，下载安装Python3.11.9-amd64
            [ID('',
                'DOWNLOAD(python-3.11.9-amd64.exe)->OPEN_DOWNLOADED(python-3.11.9-amd64.exe)->SET_FOCUS(Python 3.11.9 (64-bit) '
                'Setup)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(SPACE)->KEY(UP)->KEY(UP)->KEY(UP)->KEY(ENTER)->WAIT_OCR(Setup was '
                'successful)->SET_FOCUS(Python 3.11.9 (64-bit) Setup)->KEY(DOWN)->KEY(SPACE)->GOTO(1)'),
             # 下载安装pycharm-community-2024.1.4
             ID('1',
                'DOWNLOAD(pycharm-community-2024.1.4.exe)->OPEN_DOWNLOADED(pycharm-community-2024.1.4.exe)->SET_FOCUS(PyCharm '
                'Community Edition 安装)->KEY(ENTER)->INPUT_DOWNLOAD(MyPyCharm)->KEY(ENTER)->KEY(ENTER)->KEY(ENTER)->WAIT_OCR('
                '%运行%)->SET_FOCUS(PyCharm Community Edition 安装)->KEY(SPACE)->KEY(ENTER)->SET_FOCUS(PyCharm 用户协议)->KEY('
                'TAB)->KEY(SPACE)->KEY(SPACE)->SLEEP(0.5)->KEY(TAB)->KEY(TAB)->KEY(SPACE)->GOTO(2)'),
             # 打开项目 YOLOv8_Sample.zip，自动打开 README.md 文件
             ID('2',
                'DOWNLOAD(Sample_YOLOv8.zip)->MOVE_TO_PROJECT(Sample_YOLOv8)->OPEN_INSTALLED(PyCharm)->SET_FOCUS('  # 这里是第一次安装
                'PyCharm)->KEY(TAB)->KEY(SPACE)->SLEEP(1)->INPUT_PROJECT(Sample_YOLOv8)->KEY(TAB)->KEY(TAB)->KEY('
                'TAB)->KEY(SPACE)->SLEEP(0.5)->KEY(SPACE)->SLEEP(1)->HOTKEY(WIN+UP)->GOTO(3)'),
             # 添加虚拟环境解释器
             ID('3',  # 使用WAIT_OCR_END(Show all) 还有点问题，因为这个文字区分度不明显，不知道能不能用进度条，连续两次三秒间隔进度条都没有就好了
                'SLEEP(10)->HOTKEY(CTRL+ALT+S)->SLEEP(3)->INPUT(Python Interpreter)->SLEEP(1)->KEY(TAB)->KEY(TAB)->KEY('
                'TAB)->KEY(ENTER)->KEY(ENTER)->SLEEP(1)->KEY(ENTER)->WAIT_OCR_END(Creating Virtual Environment)->KEY('
                'TAB)->KEY(ENTER)->FINISH()')
             # TODO 现在的目标是让他编译完，然后运行代码
             # 运行代码，查找错误

             # TODO 运行项目查看情况
             # DOUBLE_KEY(SHIFT)->INPUT(1_install.py)->KEY(ENTER)
             # KEY(SHIFT+F10)
             # TODO 查看报错情况
             # 1_install.py 运行结束会显示 Process finished with exit code 0 但是此时可以包还没有index完成，不知道能不能看系统性能侧面反应有没有结束
             # 随后运行 2_train.py
             # 如果报错 c10 则安装 VC_redist.x64.exe -> ALT+A TAB ENTER OCR(完成) ALT+C
             # 如果报错 fbgemm.dll 则下载 libomp140.x86 64.dll 并放到指定目录下
             # IDEA 我应该是把c10的给人替换了，所以出问题

             # 其实还没弄好呢，用户现在还跑不起来

             # 包缺少问题——需要下载C++开发环境安装包
             # fbgemm.dll 问题
             # 运行进度为零问题

             # 模型评估能不能另起一个文件
             ]),

        # MDS('测试', [ID('', 'HOTKEY(WIN+D)->SLEEP(3)->SET_FOCUS(MyPyQt)->FINISH()')]),

        # Python入门教程(从小白到高级)(新版) http://t.csdnimg.cn/Ev9Qi
        MDS('配置Python入门环境',
            [ID('',  # 下载 Python
                'DOWNLOAD(python-3.11.9-amd64.exe)->OPEN_DOWNLOADED(python-3.11.9-amd64.exe)->SET_FOCUS(Python 3.11.9 (64-bit) '
                'Setup)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(SPACE)->KEY(UP)->KEY(UP)->KEY(UP)->KEY(ENTER)->WAIT_OCR(Setup was '
                'successful)->SET_FOCUS(Python 3.11.9 (64-bit) Setup)->KEY(DOWN)->KEY(SPACE)->GOTO(1)'),
             ID('1',  # 下载 PyCharm
                'DOWNLOAD(pycharm-community-2024.1.4.exe)->OPEN_DOWNLOADED(pycharm-community-2024.1.4.exe)->SET_FOCUS(PyCharm '
                'Community Edition 安装)->KEY(ENTER)->INPUT_DOWNLOAD(MyPyCharm)->KEY(ENTER)->KEY(ENTER)->KEY(ENTER)->WAIT_OCR('
                '%运行%)->SET_FOCUS(PyCharm Community Edition 安装)->KEY(SPACE)->KEY(ENTER)->SET_FOCUS(PyCharm 用户协议)->KEY('
                'TAB)->KEY(SPACE)->KEY(SPACE)->SLEEP(0.5)->KEY(TAB)->KEY(TAB)->KEY(SPACE)->GOTO(2)'),
             ID('2',  # 打开示例项目
                'DOWNLOAD(LearnPython.zip)->MOVE_TO_PROJECT(LearnPython)->OPEN_INSTALLED(PyCharm)->SET_FOCUS('
                'PyCharm)->KEY(TAB)->KEY(SPACE)->SLEEP(1)->INPUT_PROJECT(LearnPython)->KEY(TAB)->KEY(TAB)->KEY('
                'TAB)->KEY(SPACE)->SLEEP(0.5)->KEY(SPACE)->SLEEP(1)->HOTKEY(WIN+UP)->GOTO(3)'),
             ID('3',  # 配置虚拟环境
                'SLEEP(15)->HOTKEY(CTRL+ALT+S)->SLEEP(3)->INPUT(Python Interpreter)->SLEEP(1)->KEY(TAB)->KEY(TAB)->KEY('
                'TAB)->KEY(ENTER)->KEY(ENTER)->SLEEP(1)->KEY(ENTER)->WAIT_OCR_END(Creating Virtual Environment)->KEY('
                'TAB)->KEY(ENTER)->SLEEP(1)->SET_FOCUS(MyPyQt)->FINISH()'),
             ])

    ]

    data_new = [data_0, data_1, data_2]  # 在这里新增封装结构

    for data in data_new:
        for item in data:
            task_name = item.name
            action_set = item.actions
            for action_list in action_set:
                insert_data(task_name, action_list)

    print('Database Update Succeed!')  # 已验证，数据库可以动态更新，无需重新打包程序

    # tasks = db.query_all_tasks()
    # print(tasks)
    # result = db.find_tasks_by_task('关闭用户帐户控制')
    # print(len(result[0]), result)
