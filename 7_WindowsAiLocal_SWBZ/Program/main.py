import datetime
import glob
import os
import re
import shutil
import threading
import time
import cv2
import keyboard
import numpy as np
import pyautogui

# 把它挪到MyFunClass上面就好了，可以正常设置log了（只能设置顶层）
from config import my_logger
from MyFunClass import MyFun, start_action, sj

# 这个是会执行的
MyFun.Init.create_directories('MyWindowsAi',
                              ['Programs', 'Downloads', 'Projects', 'Statics', 'Configs', 'Logs'])  # 默认先都在C盘创建


def on_hotkey():
    recorder.stop_recording()
    MyFun.System.kill_processes('Photos.exe')
    # os.startfile(r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作')
    my_logger.error('用户强行停止程序')
    os._exit(0)


def check_admin():
    # 检测是否为管理员权限
    if MyFun.System.is_admin() != 1:
        my_logger.critical('权限不足，请使用管理员权限运行')
        raise PermissionError('权限不足，请使用管理员权限运行')
    my_logger.info('添加强制停止快捷键' + ' Ctrl+Alt+K')
    keyboard.add_hotkey('ctrl+alt+k', on_hotkey)


# 屏幕录制
class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.output_path = ""
        self.writer = None
        self.recording_thread = None

    @staticmethod
    def remove_old_log_videos(output_folder: str, log_text: str):
        """
        删除 output_folder 里所有形如 日志-{log_text}-*.mp4 的文件
        """
        # 构造匹配通配符：日志-<log_text>-任何时间戳.mp4
        pattern = os.path.join(output_folder, f"日志-{log_text}-*.mp4")

        for old_file in glob.glob(pattern):
            try:
                os.remove(old_file)
                my_logger.info(f"已删除旧日志文件: {old_file}")
            except Exception as e:
                my_logger.error(f"删除 {old_file} 失败: {e}")

    def start_recording(self, input_str):
        try:
            if self.recording:
                return False

            output_folder = sj('TempFolder')

            # 确保输出目录存在
            os.makedirs(output_folder, exist_ok=True)

            def get_tag_payload(text: str) -> str:
                match = re.search(r"TAG\s*\(\s*([^()]+?)\s*\)", text, re.IGNORECASE)
                return match.group(1).strip() if match else "其他"

            log_text = get_tag_payload(input_str)

            # 删除旧的同类型日志视频
            self.remove_old_log_videos(output_folder, log_text)

            # === ① 生成带日期-时间戳的文件名 ===
            # 生成带时间戳的文件名
            # ts = datetime.datetime.now().strftime("%H时%M分%S秒")
            ts = datetime.datetime.now().strftime("%H-%M-%S") # 冒号是非法的，无法创建
            self.output_path = os.path.join(output_folder, f"日志-{log_text}-{ts}.mp4")

            # 获取屏幕尺寸
            screen_size = pyautogui.size()
            frame_size = (screen_size.width, screen_size.height)

            # 设置视频编码参数（使用MP4兼容的编码器）
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或者使用 'avc1' 需要额外配置
            fps = 30  # 30帧/秒
            self.writer = cv2.VideoWriter(self.output_path, fourcc, fps, frame_size)

            if not self.writer.isOpened():
                raise RuntimeError("无法初始化视频写入器，请检查编码器支持")

            self.recording = True
            my_logger.info(f"已开启后台录制")

            # 启动录制线程
            self.recording_thread = threading.Thread(target=self._record_screen)
            self.recording_thread.start()

            return True

        except Exception as e:
            my_logger.error(f"启动录制失败: {e}", exc_info=True)
            if self.writer is not None:
                self.writer.release()
            return False

    def _record_screen(self):
        try:
            while self.recording:
                start_time = time.time()

                # 捕获屏幕
                img = pyautogui.screenshot()

                # 转换为numpy数组并转换颜色空间
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                # 写入视频文件
                self.writer.write(frame)

                # 精确控制帧率
                elapsed = time.time() - start_time
                sleep_time = max(0, (1 / 30) - elapsed)
                time.sleep(sleep_time)

        except Exception as e:
            my_logger.error(f"录制过程中出错: {e}", exc_info=True)
        finally:
            self._cleanup()

    def stop_recording(self):
        if not self.recording:
            return False

        self.recording = False
        if self.recording_thread is not None:
            self.recording_thread.join()

        my_logger.info(f"录制已停止，视频已保存到: {self.output_path}")

        # === ② 轮换，只保留最近 7 条日志视频 ===
        try:
            folder = os.path.dirname(self.output_path)
            videos = sorted(
                glob.glob(os.path.join(folder, "日志-*.mp4")),
                key=os.path.getmtime
            )
            for old_file in videos[:-7]:
                os.remove(old_file)
                my_logger.info(f"已删除旧日志视频: {old_file}")
        except Exception as e:
            my_logger.warning(f"清理旧日志视频时出错: {e}")

        return True

    def _cleanup(self):
        if self.writer is not None:
            self.writer.release()
            self.writer = None


# FIXME 我需要使用非OCR主导的逻辑循环
def main_function(result, user_message):
    MyFun.Init.show_bg()
    time.sleep(1)
    ocr_outputs = MyFun.Fun.once_ocr()  # 先进行一次OCR识别，开始任务
    # 开始使用强制检测，必须完全相等，相当于一次小自检
    if any(item['text'] == 'WindowsAi' for item in ocr_outputs):  # 执行第一条，第一条永远是第一条，不存在分支情况
        start_action(result, result[0][1], user_message)  # start_action函数仅仅是执行函数库操作，其他概不影响
    else:
        my_logger.error('WindowsAi识别失败')
        raise Exception('WindowsAi识别失败')


if __name__ == '__main__':

    # 定义任务
    method = [

        # TODO 找找需要PRA的单位，最好是有预算的，或者中小企业，政府机构等

        # TODO 需要改动哪些代码到时候说，这次先把环境配置好
        #  还是全发过去吧，E:\WindowsAi\7_WindowsAiLocal_SWBZ 以及 .-i-d-e-a
        #  没网就重启电脑或SZ50——问问客服
        #  必剪有电脑版吗，应该快一点
        #  做好的视频加个速把，1.25，感觉有点慢了

        # FINISHED
        #  无法使用剪映制作数字人，AI生成视频
        #  剪映太快了，效果不太理想

        # 测试单例
        # ['', f'TAG(测试)->CLICK()->CLICK()->CLICK()->CLICK()->CLICK()->CLICK()->FINISH()']

        # 城市延时摄影——youtube上搜即可，记得筛选
        # city timelapse compilation 4K 1 hour
        # urban city timelapse 4K long video
        # city skyline timelapse relaxing 4K
        # city time-lapse ultra hd 60 minutes
        # 微缩景观
        # tilt shift timelapse full hd
        # miniature city timelapse compilation
        # toy city tilt-shift 4K
        # 下载视频
        # 下次下载这个 https://www.youtube.com/watch?v=B5unCXpegAw
        # C:\Users\USER\Downloads\yt-dlp.exe --cookies "C:\Users\USER\Downloads\www.youtube.com_cookies.txt" -f "bv*[height=1080][ext=mp4]" -o "video1080p.mp4" "https://www.youtube.com/watch?v=ITBMT-sUeH0"
        # C:\Users\USER\Downloads\yt-dlp.exe --cookies "C:\Users\USER\Downloads\www.youtube.com_cookies.txt" -f "bv*[height=1080][ext=mp4]" -o "video1080p.mp4" "https://www.youtube.com/watch?v=B5unCXpegAw"

        # TODO 只需要把 素材、未完成视频 发给小电脑就好了，其他事情不需要管

        # ['',
        #  f'TAG(0-合成视频)->'
        #  f'INIT_FILES()->START_PROGRAM_BY_PATH({sj('MumuPath')})->WAIT_OCR(游戏中心)->SLEEP(5)->HOTKEY(ALT+F4)->'
        #  f'COPY({sj('VideoLink')})->START_PROGRAM_BY_PATH({sj('JijidownPath')})->'
        #  f'WAIT_OCR(下载管理)->KEY(TAB)->KEY(ENTER)->CLICK_TEXT(MP3音频文件)->SLEEP(1)->CLICK()->SLEEP(10)->'
        #  f'WAIT_MP3({sj('TempFolder')})->HOTKEY(ALT+F4)->AUDIO_2_TEXT_BY_API({sj('DateFilepath')})->'
        #  f'START_GPT_API({sj('DateFilepath')})->'  # 在这里可以添加 START_GPT_API_TO_WECHAT_ARTICLE()
        #  f'GENERATE_COVER({sj('json_path')})->START_PROGRAM_BY_PATH({sj('MumuPath')})->'
        #  f'WAIT_OCR(游戏中心)->SLEEP(1)->KEY(F11)->CLICK_TEXT_TOP(必剪,80)->SET_FOCUS(MuMu模拟器12)->CLICK_TEXT(音色克隆)->'
        #  f'CLICK_TEXT(音色01)->CLICK_TEXT(去生成文本朗读)->COPY_TEXT_FROM_JSON({sj('json_path')})->PAST_TEXT()->'
        #  f'CLICK_TEXT(生成朗读音频)->CLICK_TEXT(导出)->CLICK_TEXT(完成)->CLICK_TEXT(不保留)->SLEEP(3)->CLICK_TEXT(创作)->'
        #  f'CLICK_TEXT(语音转%)->SLEEP(1)->CLICK_POSITION(770,240)->CLICK_TEXT(下一步)->SLEEP(1)->CLICK_TEXT(开始识别)->'
        #  f'CLICK_TEXT(导出)->WAIT_OCR(已保存)->SLEEP(3)->HOTKEY(ALT+F4)->MOVE_TO_MAKE({sj('BuildVideoPath')})->'
        #  f'CUT_VIDEO()->CREATE_FINAL_VIDEO()->SLEEP(3)->COPY_VIDEO_TO_FOLDER()->UPDATE_VIDEO_PATH()->'
        #  f'GIT_REPO()->DELETE_MIDDLE_FILES()->FINISH()']

        ['',
         f'TAG(1-全流程-发表视频)->'
         f'TAG(2-检查登录)->'
         f'WEB_BROWSER_EDGE({sj('XiaoHongShu')})->SLEEP(0.25)->'
         f'WEB_BROWSER_EDGE({sj('ShiPinHao')})->SLEEP(0.25)->'
         f'WEB_BROWSER_EDGE({sj('DouYin')})->SLEEP(0.25)->'
         f'WEB_BROWSER_EDGE({sj('BaiJiaHao')})->SLEEP(0.25)->'
         f'WEB_BROWSER_EDGE({sj('BZhan')})->SLEEP(0.25)->'
         f'HOTKEY(CTRL+TAB)->WAIT_OCR_F5(上传视频)->'  # 小红书
         f'HOTKEY(CTRL+TAB)->WAIT_OCR_F5(视频描述)->'  # 视频号
         f'HOTKEY(CTRL+TAB)->WAIT_OCR_F5(上传视频)->'  # 抖音
         f'HOTKEY(CTRL+TAB)->WAIT_OCR_F5(点击上传%)->'  # 百家号
         f'HOTKEY(CTRL+TAB)->WAIT_OCR_F5(上传视频)->'  # B站
         f'SLEEP(3)->'
         f'TAG(3-小红书)->'
         f'WEB_BROWSER_EDGE({sj('XiaoHongShu')})->WAIT_OCR(%点击上传)->KEY(F11)->SLEEP(1)->HOTKEY(CTRL+0)->SLEEP(1)->HOTKEY(CTRL++)'
         f'->SLEEP(1)->HOTKEY(CTRL++)'
         f'->CLICK_TEXT(%点击上传)->SLEEP(1)->INPUT({sj('VideoPath')})->SLEEP(0.5)->KEY(ENTER)->'
         f'CLICK_TEXT(填写标题%)->COPY_TITLE_FROM_JSON({sj('json_path')})->PAST_TEXT()->KEY(TAB)->'
         f'COPY_NOTAGS_FROM_JSON({sj('json_path')})->PAST_TEXT()->MOVE_MOUSE_TO_TOP(300)->'
         f'INPUT_LABELS_AND_KEY_ENTER({sj('json_path')})->'
         f'WAIT_OCR(%上传成功)->SLEEP(2)->KEY(F11)->SLEEP(1)->HOTKEY(CTRL+0)->CLICK_TEXT(发布)->SLEEP(3)->'
         f'TAG(4-视频号)->'
         f'WEB_BROWSER_EDGE({sj('ShiPinHao')})->CLICK_TEXT(上传时长%)->SLEEP(1)->INPUT({sj('VideoPath')})->SLEEP(0.5)->'
         f'KEY(ENTER)->WAIT_OCR(删除)->CLICK_TEXT(添加描述)->COPY_INTRODUCTION_FROM_JSON({sj('json_path')})->PAST_TEXT()->KEY(TAB)->'
         f'KEY(TAB)->KEY(TAB)->KEY(SPACE)->KEY(TAB)->KEY(TAB)->KEY(SPACE)->CLICK_TEXT(声明原创)->CLICK_TEXT(发表)->SLEEP(3)->'
         f'TAG(5-抖音)->'
         f'WEB_BROWSER_EDGE({sj('DouYin')})->CLICK_TEXT(%上传视频)->SLEEP(1)->INPUT({sj('VideoPath')})->SLEEP(0.5)->KEY(ENTER)->'
         f'WAIT_OCR(预览视频%)->CLICK_TEXT(填写作品标题%)->COPY_TITLE_FROM_JSON({sj('json_path')})->PAST_TEXT()->KEY(TAB)->'
         f'COPY_NOTAGS_FROM_JSON({sj('json_path')})->PAST_TEXT()->INPUT_LABELS_AND_KEY_ENTER({sj('json_path')})->CLICK_TEXT(选择封面)->'
         f'CLICK_TEXT(完成)->SLEEP(3)->ROLL_TO_BOTTOM()->CLICK_TEXT(发布)->SLEEP(3)->'
         f'TAG(6-百家号)->'
         f'WEB_BROWSER_EDGE({sj('BaiJiaHao')})->CLICK_TEXT(点击上传%)->SLEEP(1)->INPUT({sj('VideoPath')})->SLEEP(0.5)->KEY(ENTER)->'
         f'WAIT_OCR_END(剩余时间%)->ROLL_TO(-700)->CLICK_TEXT(导出视频)->HOTKEY(CTRL+A)->'
         f'COPY_TITLE_FROM_JSON({sj('json_path')})->PAST_TEXT()->ROLL_TO_BOTTOM()->CLICK_TEXT(导出视频)->HOTKEY(CTRL+A)->'
         f'COPY_BAIJIAHAO_FROM_JSON({sj('json_path')})->PAST_TEXT()->CLICK_TEXT(发布)->SLEEP(3)->'
         f'TAG(7-B站)->'
         f'WEB_BROWSER_EDGE({sj('BZhan')})->CLICK_TEXT(上传视频)->SLEEP(1)->INPUT({sj('VideoPath')})->SLEEP(0.5)->KEY(ENTER)->'
         f'WAIT_OCR(%更换视频)->HOTKEY(CTRL++)->SLEEP(1)->CLICK_TEXT(更换封面%)->HOTKEY(CTRL+0)->SLEEP(3)->CLICK_TEXT(完成)->'
         f'CLICK_TEXT_RIGHT(%标题,200)->HOTKEY(CTRL+A)->'
         f'COPY_TITLE_FROM_JSON({sj('json_path')})->PAST_TEXT()->KEY(TAB)->INPUT_BZHAN_TAGS({sj('json_path')})->'
         f'KEY(TAB)->COPY_INTRODUCTION_FROM_JSON({sj('json_path')})->PAST_TEXT()->ROLL_TO_BOTTOM()->CLICK_TEXT(立即投稿)->'
         f'SLEEP(3)->CLICK_POSITION(1890,20)->CLICK_POSITION(960,540)->FINISH()']

    ]

    check_admin()
    recorder = ScreenRecorder()
    recorder.start_recording(str(method))
    start_time = time.time()

    try:
        main_function(method, '0')
    except KeyboardInterrupt:
        my_logger.error('用户强行停止程序')
        MyFun.System.kill_processes('Photos.exe')
    except Exception as e:
        my_logger.error(f"{'错误'}: {e}", exc_info=True)
        MyFun.System.kill_processes('Photos.exe')
        shutil.copy(os.path.join(os.path.expanduser("~"), "Desktop/MyWindowsAi/Logs/running.log"),
                    os.path.join(r"E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作", "running.log"))
        # os.startfile(r'E:\WindowsAi\7_WindowsAiLocal_SWBZ\临时制作')  # 打开日志文件夹
        # os.startfile(sj('log_path'))  # 打开日志文件
    finally:
        recorder.stop_recording()

    end_time = time.time()
    my_logger.info(f"程序运行时间: {end_time - start_time:.2f}s")
