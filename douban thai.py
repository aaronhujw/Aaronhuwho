import requests
import re
from requests.exceptions import RequestException

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

def get_page(url):#请求并获取豆瓣250源码
    try:
        response = requests.get(url, headers = header)
        if response.status_code == 200: #成功响应码应为200
            return response.text
        return response.status_code #不成功就打印响应码
    except RequestException:
        return None

def get_parse(html): #进行解析
    parse = re.compile('<div class="title">\s*?<a href=.*?target="_blank">\s*?([\u4e00-\u9fa5].*?)\s*</a>\s*</div>.*?<span class="rating_nums">-?(.*?)</span>.*?<blockquote class="comment">\s*<span>评语：</span>(.*?)\s*</blockquote>\s*</div>', re.S)
    parse_over = re.findall(parse, html)
    for item in parse_over:
        yield item

def save(items):
    for item in items:
        with open('title.txt', 'a', encoding= 'utf-8') as f:
            f.write(item[0]+""+'评分：'+ item[1]+""+'点评：'+ item[2] +'\n')

if __name__ == '__main__':
    d = {}
    for num in range(0,75,25):
        url = 'https://www.douban.com/doulist/2472863/'+'?start='+str(num)+'&sort=seq&playable=0&sub_type='
        html = get_page(url)
        items = get_parse(html)
        save(items)
        for item in items:
            print(item)
