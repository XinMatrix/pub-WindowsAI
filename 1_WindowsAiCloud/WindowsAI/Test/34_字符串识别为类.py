# TempClass(name='下载_Chrome',item=[['新建桌面_',_,_],['快捷键_Win',_,_])
import re
from dataclasses import dataclass
from typing import List


@dataclass
class Method:
    plan_a: str
    rec_text: str
    plan_b: str


@dataclass
class Solution:
    name: str
    item: List[Method]


# class Method:
#     def __init__(self, plan_a, rec_text, plan_b):
#         self.plan_a = plan_a
#         self.rec_text = rec_text
#         self.plan_b = plan_b
#
#
# class Solution:
#     def __init__(self, name, item: List[Method]):
#         self.name = name
#         self.items = item


def parse_solution_string(input_string):
    name_match = re.search(r"name='(.*?)'", input_string)
    temp_name = name_match.group(1) if name_match else ""
    item_matches = re.findall(r"Method\('(.*?)', '(.*?)', '(.*?)'\)", input_string)
    temp_item = [Method(*match) for match in item_matches]
    return Solution(temp_name, temp_item)


if __name__ == '__main__':
    # 还是用空表示会比较好，感觉
    input_str = "Solution(name='下载_Chrome', item=[Method('新建桌面_', '', ''), Method('快捷键_Win', '', '')])"
    parsed_solution = parse_solution_string(input_str)
    print(parsed_solution.name)
    for item in parsed_solution.item:
        print(item.plan_a, item.rec_text, item.plan_b)
    # print(parsed_solution.items)
    # tmp = Solution('下载_Chrome', [Method('新建桌面_', '', ''), Method('快捷键_Win', '', '')])
