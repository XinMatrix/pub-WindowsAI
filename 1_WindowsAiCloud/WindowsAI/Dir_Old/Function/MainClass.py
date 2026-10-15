# 此类定义了WindowsAI所需所有代码(包括次级实现代码)
import os
import re
import threading
import time
import tkinter as tk
from dataclasses import dataclass
from typing import List

import pyautogui
import pyperclip
import requests
import win32api
from PIL import ImageGrab, Image

# INIT
ocr_sleep_time = 2  # 因为要考虑部分动画效果，所以延迟大点好 # 或者检测要点击的对象如果在移动则延迟一秒
crop_path = 'choose_crop.jpg'
screenshot_save_path = 'last_img.jpg'
ocr_url = 'http://127.0.0.1:5000/ocr'  # 注意，两个服务应该使用不同的端口
ocra_url = 'http://127.0.0.1:5001/ocr_accuracy'

# 程序的整体检测应该是每秒一次
windows_text = None
rect_window = None


@dataclass
class Method:
    operation: str = ''  # 操作类型
    text: str = ''  # 文本对象
    true: str = ''  # 为真时如何处理
    false: str = ''  # 为假时如何处理
    for_: str = ''  # 是否需要循环
    check_text: str = ''  # 检测文字(针对非强相关操作)
    alternative_operation: str = ''  # 备选方案(针对非强相关操作)
    alternative_text: str = ''  # 备选方案(针对非强相关操作)


@dataclass
class Solution:
    execution: str = ''  # 下载 # 关闭用户帐户控制
    target: str = ''  # QQ # (Empty)
    methods: List[Method] = ''  # 因为python是动态语言，所以可以先赋值字符串


class BaseClass:
    class DataStruct:

        @staticmethod
        def _get_parsed_value(string, param):
            tmp = re.search(rf"{param}='([^']+)'", string)
            return tmp.group(1) if tmp else ''

        @staticmethod
        def _get_parsed_class_value(string):
            # true和false要针对一下，因为他们的类型是操作
            # 这里三部分也要新增
            pattern = r"operation='(.*?)'.*text='(.*?)'(?:.*true='(.*?)')?(?:.*false='(.*?)')?(?:.*for_='(.*?)')?(?:.*check_text='(.*?)')?(?:.*alternative_operation='(.*?)')?(?:.*alternative_text='(.*?)')?"
            matches = re.search(pattern, string)
            if not matches:
                raise ValueError(f"Not Matched!\n{matches}")
            operation = matches.group(1) if matches.group(1) else ''
            text = matches.group(2) if matches.group(2) else ''
            true = matches.group(3) if matches.group(3) else ''
            false = matches.group(4) if matches.group(4) else ''
            for_ = matches.group(5) if matches.group(5) else ''
            check_text = matches.group(6) if matches.group(6) else ''
            alternative_operation = matches.group(7) if matches.group(7) else ''
            alternative_text = matches.group(8) if matches.group(8) else ''
            return Method(operation, text, true, false, for_, check_text, alternative_operation, alternative_text)

        @staticmethod
        def parse_solution_string(input_string):
            # 获取Solution参数
            execution = BaseClass.DataStruct._get_parsed_value(input_string, 'execution')
            target = BaseClass.DataStruct._get_parsed_value(input_string, 'target')
            # 获取Method参数
            method_list = []
            method_matches = re.findall(r'Method\(.*?\)', input_string)
            # 这里就已经提取出来了
            for match in method_matches:
                values = BaseClass.DataStruct._get_parsed_class_value(match)
                method_list.append(values)  # 很明显把true也解析了
            return Solution(execution, target, method_list)

    class Input:

        @staticmethod
        def _click(x, y, duration=1, steps=100):  # 仅move
            start_x, start_y = win32api.GetCursorPos()
            x_distance = x - start_x
            y_distance = y - start_y
            for i in range(steps):
                progress = i / steps
                if progress < 0.5:
                    easing_progress = 2 * progress * progress
                else:
                    easing_progress = -1 + (4 - 2 * progress) * progress
                move_to_x = round(start_x + x_distance * easing_progress)
                move_to_y = round(start_y + y_distance * easing_progress)
                win32api.SetCursorPos((move_to_x, move_to_y))
                time.sleep(duration / steps)
            BaseClass.ShowProcess.reset_rectangle()  # 点击前关闭显示，不然会无法点击
            pyautogui.mouseUp()  # 释放鼠标左键 Nice
            pyautogui.click()  # 先测试直接Click

        @staticmethod  # Key目前先不用管——如无必要勿增实体
        def key(c):  # 键入快捷键 如 key_win+q
            collections = c.split('+')
            pyautogui.hotkey(collections)

        @staticmethod
        def cp(c):  # 粘贴数据，无需担心输入法
            old_clip = pyperclip.paste()
            pyperclip.copy(c)
            pyautogui.hotkey('ctrl', 'v')
            pyperclip.copy(old_clip)  # 恢复之前的剪切数据

    class OCR:

        @staticmethod
        def _average_point(points):  # 计算OCR文字平均位置点
            x_cords, y_cords = zip(*points)
            return sum(x_cords) / len(points), sum(y_cords) / len(points)

        @staticmethod
        def _crop_save(image_path, center_x, center_y, output_path):  # 以某点为中心裁剪图像并保存
            img = Image.open(image_path)
            value = 5  # 5*5
            left = max(0, center_x - value)
            top = max(0, center_y - value)
            right = min(img.width, center_x + value)
            bottom = min(img.height, center_y + value)
            cropped_img = img.crop((left, top, right, bottom))  # 截取图片
            cropped_img.save(output_path)  # 保存截取后的图片

        @staticmethod
        def _get_average_color(image_path):  # 获取图像整体RGB值
            img = Image.open(image_path)
            img = img.convert("RGB")
            pixels = img.load()
            total_red = 0
            total_green = 0
            total_blue = 0
            total_pixels = img.width * img.height
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b = pixels[x, y]
                    total_red += r
                    total_green += g
                    total_blue += b
            average_red = total_red // total_pixels
            average_green = total_green // total_pixels
            average_blue = total_blue // total_pixels
            return (average_red + average_green + average_blue) / 3

        @staticmethod
        def _get_ave_pos(coordinates_list):
            if not coordinates_list:  # 检查列表是否为空
                return []  # 如果列表为空，直接返回空列表
            total_x = 0
            total_y = 0
            for coordinates in coordinates_list:
                for coord in coordinates:
                    total_x += coord[0]
                    total_y += coord[1]
            average_x = total_x / len(coordinates_list * 4)
            average_y = total_y / len(coordinates_list * 4)
            return [round(average_x), round(average_y)]

        @staticmethod
        def _match_sequence(tmp_lst, tmp_sequence):
            full_string = ''.join(tmp_lst)
            start_index = full_string.find(tmp_sequence)
            if start_index != -1:
                end_index = start_index + len(tmp_sequence)
                return start_index, end_index
            else:
                return None

        @staticmethod
        def _parse_ocr_results(ocr_results, t):
            pos_list = []
            text_region = []
            for result in ocr_results:
                text = result['text']
                text_word = result['text_word']
                text_word_region = result['text_word_region']
                if t in text:
                    tmp = BaseClass.OCR._match_sequence(text_word, t)
                    if tmp is not None:  # 说明找到了
                        text_region = result['text_region']
                        for i in range(tmp[0], tmp[1]):
                            pos_list.append(text_word_region[i])
            # 要点击的位置 四点pos定位(用于显示)
            return BaseClass.OCR._get_ave_pos(pos_list), text_region

        @staticmethod
        def ocr(t):
            _flag = True
            while _flag:
                time.sleep(ocr_sleep_time)  # 间断性扫描OCR
                ImageGrab.grab().save(screenshot_save_path, format='JPEG')
                outputs = requests.post(ocr_url, files={'image': open(screenshot_save_path, 'rb')}).json()
                for item in outputs:
                    text = item['text'].lower()
                    s = t.lower()
                    if s in text:  # 注意小写 注意不应该是等于，而是in，注意content是我写入的，text是查到的
                        pos = item['position']  # 左上 右上 右下 左下
                        BaseClass.ShowProcess.update_rectangle(pos)
                        pos_ave = BaseClass.OCR._average_point(pos)
                        BaseClass.Input._click(pos_ave[0], pos_ave[1])
                        _flag = False
                        break

        @staticmethod
        def ocra(t):
            _flag = True
            while _flag:
                time.sleep(ocr_sleep_time)  # 间断性扫描OCR
                ImageGrab.grab().save(screenshot_save_path, format='JPEG')
                outputs = requests.post(ocra_url, files={'image': open(screenshot_save_path, 'rb')}).json()
                # BaseClass.OCR._save_ocr_result(outputs)  # 把outputs放到临时存储区，这样错误检测就可以读取了
                # 更改用户帐户控制设置 更改用户账户控制设置 ???太夸张了
                pos, box = BaseClass.OCR._parse_ocr_results(outputs, t)  # 为什么会是空呢，我已经检查过了呀
                BaseClass.ShowProcess.update_rectangle(box)  # 这个绘制的应该是text_region的平均值
                BaseClass.Input._click(pos[0], pos[1])
                _flag = False

        @staticmethod
        def opt(b, c):
            __flag = True
            while __flag:
                time.sleep(ocr_sleep_time)
                ImageGrab.grab().save(screenshot_save_path, format='JPEG')
                outputs = requests.post(ocra_url, files={'image': open(screenshot_save_path, 'rb')}).json()
                for text in outputs:
                    if c in text['text'].lower():
                        position = text['position']
                        new_x = position[0][0] + 10  # 以新坐标为中心，截取一个10*10的矩形，计算平均颜色
                        new_y = (position[0][1] + position[2][1]) / 2
                        BaseClass.OCR._crop_save(screenshot_save_path, new_x, new_y, crop_path)
                        ave_rgb = BaseClass.OCR._get_average_color(crop_path)
                        if ave_rgb in range(0, 50) or ave_rgb in range(200, 255):  # 平均像素值在边界范围，即黑色或白色，认为未选中
                            if b:  # 如果为True则说明要点击
                                pyautogui.click(new_x, new_y)
                            else:
                                pyautogui.moveTo(new_x, new_y)  # 认为未选中，仅移动鼠标
                        else:
                            if b:
                                pyautogui.moveTo(new_x, new_y)
                            else:
                                pyautogui.click(new_x, new_y)
                        __flag = False

    class OS:

        # 怎么统计桌面数？有必要吗——直接操作完就返回原桌面不就好了

        @staticmethod
        def back_desktop():
            BaseClass.Input.key('ctrl+win+right')

        @staticmethod
        def create_desktop():  # 新建Windows桌面，为每个任务专门分配桌面，借鉴Conda
            BaseClass.Input.key('ctrl+win+d')  # 执行顺序不一样会影响结果，如win+ctrl+d就不会起作用

        @staticmethod
        def ece(c, o):  # 执行函数——精髓
            if c == 'stopprogram':  # 注意小写
                os.system(f'taskkill /f /im {o}.exe')
            elif c == '控制面板':
                os.system('control')
            elif c == '输入下':
                pyautogui.press('down')
            elif c == '关闭窗口':
                pyautogui.hotkey('alt', 'f4')  # 发送快捷键 Alt + F4 来关闭控制面板窗口
                # all_windows = pygetwindow.getAllTitles()  # 获取所有打开的窗口
                # control_panel_window = [window for window in all_windows if "控制面板" in window]  # 查找包含“控制面板”的窗口标题
                # if control_panel_window:
                #     pygetwindow.getWindowsWithTitle(control_panel_window[0])[0].activate()  # 将控制面板窗口置于前台
                #     pyautogui.hotkey('alt', 'f4')  # 发送快捷键 Alt + F4 来关闭控制面板窗口

    class ExceptionHandling:
        pass
        # @staticmethod
        # def check_text_exists(t, d):  # 如果某个文字不存在，则点击输入的文字，可以把他当一个步骤而非全局
        #     # 或者不需要存储，直接调OCR
        #     # outputs = BaseClass.OCR._load_ocr_result()
        #     time.sleep(3)  # 3秒时长，如果3秒后还没有开始就认为下载失败
        #     text_collections = []
        #     time.sleep(ocr_sleep_time)
        #     ImageGrab.grab().save(screenshot_save_path, format='JPEG')
        #     outputs = requests.post(ocr_url, files={'image': open(screenshot_save_path, 'rb')}).json()
        #     for text in outputs:
        #         text_collections.append(text['text'])
        #     if t not in text_collections:  # 不在就点击
        #         for text in outputs:  # 逐步感知机而非全局感知机——算力不够
        #             if d in text['text'].lower():
        #                 pos = BaseClass.OCR._average_point(text['position'])
        #                 pyautogui.moveTo(pos)  # 先移动后点击，可以有延迟
        #                 time.sleep(ocr_sleep_time)  # 果然各种各样的问题都会遇到
        #                 pyautogui.click()

    class ShowProcess:
        class AlphaLabel(tk.Toplevel):  # 如果要点击的文字在区域内，则应该隐藏——其实应该只在测试时查看
            def __init__(self, parent, text):
                tk.Toplevel.__init__(self, parent)
                self.overrideredirect(True)
                self.attributes('-alpha', 0.5)  # 设置窗口透明度
                self.label = tk.Label(self, text=text, font=('Arial', 30), fg='white', bg='black')
                self.label.pack(expand=True, fill='both')
                self.update_idletasks()
                # 算了，不弄了
                # self.geometry('+{}+{}'.format(50, self.winfo_screenheight() - self.winfo_height() - 50))  # 屏幕左下角位置
                self.focus_force()  # 将焦点强制移到该窗口上
                self.update()

            def _update_text(self, new_text):
                if new_text == "":  # 如果新文本为空，结束程序
                    self.destroy()  # 销毁窗口
                    return
                self.label.config(text=new_text)

        @staticmethod
        def _init_text():
            global windows_text
            root_text = tk.Tk()
            root_text.attributes('-alpha', 0.0)  # 隐藏主窗口
            windows_text = BaseClass.ShowProcess.AlphaLabel(root_text, '初始化')
            windows_text.attributes('-topmost', True)  # 设置窗口置顶
            windows_text.grab_set()  # 禁止用户选择其他窗口
            root_text.mainloop()

        @staticmethod
        def start_text():
            threading.Thread(target=BaseClass.ShowProcess._init_text).start()  # 子线程可以控制，不然会阻挡线程

        @staticmethod
        def update_text(t):
            windows_text._update_text(t)

        @staticmethod
        def stop_text():
            time.sleep(3)  # 给点延迟再停止
            windows_text._update_text('')

        class AlphaRectangle(tk.Toplevel):
            def __init__(self, parent, tmp_box):
                tk.Toplevel.__init__(self, parent)
                self.overrideredirect(True)  # 移除窗口边框
                self.attributes('-alpha', 0.6)  # 设置窗口透明度
                self.tmp_box = tmp_box
                self._update_canvas()
                self.update_idletasks()

            def _update_canvas(self):
                width = round(self.tmp_box[1][0] - self.tmp_box[0][0])
                height = round(self.tmp_box[1][1] - self.tmp_box[0][1])
                self.canvas = tk.Canvas(self, bg='blue', highlightthickness=0, width=width, height=height)  # 创建Canvas，背景设为蓝色，无边框
                self.canvas.pack(expand=True, fill='both')
                ave_x = round((self.tmp_box[0][0] + self.tmp_box[1][0]) / 2)
                ave_y = round((self.tmp_box[0][1] + self.tmp_box[1][1]) / 2)
                self.geometry('+{}+{}'.format(ave_x - width // 2, ave_y - height // 2))

            # 应该是这里的问题，要不换一种方式
            def _update_position(self, new_tmp_box):
                if not new_tmp_box:  # 如果新文本为空，结束程序
                    self.destroy()  # 销毁窗口
                    return
                self.tmp_box = new_tmp_box
                self.canvas.pack_forget()  # 移除旧的Canvas
                self._update_canvas()  # 创建并显示新的Canvas

        @staticmethod
        def _init_rectangle():  # 创建AlphaRectangle实例
            global rect_window
            root_rectangle = tk.Tk()
            root_rectangle.attributes('-alpha', 0)  # 隐藏主窗口
            rect_window = BaseClass.ShowProcess.AlphaRectangle(root_rectangle, [(0, 0), (1, 1)])
            rect_window.attributes('-topmost', True)  # 设置窗口置顶
            rect_window.grab_set()
            root_rectangle.mainloop()

        @staticmethod
        def start_rectangle():
            threading.Thread(target=BaseClass.ShowProcess._init_rectangle).start()

        @staticmethod
        def update_rectangle(pos):  # 现在的问题是root为什么跑到左上角了(0,0)
            rect_window._update_position([pos[0], pos[2]])  # 左上、右下

        @staticmethod
        def reset_rectangle():
            rect_window._update_position([(0, 0), (1, 1)])

        @staticmethod
        def stop_rectangle():
            time.sleep(3)  # 给点延迟再停止
            rect_window._update_position([])

    class SystemInit:  # 这个类应该放到系统初始化里，第一次使用WindowsAI时运行

        @staticmethod
        def start():
            BaseClass.SystemInit._close_user_account_control()

        # 思考，这个方式是不是太困难了，要不要换条路，现在的问题是怎么定义操作方式及其表示书写
        @staticmethod
        def _close_user_account_control():  # 检测窗口_用户账户控制
            # 真正训练还得把这些名字都弄成最简单的，减小性能开销
            # 反应太慢了吧我去——动态控制时间？
            # orders应该是字符串。。。
            tmp_orders = [  # 这里相当于已经解析好了，不对，根本不用解析，因为这只是初始化
                # "Solution(execution='关闭用户账户控制',methods=[Method(operation='执行函数', text='控制面板'),Method(operation='点击文字', text='系统和安全'),Method(operation='点击精准文字', text='更改用户帐户控制设置'),Method(operation='查找文字', text='出现以下情况时始终不要通知我',true=Solution(execution='附加操作', methods=[Method(operation='执行函数', text='关闭窗口')]),false=Solution(execution='附加操作', methods=[Method(operation='执行函数', text='输入下')]),for_='True')])"
                "Solution(execution='关闭用户账户控制',methods=[Method(operation='执行函数', text='控制面板'),Method(operation='点击文字', text='系统和安全'),Method(operation='点击精准文字', text='更改用户帐户控制设置'),Method(operation='查找文字', text='出现以下情况时始终不要通知我',true='Solution(execution='附加操作', methods=[Method(operation='执行函数', text='关闭窗口')])',false='Solution(execution='附加操作', methods=[Method(operation='执行函数', text='输入下')])',for_='True')])"
                # "Solution(name='关闭_用户账户控制', item=[Method('执行函数_控制面板'),Method('点击文字_系统和安全'),Method('点击精准文字_更改用户帐户控制设置'),Method('判断文字_')])"
            ]  # 原来是忘记给字符串了
            MainClass(tmp_orders)
            # 是->输入esc，关闭系统和安全 # 这个能不能通过代码实现


class MainClass:
    def __init__(self, raw_collects):
        self.raw_collects = raw_collects
        time.sleep(3)
        self.start()

    @staticmethod
    def check_ocr_text(t):  # 以后节省资源可以一秒钟检测一两次，甚至本地化算力？
        if not t:  # 如果是空则直接返回
            return False  # 说明正常，有文字，或者不进行检测
        ImageGrab.grab().save(screenshot_save_path, format='JPEG')
        outputs = requests.post(ocra_url, files={'image': open(screenshot_save_path, 'rb')}).json()
        for text in outputs:
            if t in text['text'].lower():  # 注意小写 注意不应该是等于，而是in，注意content是我写入的，text是查到的
                return False
        return True  # 说明没检测到

    def start(self):
        BaseClass.ShowProcess.start_text()  # 初始化测试显示
        BaseClass.ShowProcess.start_rectangle()  # 初始化文字识别框
        # 注意这里使用的是第一组下标，也就是第一行操作方案，以后也能做成循环
        solution = BaseClass.DataStruct.parse_solution_string(self.raw_collects[0])
        execution = solution.execution  # 下载
        target = solution.target  # Chrome
        print('methods = ', solution.methods)
        # 判断文字不见了
        # exit()
        # 我希望把 true 和 false 解析成字符串
        for item in solution.methods:
            print('item = ', item)
            print('type = ', type(item))
            # 为什么输入下和关闭窗口都被归为item了，他们应该还是字符串才对
        for method in solution.methods:
            # print('method = ', method)
            time.sleep(ocr_sleep_time)
            operation = method.operation
            text = method.text
            true = method.true
            false = method.false
            for_ = method.for_
            check_text = method.check_text
            alternative_operation = method.alternative_operation
            alternative_text = method.alternative_text
            print('operation = ', operation, len(operation))
            print('text = ', text)
            print('true = ', true)
            print('false = ', false)
            print('for_ = ', for_)
            print('check_text = ', check_text)
            print('alternative_operation = ', alternative_operation)
            print('alternative_text = ', alternative_text)
            if operation == '快捷键':  # Input key 这个大概率不会出错
                BaseClass.Input.key(text)
                BaseClass.ShowProcess.update_text(operation)  # Action而非Content 防止误点击
            elif operation == '复制':  # cp
                BaseClass.Input.cp(text)
                BaseClass.ShowProcess.update_text(operation)
            elif operation == '点击文字':
                BaseClass.OCR.ocr(text)
                BaseClass.ShowProcess.update_text(operation)
                time.sleep(ocr_sleep_time)
                if self.check_ocr_text(check_text):
                    if alternative_operation == '点击精准文字':
                        BaseClass.OCR.ocra(alternative_text)
                    else:
                        BaseClass.OCR.ocr(alternative_text)
                    BaseClass.ShowProcess.update_text('正在重试')
            elif operation == '点击精准文字':
                BaseClass.OCR.ocra(text)
                BaseClass.ShowProcess.update_text(operation)
                time.sleep(ocr_sleep_time)
                if self.check_ocr_text(check_text):
                    if alternative_operation == '点击文字':
                        BaseClass.OCR.ocr(alternative_text)  # 忘记更换操作符了... 忘记给精确了...
                    else:
                        BaseClass.OCR.ocra(alternative_text)
                    BaseClass.ShowProcess.update_text('正在重试')
            elif operation == '查找文字':  # 不是查找精准文字
                # print(type(true), true)
                # print(type(false), false)
                # 怎么不执行呢，奇怪了
                if for_ == 'True':
                    while True:
                        # 这个可以封装成 get_ocr_data()
                        ImageGrab.grab().save(screenshot_save_path, format='JPEG')
                        outputs = requests.post(ocr_url, files={'image': open(screenshot_save_path, 'rb')}).json()
                        for item in outputs:
                            lower_text = item['text'].lower()
                            s = text.lower()
                            if s in lower_text:
                                MainClass(true)
                                return
                        MainClass(false)
                else:
                    ImageGrab.grab().save(screenshot_save_path, format='JPEG')
                    outputs = requests.post(ocr_url, files={'image': open(screenshot_save_path, 'rb')}).json()
                    for item in outputs:
                        lower_text = item['text'].lower()
                        s = text.lower()
                        if s in lower_text:
                            MainClass(true)
                            return
                    MainClass(false)
            # elif action == 'ocra':  # OCR AGREE # OCRA不应该存在，应该用opt1替换 TODO 重新卸载安装QQ
            #     raise DeprecationWarning('已弃用')
            # elif action == 'ocrd':
            #     raise DeprecationWarning('已弃用')  # OCRD可以分解为OCR+替换 # OCRD不应该存在，应该用OCR+RP操作替换
            # elif action == 'opene':  # 暂时用不上
            #     raise DeprecationWarning('暂时未知用途')
            elif operation == 'opt0':  # 选中
                BaseClass.OCR.opt(False, text)
                BaseClass.ShowProcess.update_text(operation)
            elif operation == 'opt1':  # 不选
                BaseClass.OCR.opt(True, text)
                BaseClass.ShowProcess.update_text(operation)
            elif operation == '执行函数':  # execute 执行内部函数
                BaseClass.OS.ece(text, execution)
                BaseClass.ShowProcess.update_text(operation)
            # elif action == '检测文字':  # content = 1_x # 可能要废弃了
            #     BaseClass.ExceptionHandling.check_text_exists(content, special)
            #     BaseClass.ShowProcess.update(action)
            elif operation == '新建桌面':
                BaseClass.OS.create_desktop()
                BaseClass.ShowProcess.update_text(operation)
            elif operation == '回到桌面':
                BaseClass.OS.back_desktop()
                BaseClass.ShowProcess.update_text(operation)
        BaseClass.ShowProcess.stop_text()
        BaseClass.ShowProcess.stop_rectangle()


if __name__ == '__main__':
    # 检测文件是否存在，如果不存在则进行初始化操作并记录内容
    BaseClass.SystemInit.start()
    # exit()
    # 考虑到Windows动画效果与OCR执行耗能，其实一秒钟检测一次就挺好的了，不用再改了
    # 操作符可以改为中文，这样就可以实时问LLAMA下一步该做什么了——中文操作符提高泛化能力
    # 原来问题是管理员模式进入。。。
    # 点击文字出问题了，还是没点上——需要使用函数取消左键按下的状态
    # 我想可视化它的识别过程——看起来帅呆了，检测到之后再屏幕上绘制方框
    # 三条为基本单位，包括执行步骤、环境状态、备选方案

    # 用户想取消怎么办，加个监听 Ctrl+P

    # 静态生成还是动态规划，亦或是两者结合——当然是结合
    # 怎么写动态规划？——使用环境OCR计算相似度？——那数据量就太大了
    # 我得先有个知识库，比如看到用户账户控制的弹窗就应该选择是，看到保留什么的也应该选择
    # 其实也可以先用YOLO检测弹窗，写一个弹窗处理，输入弹窗内容，输出下一步信息
    # 但是QQ安装会不会也会被理解为弹窗信息，所以应该选择硬检测，检测到这个文字就执行这个操作

    # 使用一个YOLO模型训练就行，后期再说多模型问题（数据相似但分类不同的情况）
    # 我完全可以训练大量用户账户控制窗口，让系统知道这个怎么处理，但其实OCR检测到关键位置的关键文字就可以下一步了

    # 重写方法，测试安装下载卸载——好漫长，感觉前面是最难的，到现在Chrome还没安装完成。。。。
    '''
    orders = [  # 下载安装QQ # 卸载QQ
        # win+q有风险，可能没有输入框，win最稳定
        # https://im.qq.com/index/
        'download_qq>>key_win+d->key_win->cp_chrome->key_enter->cp_https://im.qq.com/index/->key_enter->ocr_下载->ocr_windows->ocr_全新版本下载',
        'install_qq>>ocr_完成->ocra_阅读并同意->ocr_自定义选项->ocrd_Program->opt0_生成快捷方式->opt1_开机自动启动->ocr_立即安装->ocr_完成安装',
        'uninstall_qq>>ece_StopProgram->key_win+x->key_p->ocr_搜索应用->cp_qq->hi_uninstall->ocr_卸载->ocr_卸载->ocr_卸载->ocr_是->ocr_确定'
    ]
    '''
    # IMPORTANT 先做这个，虚拟机通过Edge安装Chrome
    # 还是得做Chrome卸载程序，可以仅当测试嘛
    orders = [
        # https://www.google.cn/chrome/index.html
        # '下载_chrome>>新建桌面_->快捷键_win->复制_https://www.google.cn/chrome/index.html->快捷键_enter->点击文字_下载chrome->点击文字_打开文件',
        # 感觉可以把这三种操作定义为一个类，用列表添加，试试字符串转类
        # TempClass(name='下载_Chrome',item=[['新建桌面_',_,_],['快捷键_Win',_,_])
        # '下载_Chrome>>新建桌面_->快捷键_Win->复制_https://www.google.cn/chrome/index.html->快捷键_Enter->点击文字_下载Chrome->点击精准文字_打开文件',
        # 有时候会识别成Q打开文件
        # 受不了了，精准不是精确，字打错了就离谱
        # '特征文字_>>_->_->_->_->ChromeSetup->_->',  # 如果到下一步时没有这些文字则执行该步骤的备选方法 不写的说明是强稳定性，不需要额外验证 # 离谱，少写了一个东西
        # '备选方案_>>_->_->_->_->点击精准文字_手动下载->点击精准文字_打开文件',

        # 注意使用双字符串
        "Solution(name='下载_Chrome', item=[Method('新建桌面_', '', ''), Method('快捷键_Win', '', ''), Method('复制_https://www.google.cn/chrome/index.html', '', ''), Method('快捷键_Enter', '', ''), Method('点击文字_下载Chrome', 'ChromeSetup', '点击精准文字_手动下载'), Method('点击精准文字_打开文件', '', '')])"

        # OCR和OCRA？要不要提取页面信息，确认哪些是可互动组件，哪些是普通组件

        # 是不是应该先走一遍正常的流程录屏编写操作

        # '下载_chrome>>点击文字_打开文件',
        # '特征文字_>>Setup',  # 如果到下一步时没有这些文字则执行该步骤的备选方法 不写的说明是强稳定性，不需要额外验证
        # '备选方案_>>强联系',

        # '备选方案_>>强联系->快捷键_win->强联系->强联系->点击文字_重新下载chrome->点击文字_打开文件->快捷键_left+enter',
        # '备选方案_>>新建桌面_->快捷键_win->复制_https://www.google.cn/chrome/index.html->快捷键_enter->点击文字_重新下载chrome->点击文字_打开文件->快捷键_left+enter',
        # 'uninstall_qq>>ece_StopProgram->key_win+x->key_p->ocr_搜索应用->cp_qq->hi_uninstall->ocr_卸载->ocr_卸载->ocr_卸载->ocr_是->ocr_确定'
    ]

    MainClass(orders)

    # 关于多级封装的设计思想——这个以后写多了完全可以封装起来，现在先不管了
    '''
    关于多级封装的构思 
        一级封装 OCR CLICK 
        二级封装 新建桌面 打开浏览器 输入内容 弹窗输入
        三级封装 打开浏览器输入内容
        四级封装 浏览器搜索内容并整理
        N级封装 下载程序 完成操作
    每级应该是上一级的封装
    一级封装最少，然后逐级递增
    相当于做了很多库，就不用每次都一个个写了。这么做是为了简化开发过程，就好像click不需要每次都写pyautogui一样，直接封装起来
    封装不会无止境地进行，应该只封装常用方法
    '''
    # 是不是除了操作符，我也应该给一组环境符——计入所有OCR识别文字，计算相似度，如果相似则认为页面正确
    # 截屏的时候能不能可视化一下——到底要不要呢——可以便于观察
    # 用户账户控制——只要出现这个页面就方向键左，回车——这个是需要一直检测的，其他的尽可能地避免出错
    # 进行文本归类回归，仅使用坐标位置或者坐标加文字
    # 文本分类检测提示选选择框，训练这个——使用Pytorch构建框架——可以用Transformer的环境训练，其中有Pytorch，复制一个就好

    # cp怎么会出问题呢-虚拟机好像不共享粘贴板——所以才想写一个程序
    # 随后测试QQ安装，不使用废弃函数
    # 再然后尝试安装YOLO环境，先获取电脑信息——流程与错误处理是核心
    # 内置GPT-4o，只有遇到流程信息我才会处理
    # 结束后新增打分反馈输入框，查看错误信息(需要录屏)
    # 让WindowsAI新建文档、写代码、改代码

# 未下载问题，为什么呢——怎么让机器知道下一步会出现什么呢，这样不就可以预测了——使用特征文字检测方法
# 是按文字还是文字加位置还是分类法如下载等——这个意义不大，我只需要关注流程即可
# 文字是要比图像快的，快很多——尽可能使用文字而非图像，图像识别太慢了
# 现在的主要问题是没有获取屏幕文字信息，这个很关键——没必要
# 虚拟机没网是什么情况，麻了——重启笔记本就好了
