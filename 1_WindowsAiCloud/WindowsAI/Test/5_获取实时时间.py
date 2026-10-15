from datetime import datetime

if __name__ == '__main__':
    # 获取当前时间
    now = datetime.now()
    # 获取微秒部分，然后将其转换为毫秒
    milliseconds = now.microsecond // 1000  # 除以1000将微秒转换为毫秒
    # 格式化时间为 "年-月-日 时:分:秒.毫秒" 的形式
    formatted_time = now.strftime(f"%Y年%m月%d日%H时%M分%S秒{milliseconds:03d}毫秒")
    print("当前完整时间（含毫秒）：", formatted_time)
    exit()
    date = datetime.now()
    now = datetime.now()
    tmp = f'{date.year}_{date.month}_{date.day}'
    print(tmp)
    # print(f'{now.hour}_{now.minute}')  # 这个方法会导致部分属性不提示
