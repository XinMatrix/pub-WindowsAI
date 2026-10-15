import os
import time

from Action import start_action
from Class_2_Init import create_directories, show_bg
from Class_4_Fun import once_ocr_en
# from MyFunClass import MyFun, start_action
from config import get_language, my_logger, log_path

# MyFun.Init.create_directories('MyWindowsAi',
#                               ['Programs', 'Downloads', 'Projects', 'Statics', 'Configs', 'Logs'])  # 默认先都在C盘创建
create_directories('MyWindowsAi', ['Programs', 'Downloads', 'Projects', 'Statics', 'Configs', 'Logs'])  # 默认先都在C盘创建


# # 我需要使用非OCR主导的逻辑循环
# def main_function(result, user_message):
#     try:  # 使用顶级异常捕获
#         if user_message != '1':  # 因为 1 是配置Hyper-V虚拟机，可以直接使用函数完成，不需要显示这个
#             MyFun.Init.show_bg()
#             time.sleep(1)
#             # ocr_outputs = MyFun.Fun.once_ocr_zh()  # 先进行一次OCR识别，开始任务
#             ocr_outputs = MyFun.Fun.once_ocr_en()  # 先进行一次OCR识别，开始任务
#             # 开始使用强制检测，必须完全相等，相当于一次小自检
#             if any(item['text'] == 'WindowsAi' for item in ocr_outputs):  # 执行第一条，第一条永远是第一条，不存在分支情况
#                 start_action(result, result[0][1], user_message)  # start_action函数仅仅是执行数据库操作，其他概不影响
#             else:
#                 my_logger.error(get_language('WindowsAi识别失败'))
#                 raise Exception(get_language('WindowsAi识别失败'))
#         else:
#             # 直接执行函数
#             start_action(result, result[0][1], user_message)  # start_action函数仅仅是执行数据库操作，其他概不影响
#     except Exception as error:
#         my_logger.error(f"{get_language('错误')}: {error}", exc_info=True)
#         os.startfile(log_path)
# 我需要使用非OCR主导的逻辑循环
def main_function(result, user_message):
    try:  # 使用顶级异常捕获
        if user_message != '1':  # 因为 1 是配置Hyper-V虚拟机，可以直接使用函数完成，不需要显示这个
            show_bg()
            time.sleep(1)
            # ocr_outputs = MyFun.Fun.once_ocr_zh()  # 先进行一次OCR识别，开始任务
            ocr_outputs = once_ocr_en()  # 先进行一次OCR识别，开始任务
            # 开始使用强制检测，必须完全相等，相当于一次小自检
            if any(item['text'] == 'WindowsAi' for item in ocr_outputs):  # 执行第一条，第一条永远是第一条，不存在分支情况
                start_action(result, result[0][1], user_message)  # start_action函数仅仅是执行数据库操作，其他概不影响
            else:
                my_logger.error(get_language('WindowsAi识别失败'))
                raise Exception(get_language('WindowsAi识别失败'))
        else:
            # 直接执行函数
            start_action(result, result[0][1], user_message)  # start_action函数仅仅是执行数据库操作，其他概不影响
    except Exception as error:
        my_logger.error(f"{get_language('错误')}: {error}", exc_info=True)
        os.startfile(log_path)
