# -*- coding: UTF-8 -*-
import os
import random
import re
import threading
import time

import requests
from bs4 import BeautifulSoup

urlMain = "http://www.nvshenba520.com/"
url = "http://www.nvshenba520.com/page/"
sum = 505
pathd = os.getcwd()
listTitleUrl = []
urltest = 'http://www.nvshenba520.com/luyilu/2020/0511/5344/ '


headers = {
        'Host': 'www.nvshenba520.com',
        'Proxy-Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://www.nvshenba520.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; the_cookie=Tue%20May%2012%202020%2017%3A26%3A22%20GMT%2B0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
}


def getUrl_Title(urlMain1):
    rus = requests.get(url=urlMain1,headers=headers)
    soup = BeautifulSoup(rus.text, 'lxml')
    sumSoup = soup.select('article ')
    for i in sumSoup:
        href_txt = i.select('h2 > a')[0]
        # 获取 连接 与标题
        oneDict = {'href': href_txt['href'], 'title': str(href_txt.get_text()).replace('\r\n', '')}
        listTitleUrl.append(oneDict)
        print(oneDict)

def mkdir(Title):
    title = Title+random.choice('abcdefghyjkh')+random.choice('1234567890')
    os.mkdir(pathd+'\\'+title)
    return pathd+'\\'+title



def getImage(listTitle):
    for x in listTitle:
        urlPage = x['href']
        title = x['title']
        print(urlPage + "   " + title)
        mkdir1 = mkdir(title)
        try:
            rus = requests.get(url=urlPage,headers=headers)
            soup = BeautifulSoup(rus.text, 'lxml')
            nexts = soup.select('body > section > div.content-wrap > div > article > div > ul ')
            #先获取图片 在判断是否有 "下一页"  body > section > div.content-wrap > div > article > div > ul > li.next-page > a

            url1 = urlPage
        except:
            time.sleep(20)

        while True:
            try:
                rus = requests.get(url=url1, headers=headers)
                soup = BeautifulSoup(rus.text, 'lxml')
                nexts = soup.select('body > section > div.content-wrap > div > article')
                pattern = re.compile('src="(.*?)"', re.S)
                items = re.findall(pattern, str(nexts))
            except:
                time.sleep(20)
            for i in items:
                try:
                    ir = requests.get(i, headers=headers)
                    open(mkdir1 + '\\' + str(i).split('/')[-1], 'wb').write(ir.content)
                except:
                    time.sleep(10)
            nexts = soup.select(
                'body > section > div.content-wrap > div > article > div > ul > li.next-page > a ')
            if len(nexts) != 0:
                url1 = nexts[0]['href']
                print(url1)
            else:
                print('到底了')
                break


class MyThread(threading.Thread):
    def __init__(self,arg):
        # 显式的调用父类的初始化函数。
        super(MyThread, self).__init__()
        self.arg=arg


    # 定义每个线程要运行的函数
    def run(self):
        time.sleep(1)
        getImage(self.arg)


if __name__ == '__main__':
    file = open('listTitleUrl.txt')
    fileStr = file.read()
    listTileth = eval(fileStr)
    #getImage(listTileth)
    print(len(listTileth))
    x = 100
    c = []
    for i in range(0,len(listTileth),x):
        if(i == 0):
            print(str(i)+ " "+ str(i+x))
            t = MyThread(listTileth[i:i+x])
            c.append(t)
        else:
            if(i == 3600):
                print(str(i + 1) + " " + str(len(listTileth)))
                t = MyThread(listTileth[i + 1:i + len(listTileth)])
                c.append(t)
                break
            print(str(i+1)+ " "+ str(i+x))
            t = MyThread(listTileth[i + 1: i+x])
            c.append(t)
    for i in c:
        i.start()
    for i in c:
        i.join()




