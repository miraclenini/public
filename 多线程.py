import requests
import io
import sys
from bs4 import BeautifulSoup
import re
import threading

# 设置最大线程数
thread_lock = threading.BoundedSemaphore(value=10)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
           'Cookie': 'uuid=5ed8092b-77c1-4004-fb53-8baf27d07526; ganji_uuid=4176103276080253494151; lg=1; antipas=2569n39191084z2Z00236L8IM; clueSourceCode=10103000312%2300; user_city_id=176; sessionid=782d3e59-8141-4798-ef49-47ee12b6c341; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22tbmkbturl%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%2210103000312%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%225ed8092b-77c1-4004-fb53-8baf27d07526%22%2C%22ca_city%22%3A%22xa%22%2C%22sessionid%22%3A%22782d3e59-8141-4798-ef49-47ee12b6c341%22%7D; preTime=%7B%22last%22%3A1567489219%2C%22this%22%3A1566629791%2C%22pre%22%3A1566629791%7D; cityDomain=cq; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A49501122668%7D'}

#发送请求
def getHTMLText(url):
    try:
        html = requests.get(url, headers= headers ,timeout =60)
        html.raise_for_status()
        html.encoding = html.apparent_encoding

        return html.text
    except:
        return '产生异常'

#获取数据
def get_data(html):
    # 解析
    soup = BeautifulSoup(html,'html.parser')
    infos = soup.find('ul',{'class':'carlist clearfix js-top'}).find_all('li')

    with open(r'C:\Users\Administrator\Desktop\guazi\guazi.csv','a',encoding = 'UTF-8') as plt:
        pic_urls = []

        for info in infos:
            # 类型
            leixing = info.find('h2').get_text()
            year = info.find('div',{'class':'t-i'}).get_text()
            year = re.sub(r'|','',year).split('|')[0]  # 竖杠替换
            yuamjia = info.find('div',{'class':'t-price'}).find('p').get_text()
            licheng = year[1]
            try:
                tite = info.find('div',{'class':'t-price'}).find('em').get_text()

            except AttributeError:
                tite = ''
            tupian = info.find('a').find('img')['src']
            pic_urls.append(tupian)   # 图片保存


            plt.write("{},{},{},{},{}\n".format(leixing,year,licheng,yuamjia,tite))

    return pic_urls

# 下载图片
def download_pics(url,n):
    r = requests.get(url)
    with open(r'C:\Users\Administrator\Desktop\guazi\tupian\{}.jpg'.format(n),'wb') as f:
        f.write(r.content)

    # 下载完毕 解锁
    thread_lock.release()

def main():
    #目标
    n = 0
    for i in range(1,47):
        start_url = 'https://www.guazi.com/xa/buy/o'+ str(i) +'r8/#bread'
        html = getHTMLText(start_url)
        pic_urls = get_data(html)
        for url in pic_urls:
            n += 1
            print('正在下载地{}张图片'.format(n))

            # 上锁
            thread_lock.acquire()
            t = threading.Thread(target=download_pics, args=(url,n))
            t.start()




main()
