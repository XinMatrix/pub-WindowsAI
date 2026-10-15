if __name__ == '__main__':
    try:
        x = 5 / 0
    except ZeroDivisionError:
        print("除数不能为0！")
    finally:
        print("这里的代码总会被执行")
