#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# @Time    : 2025/4/9 上午9:42
# @Author  : 单子叶蚕豆_DzyCd
# @File    : Assert.py
# @IDE     : PyCharm
from typing_extensions import Optional


class Product:
    def __init__(self, id, name, category, length, width, **kwargs):
        self.id = id
        self.name = name
        self.category = category
        self.length = length
        self.width = width
        self.warehouse_id = 0

        for key, value in kwargs.items():
            setattr(self, key, value)

    def show_info(self):
        print("Name : ", self.name)
        print("Category : ", self.category)
        print("Length : ", self.length)
        print("Width : ", self.width)

    @property
    def area(self) -> float:

        return self.length * self.width

    def __str__(self):
        return f"物品(ID:{self.id}, 名称:{self.name}, 面积:{self.area}({self.width} * {self.length}), 类别:{self.category})"



class StorageLocation:
    def __init__(self, location_id: str, max_length: float, max_width: float):
        self.location_id = location_id
        self.max_length = max_length
        self.max_width = max_width
        self.remaining_length = max_length
        self.remaining_width = max_width
        self.stored_goods = []

    def can_fit(self, goods_length: float, goods_width: float) -> bool:
        return (goods_length <= self.remaining_length and
                goods_width <= self.remaining_width)

    def place_goods(self, goods_id: int, goods_length: float, goods_width: float):
        if not self.can_fit(goods_length, goods_width):
            raise ValueError("货物尺寸超过存储位置剩余空间")

        self.stored_goods.append(goods_id)
        self.remaining_length -= goods_length
        self.remaining_width -= goods_width

    def remove_goods(self, goods_id: int):
        for i in self.stored_goods:
            if i == goods_id:
                self.stored_goods.remove(i)

    def __str__(self):
        return (f"存储位置(ID:{self.location_id}, 剩余空间:{self.remaining_length}x{self.remaining_width}, "
                f"存放货物数:{len(self.stored_goods)})")


class Warehouse:
    def __init__(self, id: int, name: str, length: int, width: int, category: str, split_size=2, **kwargs):
        self.id = id
        self.name = name
        self.length = length
        self.width = width
        self.category = category
        self.storage_locations = []
        self._initialize_storage_locations(split_size)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def _initialize_storage_locations(self, cut: int):
        length = self.length // cut
        width = self.width // cut
        for i in range(cut*cut):
            self.storage_locations.append(StorageLocation(str(i), length, width))



    def find_best_location(self, goods_length: float, goods_width: float) -> Optional[StorageLocation]:
        best_location = None
        min_waste = float('inf')

        for location in self.storage_locations:
            if location.can_fit(goods_length, goods_width):
                waste = (location.remaining_length - goods_length) * (location.remaining_width - goods_width)
                if waste < min_waste:
                    min_waste = waste
                    best_location = location

        return best_location

    @property
    def area(self) -> float:

        return self.length * self.width

    def __str__(self):
        return f"仓库(ID:{self.id}, 名称:{self.name}, 面积:{self.area}({self.width} * {self.length}), 类别:{self.category})"

