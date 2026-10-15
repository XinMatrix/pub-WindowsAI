# 我到底想做什么？
# 基于地理位置的信息展板，最好有3D显示
# 用户问理发店在哪，我应该给出理发店入口的 What3Words 地址，并给出使用说明，开放时间，价格等信息
# 还有监控室
# 校医院
# 学校发票信息也得有

from dataclasses import dataclass, field
from typing import List


# 虽然可以直接使用str，但这样规范些
@dataclass
class Building:
    name: str = ''  # 小崔理发店
    type: str = ''  # 理发店
    menu: str = ''  # 理发多少钱，中文描述即可（因为要微调）
    open_time: str = ''  # 开放时间
    birth_year: str = ''  # 2015
    entrance_address: List[str] = field(default_factory=list)  # 入口地址，入口也可能很大，所以要用列表
    around_address: List[str] = field(default_factory=list)  # 围绕地址


# @dataclass
# class Road:
#     name: str
#     type: str
#     address: []


b1 = Building(name='小崔理发店', type='理发店', menu='理发多少钱', birth_year='2015', entrance_address=['///逻辑.香瓜.沙漠'],
              around_address=[])
print(b1)
