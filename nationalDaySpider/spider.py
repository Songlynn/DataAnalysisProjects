import requests
import re
import json

class NationalDaySpider:
    baseUrl = 'http://zhishu.sogou.com/index/searchHeat'
    addresses = [ \
        "布达拉宫", "稻城亚丁", "故宫", "张家界", "九寨沟", "丽江古城", "雅鲁藏布江大峡谷", "乐山大佛", "万里长城", \
        "宏村", "鼓浪屿", "婺源", "纳木错", "外滩", "三清山","三亚", "乌镇", "凤凰古城", "峨眉山", "青海湖", "黄山", \
        "洱海", "元阳梯田", "长白山天池", "周庄", "桂林", "长江三峡", "呼伦贝尔", "月牙泉", "颐和园", "黄果树瀑布", \
        "华山", "阿坝", "壶口瀑布", "龙脊梯田", "维多利亚港", "香格里拉", "泸沽湖", "鸟巢", "可可西里", "秦始皇兵马俑", \
        "西双版纳", "趵突泉", "大连", "中山陵", "大兴安岭", "大雁塔", "丹霞山", "都江堰", "贺兰山", "夫子庙", "龙虎山", \
        "恒山", "衡山", "黄帝陵", "黄龙景区", "晋祠", "井冈山", "喀纳斯", "海口", "楼兰古城", "景德镇", "庐山", "罗平", \
        "莫高窟", "帕米尔高原", "平遥古城", "普陀山", "千户苗寨", "曲阜三孔", "日月潭", "三峡大坝", "三星堆遗址", \
        "沙坡头", "神农架",  "瘦西湖", "苏州园林", "泰山", "避暑山庄", "太湖", "滕王阁", "五大连池", "武当山", "西湖", \
        "阳朔西街", "西塘", "西夏王陵", "雁荡山", "殷墟", "玉龙雪山", "云冈石窟", "千岛湖", "朱家角", "北戴河", \
        "自贡恐龙博物馆" \
    ]
    urlList = []

    def setUrl(self):
        for index, address in enumerate(self.addresses):
            # http://zhishu.sogou.com/index/searchHeat?kwdNamesStr={address1,address2...}&timePeriodType=MONTH&dataType=SEARCH_ALL&queryType=INPUT
            if index % 5 == 0:
                url = self.baseUrl + '?kwdNamesStr=' + address
                end = 5 if index + 4 <= len(self.addresses) else len(self.addresses) - index + 1
                for i in range(1, end):
                    url += ',' + self.addresses[index+i]
                url += '&timePeriodType=MONTH&dataType=SEARCH_ALL&queryType=INPUT'
                self.urlList.append(url)

    def getData(self):
        try:
            self.setUrl()
            dayData = []
            monthData = []
            for url in self.urlList:
                print('当前地址为：' + url)
                res = requests.get(url)
                data = re.findall(r'root.SG.data = (.*)}]};', res.text)
                totalJson = json.loads(data[0] + "}]}")
                topPvDataList = totalJson['topPvDataList']
                infoList = totalJson["infoList"]
                pvList = totalJson["pvList"]

                for index, info in enumerate(infoList):
                    # info的keys：['kwdName', 'kwdSumPv', 'avgWapPv', 'ratioWapChain', 'ratioMonth', 'ratioChain', 'avgPv', 'ratioWapMonth']
                    # info['kwdSumPv']的key：['sumPv']
                    for pvDate in pvList[index]:
                        # print("index => " + str(index) + "，地址 => " + info["kwdName"] + "，日期 => " + str(
                        #     pvDate["date"]) + " => " + str(pvDate["pv"]) + " => " + str(
                        #     info["avgPv"]) + " => " + str(info["kwdSumPv"]["sumPv"]) + " => ")
                        dayData.append([info['kwdName'], pvDate['date'], pvDate['pv']])     # 景点名，日期，日访问量
                    monthData.append([info['kwdName'], info['avgPv'], info['kwdSumPv']['sumPv']])   # 景点，平均访问量，总访问量

            return dayData, monthData
        except:
            print('exception')

    def saveData(self, dayData, monthData):
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
dayData, monthData = sp.getData()
sp.saveData(dayData, monthData)
