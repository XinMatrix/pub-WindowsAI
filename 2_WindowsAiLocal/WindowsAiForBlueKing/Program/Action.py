import re
import time

from Class_3_Input import press, input_content, input_param_content, hot_key, click_text_auto, click_text_all, click_text_up, \
    click_text_down, click_position, click_text_area, click_text_accuracy, input_project, input_download, click_right, \
    mouse_slide_down
from Class_4_Fun import _detect_language_status, start_inner_fun, delay, close_windows, once_ocr_zh, once_ocr_en, fuzzy_search, \
    _add_system_path
from Class_1_System import open_web, open_chrome, open_downloaded, open_installed, open_system, check_exe_exists, \
    switch_to_windows, switch_to_windows_full, _move_file, finish
from config import get_language, my_logger
from Data import temp_check


def start_action(results, action_string, user_message, temp_ocr_text=None, temp_ocr_position=None,
                 temp_ocr_accuracy_outputs=None):
    action_list = action_string.split('->')  # 还是用箭头吧，因为有些函数名字比较长，KeyWord也是
    for action in action_list:
        # time.sleep(0.25)  # 感觉0.25有点快了——还是在db里添加把，不然会越来越大
        time.sleep(0.5)  # 我不喜欢它笨笨的感觉，太慢了
        # 0.5谢谢，安全第一，安全第一

        # 按键
        if re.search(r"\bKEY\((.*?)\)", action):  # Nice 使用正则匹配减小工作量——加\b是为了完全有且仅有匹配模式
            target = re.search(r"\bKEY\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 按键')} : {action}")  # 原来要区分引号要
            press(target)

        # 输入内容
        elif re.search(r"\bINPUT\((.*?)\)", action):
            target = re.search(r"\bINPUT\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 输入')} : {action}")
            input_content(target)

        elif re.search(r"\bINPUT_PARAM\((.*?)\)", action):
            target = re.search(r"\bINPUT_PARAM\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 输入参数内容')} : {action}")
            input_param_content(target)

        # 组合键
        elif re.search(r"\bHOTKEY\((.*?)\)", action):
            target = re.search(r"\bHOTKEY\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 热键')} : {action}")
            keys = target.split('+')
            lowercase_keys = [key.lower() for key in keys]  # 转换为小写防止按住Shift模拟大小——这个是必要的
            hot_key(lowercase_keys)

        # OCR点击文本——自带文本语言检测与循环检测
        elif re.search(r"\bCLICK_TEXT\((.*?)\)", action):
            target = re.search(r"\bCLICK_TEXT\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 点击文本')} : {action}")
            click_text_auto(target)

        # 遍历并点击所有文本，用户操作文本与标题重复的情况，较为特殊，在蓝鲸开发创建项目时第一次遇到
        elif re.search(r"\bCLICK_TEXT_ALL\((.*?)\)", action):
            target = re.search(r"\bCLICK_TEXT_ALL\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 点击全部匹配文本')} : {action}")
            click_text_all(target)

        # OCR点击文本——向上偏移
        elif re.search(r"\bCLICK_TEXT_UP\((.*?)\)", action):
            target = re.search(r"\bCLICK_TEXT_UP\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 点击文本并向上偏移')} : {action}")
            click_text_up(target)

        # OCR点击文本——向下偏移
        elif re.search(r"\bCLICK_TEXT_DOWN\((.*?)\)", action):
            target = re.search(r"\bCLICK_TEXT_DOWN\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 点击文本并向下偏移')} : {action}")
            click_text_down(target)

        # 点击坐标
        elif re.search(r"\bCLICK_POS\((.*?)\)", action):
            target = re.search(r"\bCLICK_POS\((.*?)\)", action).group(1)  # 200,600
            my_logger.info(f"{get_language('匹配操作 点击坐标')} : {action}")
            click_position(target)

        # FIXME 测试中 按区域点击
        elif re.search(r"\bCLICK_TEXT_AREA\((.*?)\)", action):
            # target = re.search(r"\bCLICK_TEXT_AREA\((.*?)\)", action).group(1)  # TODO 识别出两个参数
            target = re.search(r"\bCLICK_TEXT_AREA\((.*?),(.*?)\)", action)
            t1 = target.group(1)  # 区域程序名称
            t2 = target.group(2)  # 点击文字
            my_logger.info(f"{get_language('匹配操作 点击区域文本')} : {action}")
            click_text_area(t1, t2, temp_ocr_text, temp_ocr_position)

        # 点击精确文字
        elif re.search(r"\bCLICK_TEXT_ACCURACY\((.*?)\)", action):
            target = re.search(r"\bCLICK_TEXT_ACCURACY\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 点击精确文本')} : {action}")
            click_text_accuracy(target, temp_ocr_accuracy_outputs)

        # 使用默认浏览器打开网址
        elif re.search(r"\bWEB_BROWSER\((.*?)\)", action):
            target = re.search(r"\bWEB_BROWSER\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 打开浏览器')} : {action}")
            open_web(target)

        elif re.search(r"\bOPEN_CHROME\((.*?)\)", action):
            target = re.search(r"\bOPEN_CHROME\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 打开Chrome浏览器')} : {action}")
            open_chrome(target)

        # 精准搜索打开 MyWindowsAi/Downloads/ 下文件
        elif re.search(r"\bOPEN_DOWNLOADED\((.*?)\)", action):
            target = re.search(r"\bOPEN_DOWNLOADED\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 打开下载内容')} : {action}")
            open_downloaded(target)

        # 打开已安装程序，系统或 MyWindowsAi/Program/ 下程序
        elif re.search(r"\bOPEN_INSTALLED\((.*?)\)", action):  # 模糊匹配已安装程序
            target = re.search(r"\bOPEN_INSTALLED\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 打开安装程序')} : {action}")
            open_installed(target)

        # 打开系统程序，如用户帐户控制、程序和功能
        elif re.search(r"\bOPEN_SYSTEM\((.*?)\)", action):  # 打开系统程序
            target = re.search(r"\bOPEN_SYSTEM\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 打开系统程序')} : {action}")
            open_system(target)

        # FIXME 检查程序是否存在
        elif re.search(r"\bCHECK_EXE_EXIST\((.*?)\)", action):
            target = re.search(r"\bCHECK_EXE_EXIST\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 检查程序是否存在')} : {action}")
            check_exe_exists(target)

        # 设置程序焦点
        elif re.search(r"\bSET_FOCUS\((.*?)\)", action):  # 普通切换
            target = re.search(r"\bSET_FOCUS\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 设置焦点')} : {action}")
            check = True
            while check:
                time.sleep(1)
                check = switch_to_windows(target)  # 循环检测

        # 设置全屏焦点
        elif re.search(r"\bSET_FOCUS_FULL\((.*?)\)", action):  # 全屏切换——有点问题，Chrome安装和普通程序都会被打开隐藏
            target = re.search(r"\bSET_FOCUS_FULL\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 设置焦点并全屏')} : {action}")
            check = True
            while check:
                time.sleep(1)
                check = switch_to_windows_full(target)  # 循环检测

        # 执行函数，如获取WIFI密码，也可以是好玩
        elif re.search(r"\bFUN\((.*?)\)", action):
            target = re.search(r"\bFUN\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 执行函数')} : {action}")
            start_inner_fun(target)

        # 小睡一会
        elif re.search(r"\bSLEEP\((.*?)\)", action):
            target = re.search(r"\bSLEEP\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 睡眠')} : {action}")
            delay(target)

        # 关闭运行窗口/清理后台程序
        elif re.search(r"\bCLOSE_WINDOWS\((.*?)\)", action):
            target = re.search(r"\bCLOSE_WINDOWS\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 关闭程序窗口')} : {action}")
            close_windows(target)

        # TODO
        # 下载文件，默认保存在MyWindowsAi/Download目录下
        # elif re.search(r"\bDOWNLOAD\((.*?)\)", action):
        #     target = re.search(r"\bDOWNLOAD\((.*?)\)", action).group(1)
        #     my_logger.info(f"{get_language('匹配操作 下载内容')} : {action}")
        #     temp = download(target)  # download不见了
        #     if temp.endswith('.zip'):
        #         with zipfile.ZipFile(temp, 'r') as zip_ref:
        #             files = zip_ref.namelist()  # 获取压缩包内的文件列表
        #             for file in files:  # 原地解压文件
        #                 zip_ref.extract(file, os.path.dirname(temp))
        #         os.remove(temp)  # 解压完成后删除压缩包
        #         my_logger.info(f"{get_language('删除压缩包')} : {temp}")

        # 输入安装目录到 MyWindowsAi/Project/{target} 下
        elif re.search(r"\bINPUT_DOWNLOAD\((.*?)\)", action):  # 下载程序文件，默认保存在MyWindowsAi/Download目录下
            target = re.search(r"\bINPUT_DOWNLOAD\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 输入安装地址')} : {action}")
            input_download(target)

        # 输入项目目录到 MyWindowsAi/Project/{target} 下
        elif re.search(r"\bINPUT_PROJECT\((.*?)\)", action):
            target = re.search(r"\bINPUT_PROJECT\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 输入项目地址')} : {action}")
            input_project(target)

        elif re.search(r"\bGOTO\((.*?)\)", action):
            target = re.search(r"\bGOTO\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 跳转')} : {action}")
            # 先查找，再执行 Nice
            for y in results:  # 这个是必中的
                if y[0] == target:  # 这里需要修改，一直是这里报错，注意，将 2 改为 0 ， 将 3 改为 1
                    start_action(results, y[1], my_logger, user_message)
                    break

        # 循环OCR，并等待检测target
        elif re.search(r"\bWAIT_OCR\((.*?)\)", action):
            target = re.search(r"\bWAIT_OCR\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 等待文本出现')} : {action}")
            while True:
                time.sleep(1)
                language_result = _detect_language_status([target])
                if language_result == 'ZH':
                    ocr_outputs = once_ocr_zh()
                elif language_result == 'EN':
                    ocr_outputs = once_ocr_en()
                else:
                    raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
                if any(fuzzy_search(target, item['text']) for item in ocr_outputs):
                    break

        elif re.search(r"\bWAIT_OCR_END\((.*?)\)", action):
            target = re.search(r"\bWAIT_OCR_END\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 等待文本出现并消失')} : {action}")
            while True:  # 等待文本出现
                time.sleep(1)
                language_result = _detect_language_status([target])
                if language_result == 'ZH':
                    ocr_outputs = once_ocr_zh()
                elif language_result == 'EN':
                    ocr_outputs = once_ocr_en()
                else:
                    raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
                if any(fuzzy_search(target, item['text']) for item in ocr_outputs):
                    break
            while True:  # 等待文本消失
                time.sleep(1)
                language_result = _detect_language_status([target])
                if language_result == 'ZH':
                    ocr_outputs = once_ocr_zh()
                elif language_result == 'EN':
                    ocr_outputs = once_ocr_en()
                else:
                    raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
                if not any(fuzzy_search(target, item['text']) for item in ocr_outputs):
                    break

        # SELECT_OCR() 匹配数据库OCR 如 OCR(%ABC%)
        elif action == 'SELECT_OCR()':
            _Flag = True
            my_logger.info(f"{get_language('匹配操作 特征文本转操作')} : {action}")
            target_list = []
            action_list = []
            for y in results:  # 这个是必中的
                if re.search(r"\bOCR\((.*?)\)", y[0]):
                    target = re.search(r"\bOCR\((.*?)\)", y[0]).group(1)
                    # TODO 判断 target 语言类型
                    target_list.append(target)
                    action_list.append(y[1])
            while _Flag:
                time.sleep(1)
                language_result = _detect_language_status(target_list)
                if language_result == 'ZH':
                    ocr_outputs = once_ocr_zh()
                elif language_result == 'EN':
                    ocr_outputs = once_ocr_en()
                else:
                    raise ValueError(f"未知语言类型/未统一语言类型 : {language_result}")
                for x in ocr_outputs:
                    for index, y in enumerate(target_list):
                        if fuzzy_search(y, x['text']):
                            _Flag = False
                            start_action(results, action_list[index], my_logger, user_message)

        elif re.search(r"\bMOVE_FILE\((.*?)\)", action):
            target = re.search(r"\bMOVE_FILE\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 移动文件')} : {action}")
            _move_file(target)

        elif re.search(r"\bADD_SYSTEM_PATH\((.*?)\)", action):
            target = re.search(r"\bADD_SYSTEM_PATH\((.*?)\)", action).group(1)
            my_logger.info(f"{get_language('匹配操作 添加系统路径')} : {action}")
            _add_system_path(target)

        # -----------------------------------

        # FIXME 右键
        elif action == 'CLICK_RIGHT()':  # 无参函数
            my_logger.info(f"{get_language('匹配操作 右键')} : {action}")
            click_right()

        # 鼠标向下滑动
        elif action == 'MOUSE_SLIDE_DOWN()':  # 无参函数
            my_logger.info(f"{get_language('匹配操作 向下滑动鼠标')} : {action}")
            mouse_slide_down()

        elif action == 'FINISH()':  # 无参函数
            my_logger.info(f"{get_language('匹配操作 程序结束')} : {action}")
            finish()
            # 我想让它执行完成后返回聊天内容
            global temp_check
            temp_check['Value'] = True

        else:
            text = f"{get_language('操作未定义')} : {action}"
            my_logger.critical(text)
            raise ModuleNotFoundError(text)
            # return  # return会无法显示错误信息，所以还是用raise吧
