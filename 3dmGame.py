from bs4 import BeautifulSoup
import requests


"""
url:http://dl.3dmgame.com/pc/click_desc/
思路：爬取排行，获得子url指向游戏页面，获取游戏页面信息得到名称发行商之类信息，获得孙页面获得下载地址。
"""


def fater_url(url):
    # 游戏页面链接获取
    rosepse = requests.get(url)
    soup = BeautifulSoup(rosepse.text,'lxml')

    href = soup.select('div.text > h2 > a')
    for i in href:
        son_url(i.get('href'))


# 进入单个游戏界面
def son_url(url):
    son_rosepse = requests.get(url)
    son_rosepse.encoding = 'utf-8'
    #print(son_rosepse.text)
    #time.sleep(10)
    son_suop = BeautifulSoup(son_rosepse.text, 'lxml')
    game_name = son_suop.select('div.game_wrap > h1')
    down_game = son_suop.select('#xzhzdownurl')# 找到下载页面，进行分析
    hard = 'http://so.hyds360.com'
    for j in down_game:
        # 获取游戏名
        print(game_name[0].text)
        f = open('game.txt', 'a+', encoding='utf-8')
        f.write(game_name[0].text+'\n')
        f.close()
        #加入判断，某些页面的链接会失去“http://so.hyds360.com”的头，手动加上。
        if 'http' in j.get('value'):
            grandson_url(j.get('value'))# 分析下载页面
        else:
            new_url = hard+j.get('value')
            grandson_url(new_url)



def grandson_url(html):
    if len(html):
        grandson_rosepse = requests.get(html)
        grandson_rosepse.encoding = 'utf-8'
        grandson_suop = BeautifulSoup(grandson_rosepse.text, 'lxml')
        grandson_url = grandson_suop.select('a.result_down') # 获取次级下载页面
        if grandson_url != None:
            str = grandson_url[0]['href']
            down_rosepse = requests.get(str)
            down_rosepse.encoding = 'utf-8'
            grandson_suop = BeautifulSoup(down_rosepse.text, 'lxml')
            down = grandson_suop.select('body > div.yxhz_n1_container > div.n1_content > a.gameDown.down_xl')# 获取真实下载页面
            print()
            f = open('game.txt', 'a+', encoding='utf-8')
            if down.__len__() == 0:
                f.write('没有迅雷下载地址！' + '\n')
            else:
                f.write(down[0]['href'] + '\n')
                f.close()

def main_url():
    # 游戏爬取页面，主页面的游戏LIST爬取。
    url = 'http://dl.3dmgame.com/pc/click_desc_'
    Surl = ''
    for i in range(1, 200):
        # 页面轮换
        Surl = url + str(i)
        fater_url(Surl)
    print('爬取完成！')


if __name__ == '__main__':
    #入口
    main_url();
