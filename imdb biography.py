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
    parse = re.compile('<a href="/title/.*?adv_li_tt"\s*>(.*?)</a>.*?"ratings-bar".*?data-value="(.*?)">.*?"text-muted">\s*(.*?)</p>.*?Director:.*?ref_=adv_li_dr_0"\s*>(.*?)</a>', re.S)
    parse_over = re.findall(parse, html)
    for item in parse_over:
        yield item

def save(items):
    for item in items:
        with open('imdb biography.txt', 'a', encoding= 'utf-8') as f:
            f.write(item[0]+'\n'+'director：'+ item[3]+'\n'+'ratings：'+ item[1]+'\n'+'despcriptions:'+item[2] +'\n'+'\n')

if __name__ == '__main__':
    for num in range(1,351,50):
        url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=biography&sort=user_rating,desc&start='+str(num)+'&ref_=adv_nxt'
        html = get_page(url)
        items = get_parse(html)
        save(items)
        for item in items:
            print(item)
