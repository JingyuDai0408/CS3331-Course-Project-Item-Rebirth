class ItemManager:
    def __init__(self):
        self.items = []
        # 初始的物品类型及其属性
        self.item_types = {
            "食品": ["保质期", "数量"],
            "书籍": ["作者", "出版社"],
            "电子产品": ["品牌", "颜色"]
        }
        self.current_user = None

    def add_item(self, item):
        self.items.append(item)

    def delete_item(self, item_name):
        self.items = [item for item in self.items if item.name != item_name]

    def search_item(self, item_type, keyword):
        return [item for item in self.items if item.item_type == item_type and (keyword in item.name or keyword in item.description)]

    def get_all_items(self):
        return self.items
    
    def get_item_types(self):
        """ 获取所有物品类型 """
        return list(self.item_types.keys())
    
    def add_item_type(self, type_name, attributes):
        """ 添加物品类型 """
        if type_name in self.item_types:
            raise ValueError(f"物品类型 {type_name} 已存在！")
        self.item_types[type_name] = attributes

    def update_item_type(self, type_name, attributes):
        """ 修改物品类型 """
        if type_name not in self.item_types:
            raise ValueError(f"物品类型 {type_name} 不存在！")
        self.item_types[type_name] = attributes

    def remove_item_type(self, type_name):
        """ 删除物品类型 """
        if type_name in self.item_types:
            del self.item_types[type_name]
        else:
            raise ValueError(f"物品类型 {type_name} 不存在！")
    
    def get_item_type_attributes(self, type_name):
        """ 获取物品类型的属性 """
        return self.item_types.get(type_name, None)