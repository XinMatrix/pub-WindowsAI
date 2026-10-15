local_data = [

    # TODO 准备进行全流程测试，准备说明文件与打包

    # 顺序使用，使用前请移动 MyWindowsAi文件夹 到桌面，并打开 Config/BG_WindowsAi.png 图片查看是否正常
    # 1 需要手动点击确认
    # 3 需要保持网络畅通
    # 5 需要保持网络畅通 MySQL默认密码 000000
    # 8 需要 gitee 帐户 仓库名称为 WindowsAi-BlueKingProject-{gitee_user_name} 仓库介绍为 （WindowsAi自动配置）大数据平台及其应用课程实践，蓝鲸智云项目
    # 9 需要 gitee 帐户与密码 应用ID为 my-blue-king 应用名称为 蓝鲸智云大数据项目实践

    # 配置Hyper-V——需要提示用户重启电脑
    ['1', [['', 'FUN(START_HYPER_V)->FINISH()']]],

    # IDEA 以下操作应该在虚拟机中操作------------------------------------------------------------------------------------

    # 关闭用户帐户控制——需要提示用户手动点击确认
    ['2', [['', 'OPEN_SYSTEM(UserAccountControlSettings)->SELECT_OCR()'],
           ['OCR(%始终通知我%)', 'KEY(TAB)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
           ['OCR(%默认%)', 'KEY(TAB)->KEY(DOWN)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
           ['OCR(%桌面%)', 'KEY(TAB)->KEY(DOWN)->KEY(TAB)->KEY(ENTER)->FINISH()'],
           ['OCR(%始终不要通知我%)', 'KEY(ESC)->FINISH()']]],

    # 安装Chrome
    ['3', [['', 'OPEN_DOWNLOADED(ChromeSetup.exe)->SET_FOCUS(Google Chrome)->SLEEP(5)->KEY(TAB)->KEY(SPACE)->KEY(TAB)->KEY('
                'SPACE)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY(SPACE)->SET_FOCUS(WindowsAiChat)->FINISH()']]],

    # 安装Python
    ['4', [['', 'OPEN_DOWNLOADED(python-3.6.7-amd64.exe)->SET_FOCUS(Python 3.6.7 (64-bit) '
                'Setup)->KEY(DOWN)->KEY(DOWN)->KEY(DOWN)->KEY(SPACE)->KEY(UP)->KEY(UP)->KEY(UP)->KEY(ENTER)->WAIT_OCR(%Setup was '
                'successful%)->SET_FOCUS(Python 3.6.7 (64-bit) Setup)->KEY(DOWN)->KEY(SPACE)->SET_FOCUS(WindowsAiChat)->FINISH()']]],

    # 安装MySQL——密码 000000
    # 思考，如果下载太快WAIT_OCR_END()可能会出问题，因为检测不到，如果以后遇到这个问题就应该换一种检测方法——果然，WAIT_OCR_END出问题了
    ['5', [['', 'OPEN_DOWNLOADED(mysql-installer-community-5.7.39.0.msi)->WAIT_OCR(%Mandatory%)->KEY(LEFT)->KEY('
                'SPACE)->WAIT_OCR(%Client Only%)->HOTKEY(ALT+N)->SLEEP(1)->HOTKEY('
                'ALT+X)->WAIT_OCR(%SOFTWARE LICENSE TERMS%)->FUN('
                'CLICK_CENTER)->HOTKEY(ALT+A)->HOTKEY(ALT+I)->WAIT_OCR(%Setup Successful%)->HOTKEY(ALT+C)->WAIT_OCR('
                '%许可条款%)->FUN(CLICK_CENTER)->HOTKEY(ALT+A)->HOTKEY(ALT+I)->WAIT_OCR(%设置成功%)->FUN(CLICK_CENTER)->HOTKEY('
                'ALT+C)->SLEEP(1)->HOTKEY('
                'ALT+N)->HOTKEY(ALT+X)->WAIT_OCR_END(%Installing%)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->INPUT('
                '000000)->KEY('
                'TAB)->INPUT(000000)->SLEEP(3)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+X)->WAIT_OCR(%Click '
                r'Finish%)->HOTKEY(ALT+F)->HOTKEY(ALT+N)->HOTKEY(ALT+F)->ADD_SYSTEM_PATH(C:\Program Files\MySQL\MySQL Server '
                r'5.7\bin)->SET_FOCUS(WindowsAiChat)->FINISH()']]],

    # 安装Git
    ['6', [['', 'OPEN_DOWNLOADED(Git-2.46.0-64-bit.exe)->SLEEP(3)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY('
                'ALT+N)->HOTKEY('
                'ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY('
                'ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+N)->HOTKEY(ALT+I)->WAIT_OCR(%Completing the Git Setup Wizard%)->HOTKEY('
                'ALT+F)->SLEEP(1)->KEY(ESC)->SET_FOCUS(WindowsAiChat)->FINISH()']]],  # 也可以点击仅一次，或直接空格，还是要有ESC的——打开浏览器

    # 创建git仓库
    # WindowsAi-BlueKingProject 这个是我定的
    ['7', [['', 'OPEN_CHROME(gitee.com/projects/new)->HOTKEY(CTRL+0)->CLICK_TEXT_DOWN(%仓库名称%,40)->INPUT('
                'MyBlueKingProject)->SLEEP(1)->CLICK_TEXT(%简短的语言%)->INPUT('
                '大数据平台及其应用课程实践，蓝鲸智云项目)->CLICK_TEXT(%仓库成员%)->CLICK_TEXT('
                '创建)->SET_FOCUS(WindowsAiChat)->FINISH()']]],

    # 创建蓝鲸项目
    # ce.bktencent.com->bkpaas.ce.bktencent.com->bkpaas.ce.bktencent.com/developer-center/app/create
    ['8', [['', 'OPEN_CHROME(bkpaas.ce.bktencent.com/developer-center/app/create)->CLICK_TEXT(%请输入%)->INPUT_PARAM({'
                'BKPAAS_APP_ID})->KEY('
                'TAB)->INPUT_PARAM({BKPAAS_APP_NAME})->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY('
                'TAB)->INPUT_PARAM('
                'https://gitee.com/{gitee_user_name}/my-blue-king-project)->KEY(TAB)->INPUT_PARAM({'
                'gitee_user_name})->KEY(TAB)->INPUT_PARAM({gitee_user_password})->KEY(TAB)->KEY(TAB)->CLICK_TEXT('
                '%下一步%)->CLICK_TEXT_ALL(创建应用)->SET_FOCUS(WindowsAiChat)->FINISH()']]],
    # 创建应用 的情况比较特殊，应该点击所有的创建应用

    # 安装配置PyCharm开发环境
    ['9', [['', 'OPEN_DOWNLOADED(pycharm-community-2024.2.exe)->SET_FOCUS(PyCharm '
                'Community Edition 安装)->KEY(ENTER)->INPUT_DOWNLOAD(MyPyCharm)->KEY(ENTER)->KEY(ENTER)->KEY(ENTER)->WAIT_OCR('
                '%运行%)->SET_FOCUS(PyCharm Community Edition 安装)->KEY(SPACE)->KEY(ENTER)->SET_FOCUS(PyCharm 用户协议)->KEY('
                'TAB)->KEY(SPACE)->KEY(SPACE)->SLEEP(0.5)->KEY(TAB)->KEY(TAB)->KEY(SPACE)->GOTO(1)'],
           # 打开示例项目
           ['1', 'OPEN_INSTALLED(PyCharm)->SET_FOCUS('
                 'PyCharm)->KEY(TAB)->KEY(SPACE)->SLEEP(1)->INPUT_PROJECT(BlueKingProject)->KEY(TAB)->KEY(TAB)->KEY('
                 'TAB)->KEY(SPACE)->SLEEP(0.5)->KEY(SPACE)->GOTO(2)'],
           # 配置虚拟环境
           ['2', 'SLEEP(15)->KEY(ESC)->HOTKEY(WIN+UP)->HOTKEY(CTRL+ALT+S)->SLEEP(3)->INPUT(Python Interpreter)->SLEEP(1)->KEY('
                 'TAB)->KEY('
                 'TAB)->KEY(TAB)->KEY(ENTER)->KEY(ENTER)->SLEEP(1)->KEY(ENTER)->WAIT_OCR_END(Creating Virtual Environment)->KEY('
                 'TAB)->KEY(ENTER)->GOTO(3)'],
           # 新增Git上传，等加载好了再上传代码，或者放到最后
           ['3', 'WAIT_OCR(%Credential%)->INPUT_PARAM({gitee_user_name})->KEY(TAB)->INPUT_PARAM({gitee_user_password})->KEY('
                 'ENTER)->GOTO(4)'],
           # 蓝鲸示例项目配置
           # 完成后让用户运行下载文件
           ['4', 'FUN(BK_REPLACE_TEXT)->SLEEP(1)->FUN(BK_INIT_DB)->FUN(ADD_HOST)->SLEEP(60)->FUN(INIT_GIT)->SET_FOCUS('
                 'WindowsAiChat)->FINISH()']
           ]],
    # ['4', 'FUN(BK_REPLACE_TEXT)->SLEEP(1)->SET_FOCUS(BlueKingProject)->FUN(BK_INIT_DB)->SLEEP(1)->HOTKEY('
    #       'ALT+F12)->INPUT(python manage.py migrate)->KEY(ENTER)->FUN(ADD_HOST)->SET_FOCUS(WindowsAi)->FINISH()']
    # ]],
]
