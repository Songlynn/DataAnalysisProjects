from bs4 import BeautifulSoup
import requests

class Athlete:
    def __init__(self, info):
        self.name, self.name2 = self.get_name_from_info(info)
        lis = info.find_all('li')
        self.sex = self.get_item_info(lis, "性别")
        self.country = self.get_item_info(lis, "国家")
        self.birth = self.get_item_info(lis, "出生日期")
        self.height = self.get_item_info(lis, "身高")
        self.weight = self.get_item_info(lis, "体重")
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

    def print_item(self):
        print(self.name, self.name2, self.sex, self.country, self.birth, self.height, self.weight, self.event, self.native, self.register)

class DataSpider:
    baseUrl = 'http://info.2016.163.com'
    headers = {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
    }

    def __init__(self):
        self.alphabetUrls = []
        self.athletes = []

    # 获取每个字母的url
    def get_alphabet_urls(self):
        res = requests.get(self.baseUrl + '/athlete/list/', headers=self.headers)
        soup = BeautifulSoup(res.text, 'lxml')
        body_soup = soup.html.body
        a_list = body_soup.select('.RScrollNav-filer2.fixed-width ul > li a')
        for item in a_list:
            self.alphabetUrls.append(item['href'])

    # 获取运动员的信息
    def get_athlete_info(self, url):
        res = requests.get(self.baseUrl + url, headers=self.headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        body_soup = soup.html.body
        info = body_soup.select('.brief .table')[0]
        athlete = Athlete(info)
        self.athletes.append(athlete)

    # 获取每个字母下的运动员
    def get_each_alphabet(self, url):
        res = requests.get(self.baseUrl + url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'lxml')
        body_soup = soup.html.body
        a_list = body_soup.select('.athlete_item li div a')
        for item in a_list:
            self.get_athlete_info(item['href'])

    # 获取所有运动员
    def get_athletes(self):
        for url in self.alphabetUrls:
            self.get_each_alphabet(url)
        print(len(self.athletes))

data = DataSpider()
data.get_alphabet_urls()
data.get_athletes()

