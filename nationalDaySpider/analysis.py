from matplotlib import pyplot as plt
import numpy as np

class Analysis:
    data = []
    labels = []

    # 绘制条形图
    def show_figure(self, title, labels, data):
        plt.figure(1)       # 取白纸
        ax = plt.subplot(111)       # 确定绘图范围

        # 绘制条形主体
        # left：条形位置（中心）
        # height：条形高度
        # weight：条形宽度
        rect = plt.bar(left=np.arange(len(data)), height=data, width=0.5, color='blue')

        # 为各条形加上数据标签
        for rec in rect:
            x = rec.get_x()
            height = rec.get_height()
            ax.text(x, height, str(height))

        plt.xlabel('景点')    # 横坐标名称
        plt.ylabel('平均访问量')     # 纵坐标名称
        plt.title(title)        # 条形图标题
        plt.xticks(range(0, len(labels)), labels)       # 横坐标

        # 解决绘图中文不显示
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        plt.show()

    # 读取txt中的数据，按照搜索量从高到低排序
    def get_data(self):
        f = open('monthData.txt', 'r')
        lines = f.readlines()
        lines.pop(0)
        data = []
        for line in lines:
            s = line.split(',')
            data.append([s[0], int(s[1].strip())])
        data = sorted(data, key=lambda item: item[1])
        data.reverse()
        self.data = data

    # 显示条形图
    def show_data(self):
        self.get_data()
        index = 0
        # 每10个景点输出一张条形图
        while index < len(self.data):
            end = index + 10 if index + 10 <= len(self.data) else len(self.data)
            sub_data = [self.data[i][1] for i in range(index, end)]     # 获取10个景点的平均搜索量
            sub_labels = [self.data[i][0] for i in range(index, end)]   # 获取10个景点的名称
            self.show_figure('景点30天内平均搜索量', sub_labels, sub_data)
            index = index + 10

an = Analysis()
an.show_data()