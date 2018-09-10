# tieba_spider
1. 源码思想(这里用的是requests, scripy框架这些以后更新, 最近太累了不更)

import requests
from lxml import etree
import os

# 贴吧的前缀
tb_url = 'https://tieba.baidu.com/f?'
# 输入贴吧的名称
keyword = input('请输入要爬取图片的贴吧: ')
start_pn = int(input('请输入起始页码: '))
end_pn = int(input('请输入结束页码: '))
# 这个 path 现在只是 str 字符串, 用来生成下载图片的位置
path = './source/'
# 如果在软件(py 脚本同一文件夹下木有这个目录, 自动创建)
if not os.path.exists(path):
    os.makedirs(path)
# 循环打开起始到终止页的页码
for page in range(start_pn, end_pn+1):
    # 贴吧需要携带的字头网址数据, 注意 kw 必须要 url encoding , 否则中文无法识别, pn 是页码信息参数
    info = {
        'kw': keyword,
        'pn': (page - 1) * 50,
    }
    # 拼装请求的网址, 在 tb_url 字符串后面增加了携带信息 info, 向拼装完的网址发起请求
    # 在这不要请求头, 要IE垃圾浏览器的请求头才会通过, google firefox的浏览器百毒自动屏蔽
    response = requests.get(url=tb_url, params=info)
    # 得到在ram 里的网页内容数据
    content = response.content

    # 从 xml 处理网页内容
    html = etree.HTML(content)
    # 这是帖子的地址
    # xml 处理的时候 xpath 是处理规则, 相比正则更容易实现
    tie_html = html.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')
    # 循环找到的帖子网页
    for tie in tie_html:
        # 判断网页的开头是不是 /p/ 贴吧掺杂广告, 筛选, pass 不作处理
        if not str(tie).startswith('/p/'):
            pass
        # 帖子的网络地址
        tie_zi_url = 'https://tieba.baidu.com' + str(tie)
        # print(tie_zi_url)
        # 请求帖子的地址
        res = requests.get(tie_zi_url)
        # 返回 ram 里的帖子网页内容
        cont = res.content
        # 同 xml 处理帖子的数据
        img_html = etree.HTML(cont)
        # xml 的出路规则
        img_html = img_html.xpath('//div[contains(@id,"post_content_")]/img[@class="BDE_Image"]/@src')
        # img_html 是列表, 得到每个网址
        for img in img_html:
            # 请求每个网址
            image = requests.get(str(img))
            # 处理得到每张图片的名字, 我是直接切割原始网页的名字, 可以自定义
            img_name = str(img).split('/')[-1]
            # 尝试保存图片, 如果保存失败则不抛出异常, 而是打印异常, 脚本不终止
            try:
                with open(path + img_name, 'wb+') as fw:
                    fw.write(image.content)
                    print('downloading    ', str(img_name))
            except Exception as msg:
                print('出错情况:    ', msg)
print('finished')

2.  更新代码详见py文件  封装了函数