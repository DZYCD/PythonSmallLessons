#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# @Time    : 2025/4/9 上午10:53
# @Author  : 单子叶蚕豆_DzyCd
# @File    : operations.py
# @IDE     : PyCharm
from Assert import *
from datetime import datetime


class WarehouseManager:
    def __init__(self):
        self.warehouses = []
        self.goods = []
        self.operation_logs = []

        self._initialize_default_warehouses()

    def _initialize_default_warehouses(self):
        default_warehouses = [
            Warehouse(1, "食品仓", 50, 30, "食品"),
            Warehouse(2, "冷链仓", 100, 100, "*"),
            Warehouse(3, "日用品仓", 60, 40, "日用品"),
            Warehouse(4, "电子产品仓", 45, 35, "电子产品")
        ]
        self.warehouses.extend(default_warehouses)

    def create_warehouse(self, name, length, width, category, cut=2):
        self.warehouses.append(Warehouse(len(self.warehouses), name, length, width, category, cut))
        return self.warehouses[-1]

    def create_goods(self, **kwargs) -> Product:

        goods = Product(**kwargs)
        self.goods.append(goods)
        self._log_operation("CREATE", goods.id, f"新建货物: {goods.name}")
        return goods

    def query_goods(self, **kwargs):
        self._log_operation("QUERY", -1, "查询库存")
        msg = ""
        for i in self.goods:
            msg += f'{i.name}, 宽{i.width}, 长{i.length}, 种类{i.category}, 所属库{self._find_warehouse(i.warehouse_id)}\n'
        return msg

    def query_goods_info(self, goods_id: int) -> Optional[Product]:
        goods = self._find_goods(goods_id)
        if goods:
            self._log_operation("QUERY", goods_id, "查询货物信息")
        return goods

    def query_operation_logs(self, goods_id: int = None):
        if goods_id:
            logs = [log for log in self.operation_logs if log.get('goods_id') == goods_id]
        else:
            logs = self.operation_logs.copy()

        self._log_operation("QUERY", goods_id or "ALL", "查询操作记录")
        return logs

    def update_goods_info(self, goods_id: int, **kwargs) -> bool:
        goods = self._find_goods(goods_id)
        if not goods:
            return False

        # 更新属性
        for key, value in kwargs.items():
            if hasattr(goods, key):
                setattr(goods, key, value)

        self._log_operation("UPDATE", goods_id, f"更新货物信息: {kwargs}")
        return True

    def _find_goods(self, goods_id: int) -> Optional[Product]:
        for goods in self.goods:
            if goods.id == goods_id:
                return goods
        return None

    def _find_warehouse(self, warehouse_id: int) -> Optional[Warehouse]:
        for warehouse in self.warehouses:
            if warehouse.id == warehouse_id:
                return warehouse
        return None

    def _log_operation(self, operation_type: str, goods_id: int, description: str):
        log = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operation": operation_type,
            "goods_id": goods_id,
            "description": description
        }
        self.operation_logs.append(log)

    def stock_in(self, goods_id: int, warehouse_id: int):
        goods = self._find_goods(goods_id)
        warehouse = self._find_warehouse(warehouse_id)

        if not goods or not warehouse:
            return False

        if warehouse.category != '*' and goods.category != warehouse.category:
            print(f"错误: 货物类别'{goods.category}'与仓库类别'{warehouse.category}'不匹配")
            return False

        best_location = warehouse.find_best_location(goods.length, goods.width)
        if not best_location:
            return False

        if goods.warehouse_id and goods.warehouse_id != warehouse_id:
            self.stock_out(goods_id)

        best_location.place_goods(goods_id, goods.length, goods.width)
        goods.warehouse_id = warehouse_id
        goods.location_id = best_location.location_id

        self._log_operation("STOCK_IN", goods_id, f"入库到仓库{warehouse_id}, 位置{best_location.location_id}")
        return True

    def stock_out(self, goods_id: int) -> bool:
        goods = self._find_goods(goods_id)
        self._log_operation("STOCK_OUT", goods_id, f"{goods.name} 出库")
        warehouse = self._find_warehouse(goods.warehouse_id)
        location_id = goods.warehouse_id
        if not goods or not warehouse:
            return False
        warehouse.storage_locations[location_id].remove_goods(goods.id)
        return True
