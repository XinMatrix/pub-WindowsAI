def find_continuous_sequence(tmp_lst, tmp_sequence):
    full_string = ''.join(tmp_lst)
    start_index = full_string.find(tmp_sequence)
    if start_index != -1:
        end_index = start_index + len(tmp_sequence)
        return start_index, end_index
    else:
        return None


if __name__ == '__main__':
    # for i in range(3, 5):
    #     print(i)
    # exit()
    # 示例用法
    lst = ["你", "好", "我", "是", "陈", "鑫"]
    print(type(lst))
    sequence = "是YOUR_NAME"
    result = find_continuous_sequence(lst, sequence)
    print(result)  # 输出 (3, 5)
    print(lst[0])
