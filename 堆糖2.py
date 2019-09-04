import requests
import urllib.parse
import threading

# 设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=10)

def get_page(url):
    page = requests.get(url)
    page = page.content
    # 将byye 转成 字符串
    page = page.decode('utf-8')
    return page

def pages_from_duitang(label):
    pages = []
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw=%E6%A0%A1%E8%8A%B1&type=feed&include_fields=top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Clike_id%2Csender%2Calbum%2Creply_count%2Cfavorite_blog_id&_type=&start=48&_=1567579292388'
    label = urllib.parse.quote(label)
    for index in range(0, 3600, 24):
        u = url.format(label, index)
        print(u)
        page = get_page(u)
        pages.append(page)
    return pages

def findall_in_page(page,startpart, endpart):
    all_strings = []
    end = 0
    while page.find(startpart, end)  != -1:
        start = page.find(startpart, end) + len(startpart)
        end = page .find(endpart,start)
        string = page[start:end]
        all_strings.append(string)
    return all_strings

def pic_urls_from_pages(pages):
    pic_urls = []
    for page in pages:
        urls = findall_in_page(page,'path":"','"')
        pic_urls.extend(urls)
    return pic_urls


def download_pics(url,n):
    r = requests.get(url)
    path = 'pics/' + str(n) + '.jpg'
    with open(path,'wb') as f:
        f.write(r.content)
    #下载完成，解锁
    thread_lock.release()

def main(label):
    pages = pages_from_duitang(label)
    pic_urls = pic_urls_from_pages(pages)
    n = 0
    for url in pic_urls:
        n += 1
        print('正在下载第{}张图片'.format(n))
        # 上锁
        thread_lock.acquire()
        t = threading.Thread(target=download_pics, args=(url, n ))
        t.start()

main()