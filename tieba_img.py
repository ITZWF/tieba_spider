import requests
from lxml import etree
import os


def down_img(img_htmls, path):
    for img_html in img_htmls:
        img = requests.get(img_html)
        img_name = img_html.split('/')[-1]
        for block in img.iter_content(1024):
            if not block:
                break
            with open(path + img_name, 'wb+') as fw:
                fw.write(img.content)
        print('downloading    ', img_name)


def get_tzs(tz_url):
    if not tz_url.startswith('/'):
        pass
    else:
        tz_url = 'https://tieba.baidu.com' + tz_url
        tz = requests.get(tz_url)
        cont = tz.content
        tz_html = etree.HTML(cont)
        tz_more = tz_html.xpath('//img[@class="BDE_Image"]/@src')
        return tz_more


def get_tz_urls(start, end, url, kw):
    for page in range(start, end + 1):
        info = {
            'kw': kw,
            'pn': str((page - 1) * 50)
        }
        url = requests.get(url=url, params=info)
        print(url.url)
        content = url.content
        html = etree.HTML(content)
        tz_urls = html.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')
        return tz_urls


def start():
    tb_url = 'https://tieba.baidu.com/f?'
    kw = input('请输入关键字: ')
    start_pn = int(input('请输入起始页码: '))
    end_pn = int(input('请输入结束页码: '))
    path = './test_tb/'
    if not os.path.exists(path):
        os.makedirs(path)
    tz_urls = get_tz_urls(start_pn, end_pn, tb_url, kw)
    # print(tz_urls)
    for tz_url in tz_urls:
        tzs = get_tzs(tz_url)
        # print(tzs)
        down_img(tzs, path)
    print('finished')


if __name__ == '__main__':
    start()
