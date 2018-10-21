#! /bin/usr/python3
# 电影天堂爬虫实战

import requests
from lxml import etree
from dyttspider.dyttcategoryallurls import DyttCategoryAllUrls

# 电影天堂主网址，注意：最新电影、经典电影、国内电影、欧美电影均跳转到阳光电影http://www.ygdy8.net
YGDYURL = 'http://www.ygdy8.net/'
DYTTURL = 'http://www.dytt8.net'

# 代理IP地址
PROXY = {
    'http': '106.75.164.15:3128'
}

# 请求头信息
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
}

# 爬取的信息存放在指定的目录下。
INFO_DIR = './info/'

# 主页下的分类信息存放的文件地址
CATEGORY_INFO_DIR = INFO_DIR + 'dytt_category_urls.txt'

# 各个分类信息的存放目录字典
DIR = {'zuixinyingpian_dir': INFO_DIR + 'zuixinyingpian/',
       'jingdianyingpian_dir': INFO_DIR + 'jingdianyingpian/',
       'guoneidianying_dir': INFO_DIR + 'guoneidianying/',
       'oumeidianying_dir': INFO_DIR + 'oumeidianying/',
       'qitadianying_dir': INFO_DIR + 'qitadianying/',
       'huayudianshi_dir': INFO_DIR + 'huayudianshi/',
       'oumeidianshi_dir': INFO_DIR + 'oumeidianshi/',
       'zuixinzongyi_dir': INFO_DIR + 'zuixinzongyi/',
       'jiubanzongyi_dir': INFO_DIR + 'jiubanzongyi/',
       'dongmanziyuan_dir': INFO_DIR + 'dongmanziyuan/',
       'jiubanyouxi_dir': INFO_DIR + 'jiubanyouxi/',
       'youxixizai_dir': INFO_DIR + 'youxixiazai/'}


def dytt_first_page(dytt_url):
    """
    读取电影天堂的主页上的分类信息
    并将分类信息的网址存储到指定的文件-CATEGORY_INFO_DIR。

    使用方法：将想要爬取的类别判断语句中的continue语句注释，并将以下三行取消注释
    可以尝试一次性爬取多个类别，请保证网速！！！
    尝试同时爬取所有类别：由于自身网速不佳，测试过程中，常常发生请求失败！！！
    同时间只爬取一个类别是可以的！！！

    :param dytt_url: 电影天堂的主网址URL
    :return:
    """
    print('spider info: start spider dytt first page !')
    dytt_first_page = requests.get(dytt_url, headers=HEADERS, proxies=PROXY)
    dytt_first_page_html = etree.HTML(dytt_first_page.content.decode('gbk'))
    dytt_category_info = dytt_first_page_html.xpath('//div[@id="menu"]//div[@class="contain"]//a')
    print('spider info: finish spider category urls !')
    with open(CATEGORY_INFO_DIR, 'w', encoding='utf-8') as fp:
        for index, info in enumerate(dytt_category_info):
            if index >= 12:
                break
            elif index >= 4:
                url = DYTTURL + info.xpath('./@href')[0]
            else:
                url = info.xpath('./@href')[0]
            category = info.xpath('./text()')[0]
            fp.write(category + ' : ' + url + '\n')
            if category == '最新影片':
                # 类型标志：1
                # continue
                zuixinyingpian_dir = DIR['zuixinyingpian_dir']
                category = DyttCategoryAllUrls(url, zuixinyingpian_dir, headers=HEADERS, proxy=PROXY, type_flag=1)
                category.start()
            elif category == '经典影片':
                # 类型标志：1
                # 由于经典影片下是排行榜，这里不再深入爬取经典影片
                continue
            elif category == '国内电影':
                # 类型标志：1
                continue
                # guoneidianying = DIR['guoneidianying_dir']
                # category = DyttCategoryAllUrls(url, guoneidianying, headers=HEADERS, proxy=PROXY, type_flag=1)
                # category.start()
            elif category == '欧美电影':
                # 类型标志：1
                continue
                # oumeidianying = DIR['oumeidianying_dir']
                # category = DyttCategoryAllUrls(url, oumeidianying, headers=HEADERS, proxy=PROXY, type_flag=1)
                # category.start()
            elif category == '其它电影':
                # 类型标志：1
                continue
                # qitadianying = DIR['qitadianying_dir']
                # category = DyttCategoryAllUrls(url, qitadianying, headers=HEADERS, proxy=PROXY, type_flag=1)
                # category.start()
            elif category == '华语电视':
                # 类型标志：2
                continue
                # huayudianshi = DIR['huayudianshi_dir']
                # category = DyttCategoryAllUrls(url, huayudianshi, headers=HEADERS, proxy=PROXY, type_flag=2)
                # category.start()
            elif category == '欧美电视':
                # 类型标志：2
                continue
                # oumeidianshi = DIR['oumeidianshi_dir']
                # category = DyttCategoryAllUrls(url, oumeidianshi, headers=HEADERS, proxy=PROXY, type_flag=2)
                # category.start()
            elif category == '最新综艺':
                # 类型标志：2
                continue
                # zuixinzongyi = DIR['zuixinzongyi_dir']
                # category = DyttCategoryAllUrls(url, zuixinzongyi, headers=HEADERS, proxy=PROXY, type_flag=2)
                # category.start()
            elif category == '旧版综艺':
                # 类型标志：2
                continue
                # jiubanzongyi = DIR['jiubanzongyi_dir']
                # category = DyttCategoryAllUrls(url, jiubanzongyi, headers=HEADERS, proxy=PROXY, type_flag=2)
                # category.start()
            elif category == '动漫资源':
                # 类型标志：2
                continue
                # dongmanziyuan = DIR['dongmanziyuan_dir']
                # category = DyttCategoryAllUrls(url, dongmanziyuan, headers=HEADERS, proxy=PROXY, type_flag=2)
                # category.start()
            elif category == '旧版游戏':
                # 类型标志：3
                continue
                # jiubanyouxi = DIR['jiubanyouxi_dir']
                # category = DyttCategoryAllUrls(url, jiubanyouxi, headers=HEADERS, proxy=PROXY, type_flag=3)
                # category.start()
            elif category == '游戏下载':
                # 类型标志：3
                continue
                # youxixiazai = DIR['youxixizai_dir']
                # category = DyttCategoryAllUrls(url, youxixiazai, headers=HEADERS, proxy=PROXY, type_flag=3)
                # category.start()
            else:
                continue


def main():
    dytt_first_page(DYTTURL)


if __name__ == '__main__':
    """
    程序入口
    """
    main()
