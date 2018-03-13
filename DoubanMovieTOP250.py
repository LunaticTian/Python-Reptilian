
import requests
from requests.exceptions import RequestException
import re

headers = {
    'Host': 'http://maoyan.com/board/4',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.baidu.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
}

def get_one_page(url):#页数选择
    try:
        response=requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
def parse_one_page(html):
    pattern = re.compile('<img.*?src="(.*?)".*?title">(.*?)</span>.*?"">(.*?)<.p>.*?age">(.*?)</span>.*?<span>(.*?)</span>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        print(item)

def main(url):#主方法

    html = get_one_page(url)
    parse_one_page(html)
    # print(url)

if __name__ == '__main__':
    url = 'https://movie.douban.com/top250?start='
    url1='&filter='
    for i in range(0, 225, 25):
        url3 = url+str(i)+url1
        main(url3)

