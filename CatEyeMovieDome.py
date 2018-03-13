import requests
import re
import pymysql.cursors

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
##待加入的头文件(防止被检测)

def get_page(url):##将爬取到的数据存入自己的数据库
    html = requests.get(url, headers=headers)
    # Mysql = Set_Mysql()
    # Mysql.add(Mysql.cursor,data)
    connect = pymysql.Connect(
        host='xxx.xxx.xxx.xxx',
        port=3306,
        user='root',
        passwd='root',
        db='Python',
        charset='utf8'
    )
    cursor = connect.cursor()


    for item in requstst_paly(html.text):
        name = item.get('name')
        foot = item.get('foot')
        time = item.get('time')
        mark = item.get('mark')
        img = item.get('img')
        data = (name, foot, time, mark, img)
        sql = "INSERT INTO CatEyeMovie (MovieName, Protagonist, ReleasedTime,Score,Poster) VALUES ( '%s', '%s', '%s','%s','%s')"
        cursor.execute(sql % data)
        print(mark)

    connect.commit()


def requstst_paly(html):##用正则表达式提取信息，使用“yield”创造字典
    pattern = re.compile(
        '<img data-src="(.*?)@.*?".*?"name".*?">(.*?)</a>.*?star">(.*?)</p>.*?time">(.*?)</p>.*?ger">(\d.).*?">(\d)</i>',  re.S)
    items = re.findall(pattern, html)

    for movie in items:
        yield {
            'name': movie[1],
            'foot': movie[2].strip()[3:],
            'time': movie[3].strip()[5:],
            'mark': movie[4] + movie[5],
            'img': movie[0]
        }


def main():
    #遍历网址,网址的目录
    url = 'http://maoyan.com/board/4?offset='
    urlsum=''
    for i in range(0, 100, 10):
        urlsum = url + str(i)
        get_page(urlsum)


if __name__ == '__main__':
    main()