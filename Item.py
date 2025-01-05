class Item:
    def __init__(self, name, description, address, phone, email, item_type, item_attributes = {}):
        self.name = name
        self.description = description
        self.address = address
        self.phone = phone
        self.email = email
        self.item_type = item_type
        self.attributes = item_attributes
        
    def set_attribute(self, key, value):
        self.attributes[key] = value

    def get_attribute(self, key):
        return self.attributes.get(key, None)

    def __str__(self):
        return f"物品名称: {self.name}, 类型: {self.item_type}, 属性: {self.attributes}"