import re

class Athlete:
    def __init__(self, info):
        self.name, self.name2 = self.get_name_from_info(info)
        lis = info.find_all('li')
        self.sex = self.get_item_info(lis, "性别")
        self.country = self.get_item_info(lis, "国家")
        self.birth = self.get_item_info(lis, "出生日期")
        self.height = self.handle_height(self.get_item_info(lis, "身高"))
        self.weight = self.handle_weight(self.get_item_info(lis, "体重"))
        # self.height = self.get_item_info(lis, "身高")
        # self.weight = self.get_item_info(lis, "体重")
        self.event = self.get_item_info(lis, "项目")
        self.native = self.get_item_info(lis, "籍贯")
        self.register = self.get_item_info(lis, "注册单位")

    # 获取运动员的中文名和英文名
    @staticmethod
    def get_name_from_info(info):
        name_soup = info.h1.contents
        name = name_soup[0]
        name2 = name_soup[1].string
        return name, name2

    # 获取运动员对应的信息，根据不同内容获取，有部分运动员的某类别信息无，则返回None
    @staticmethod
    def get_item_info(lis, typename):
        for li in lis:
            for child in li.descendants:
                if "".join(child).find(typename) >= 0:
                    return li.contents[1] if len(li.contents) >= 2 else None    # 部分运动员的某类信息未显示，需要甄别
        return None

    # 180厘米，180cm，1.83米，170米厘米
    @staticmethod
    def handle_height(item):
        if item and len(item) > 0:
            print(item)
            h = float(re.findall('\d+\.?\d*', item)[0])
            return int(h) if h > 10 else int(h*100)
        else:
            return item

    @staticmethod
    def handle_weight(item):
        if item and len(item) > 0:
            h = re.findall('\d+\.?\d*', item)
            return float(h[0]) if len(h) > 0 else None
        else:
            return item

    def print_item(self):
        print(self.name, self.name2, self.sex, self.country, self.birth, self.height, self.weight, self.event,
              self.native, self.register)

    def obj_to_list(self):
        item = [self.name, self.name2, self.sex, self.country, self.birth, self.height, self.weight, self.event,
                self.native, self.register]
        return item
