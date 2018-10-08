from athleteClass import Athlete

from bs4 import BeautifulSoup
import requests
import pandas as pd


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

    def save_athletes(self):
        data = [item.obj_to_list() for item in self.athletes]
        df = pd.DataFrame(data, columns=['name', 'name2', 'sex', 'country', 'birth', 'height(cm)', 'weight(kg)', 'event',
                                         'native', 'register'])
        df.to_csv('athletes.csv', encoding='utf_8_sig', index=False)        # 设置编码方式为utf_8_sig，防止中文乱码

data = DataSpider()
data.get_alphabet_urls()
data.get_athletes()
data.save_athletes()

# 数据爬取后，做了一定的操作，但有部分数据在网页上不规范且其量很小，所以可以手动进行修正
# 如项目字段

