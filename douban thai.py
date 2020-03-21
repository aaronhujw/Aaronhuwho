import requests
import re
from requests.exceptions import RequestException

header = {'User-Agent':'#这个地方换成自己浏览器的ua.不懂的话Issues里提呀我教你啊哈哈哈哈'}

def get_page(url):#请求并获取豆瓣250源码
    try:
        response = requests.get(url, headers = header)
        if response.status_code == 200: #成功响应码应为200
            return response.text
        return response.status_code #不成功就打印响应码
    except RequestException:
        return None

def get_parse(html): #进行解析 正则表达式是根据网页源码改写的，照着字典多写写就会了
    parse = re.compile('<div class="title">\s*?<a href=.*?target="_blank">\s*?([\u4e00-\u9fa5].*?)\s*</a>\s*</div>.*?<span class="rating_nums">-?(.*?)</span>.*?<blockquote class="comment">\s*<span>评语：</span>(.*?)\s*</blockquote>\s*</div>', re.S)
    parse_over = re.findall(parse, html)
    for item in parse_over:
        yield item

def save(items):
    for item in items:
        with open('douban thai.txt', 'a', encoding= 'utf-8') as f:
            f.write(item[0]+'\n'+'评分：'+ item[1]+'\n'+'点评：'+ item[2] +'\n'+'\n')

if __name__ == '__main__':
    for num in range(0,75,25):
        url = 'https://www.douban.com/doulist/2472863/'+'?start='+str(num)+'&sort=seq&playable=0&sub_type='
        html = get_page(url)
        items = get_parse(html)
        save(items)
        for item in items:
            print(item)

