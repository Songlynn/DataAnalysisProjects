import requests     # 模拟请求
import re   # 正则表达式
import json

class NationalDaySpider:
    baseUrl = 'http://zhishu.sogou.com/index/searchHeat'
    addresses = [
        "布达拉宫", "稻城亚丁", "故宫", "张家界", "九寨沟", "丽江古城", "雅鲁藏布江大峡谷", "乐山大佛", "万里长城",
        "宏村", "鼓浪屿", "婺源", "纳木错", "外滩", "三清山","三亚", "乌镇", "凤凰古城", "峨眉山", "青海湖", "黄山",
        "洱海", "元阳梯田", "长白山天池", "周庄", "桂林", "长江三峡", "呼伦贝尔", "月牙泉", "颐和园", "黄果树瀑布",
        "华山", "阿坝", "壶口瀑布", "龙脊梯田", "维多利亚港", "香格里拉", "泸沽湖", "鸟巢", "可可西里", "秦始皇兵马俑",
        "西双版纳", "趵突泉", "大连", "中山陵", "大兴安岭", "大雁塔", "丹霞山", "都江堰", "贺兰山", "夫子庙", "龙虎山",
        "恒山", "衡山", "黄帝陵", "黄龙景区", "晋祠", "井冈山", "喀纳斯", "海口", "楼兰古城", "景德镇", "庐山", "罗平",
        "莫高窟", "帕米尔高原", "平遥古城", "普陀山", "千户苗寨", "曲阜三孔", "日月潭", "三峡大坝", "三星堆遗址",
        "沙坡头", "神农架",  "瘦西湖", "苏州园林", "泰山", "避暑山庄", "太湖", "滕王阁", "五大连池", "武当山", "西湖",
        "阳朔西街", "西塘", "西夏王陵", "雁荡山", "殷墟", "玉龙雪山", "云冈石窟", "千岛湖", "朱家角", "北戴河",
        "自贡恐龙博物馆"
    ]
    urlList = []

    # 拼接url
    def set_url(self):
        for index, address in enumerate(self.addresses):
            # http://zhishu.sogou.com/index/searchHeat?kwdNamesStr={address1,address2...}&timePeriodType=MONTH&dataType=SEARCH_ALL&queryType=INPUT
            if index % 5 == 0:
                url = self.baseUrl + '?kwdNamesStr=' + address
                end = 5 if index + 4 <= len(self.addresses) else len(self.addresses) - index + 1
                for i in range(1, end):
                    url += ',' + self.addresses[index+i]
                url += '&timePeriodType=MONTH&dataType=SEARCH_ALL&queryType=INPUT'
                self.urlList.append(url)

    def get_data(self):
        try:
            self.set_url()
            dayData = []
            monthData = []
            for url in self.urlList:
                print('当前地址为：' + url)
                res = requests.get(url)     # 使用requests模块模拟请求获取数据
                data = re.findall(r'root.SG.data = (.*)}]};', res.text)     # 使用正则表达式re模块获取数据
                total_json = json.loads(data[0] + "}]}")     # 将数据转换为json格式
                print(total_json)
                info_list = total_json["infoList"]      # 景点的总体数据
                pv_list = total_json["pvList"]      # 景点每日的数据

                '''
                数据格式
                total_json = {
                    'infoList': [
                        {
                            'kwdName': xxx, 
                            'kwdSumPv': {
                                'sumPv': xxx
                            } 
                            'avgWapPv': xxx, 
                            'ratioWapChain': xxx, 
                            'ratioMonth': xxx, 
                            'ratioChain': xxx, 
                            'avgPv': xxx, 
                            'ratioWapMonth': xxx
                        },
                        ... ...
                    ],
                    'pvList': [
                        [
                            {
                                'pv': xxx, 
                                'date': xxx, 
                                'kwdId': xxx, 
                                'id': xxx, 
                                'isPeak': xxx, 
                            },
                            ... ...
                        ],  # 地点1
                        [],  # 地点2
                        ... ...
                    ]
                }
                '''

                for index, info in enumerate(info_list):
                    for pvDate in pv_list[index]:
                        dayData.append([info['kwdName'], pvDate['date'], pvDate['pv']])     # 景点名，日期，日访问量
                    monthData.append([info['kwdName'], info['avgPv'], info['kwdSumPv']['sumPv']])   # 景点，平均访问量，总访问量

            return dayData, monthData
        except:
            print('exception')

    # 将数据存储到txt中
    def save_data(self, dayData, monthData):
        f1 = open('dayData.txt', 'w+')
        f1.write('景点, 日期, 日访问量\n')
        for line in dayData:
            f1.write(", ".join('%s' % k for k in line) + '\n')
        f1.close()

        f2 = open('monthData.txt', 'w+')
        f2.write('景点, 平均访问量, 总访问量\n')
        for line in monthData:
            f2.write(", ".join('%s' % k for k in line) + '\n')
        f2.close()

sp = NationalDaySpider()
dayData, monthData = sp.get_data()
sp.save_data(dayData, monthData)
