#! /bin/usr/python3
# 电影天堂分类下的所有资源URLS进行爬取
import logging
import threading
import requests
from lxml import etree


class DyttCategoryAllUrls(threading.Thread):
    """
    爬取各分类的主网页中的重要信息。
    1. 分类下有多少页的该类信息
    2. 爬取每页上的电影导航信息
    3. 启动电影详情信息爬虫
    """
    def __init__(self, cur_url, cur_dir, headers, proxy, type_flag):
        """
        初始化分类信息爬虫，接受分类的主网址、存储地址目录、请求头信息、代理IP
        :param cur_url: 当前分类的URL
        :param cur_dir: 当前分类信息的存储地址
        :param headers: 请求头信息
        :param proxy: 请求代理IP
        :param type_flag: 启动线程的类型（电影-1、电视-2、综艺-2、游戏-3）
        """
        threading.Thread.__init__(self)
        self.cur_url = cur_url
        self.base_url = cur_url[0:-10]
        self.cur_dir = cur_dir
        self.headers = headers
        self.proxy = proxy
        self.type_flag = type_flag
        self.log_dir = './info/my.log'
        # 日志模块的构建
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename=self.log_dir, level=logging.DEBUG, format=log_format)

    def run(self):
        """
        对各分类的首页进行资源提取，提取每个分类总共包含的网页数量。
        并调用函数get_movie_urls对每页上的影视资源的URL信息进行提取。
        :return:
        """
        logging.info('category spider info: init category spider from ' + self.cur_url)
        try:
            category_page = requests.get(self.cur_url, headers=self.headers, proxies=self.proxy, timeout=30)
        except:
            logging.error('requests ' + self.cur_url + ' is FAIL!')
            return
        logging.info('category spider info: finish spider info from '  + self.cur_url)
        try:
            category_html = etree.HTML(category_page.content.decode('iso8859-1'))
        except:
            logging.error('lxml analysis ' + self.cur_url + ' is FAIL!')
            return
        pages_urls = category_html.xpath('//select[@name="sldd" and '
                                         '@onchange="location.href=this.options[this.selectedIndex].value;"]//option')
        for info in pages_urls:
            url = self.base_url + info.xpath('./@value')[0]
            self.get_all_urls(url)

    def get_all_urls(self, page_url):
        """
        获取每页上的影视URL信息
        :param page_url:每页的URL
        :return:
        """
        logging.info('request info: start spider movie urls from ' + page_url)
        try:
            page = requests.get(page_url, headers=self.headers, proxies=self.proxy, timeout=30)
        except:
            logging.error('requests ' + page_url + ' is FAIL!')
            return
        logging.info('request info: finish spider movie urls from ' + page_url)
        try:
            page_html = etree.HTML(page.content.decode('iso8859-1'))
        except:
            logging.error('lxml analysis ' + page_url + ' is FAIL!')
            return
        all_urls = page_html.xpath('//div[@class="co_content8"]/ul//table[@class="tbspan" and '
                                     '@style="margin-top:6px" and @width="100%" and @cellspacing="0" '
                                     'and @cellpadding="0" and @border="0"]//a[@class="ulink"]')
        with open(self.cur_dir+'1_all_urls.txt', 'a+', encoding='utf-8') as fp:
            for one_url in all_urls:
                try:
                    url = self.cur_url[0:20] + one_url.xpath('./@href')[0].strip()
                    if url.endswith('index.html'):
                        continue
                    name = one_url.xpath('./text()')[0].encode('iso8859-1').decode('gbk').strip()
                    fp.write(name + '-++-' + url + '\n')
                except:
                    logging.error('make error from ' + page_url + ' when lxml anaylsis get ' + url)
                    continue
                if self.type_flag == 1:
                    self.get_movie_info(url)
                elif self.type_flag == 2:
                    self.get_tv_info(url)
                elif self.type_flag == 3:
                    self.get_game_info(url)
                else:
                    logging.error('type_flag is no exist! from ' + self.cur_url)

    def get_movie_info(self, info_url):
        """
        获取电影的详细信息，类型：电影-1
        根据info_url传送来的具体电影详情页，爬取指定的电影信息
        包括：名称、译名、年代、产地、片长、类型、语言、导演、主演员、下载地址、电影截图
        :param info_url:
        :return:
        """
        movie = {}
        try:
            movie_page = requests.get(info_url, headers=self.headers, proxies=self.proxy, timeout=30)
        except:
            logging.error('requests ' + info_url + ' is FAIL!')
            return
        try:
            movie_html = etree.HTML(movie_page.content.decode('gbk'))
        except:
            logging.error('lxml analysis ' + info_url + ' is FAIL!')
            return
        try:
            movie_info = movie_html.xpath('//div[@id="Zoom"]')[0]
            # 电影下载地址
            movie_download = movie_info.xpath('.//a[1]/text()')[0]
            # 电影宣传海报及图片
            movie_image = movie_info.xpath('.//img//@src')
            # 电影其他信息
            movie_detail_info = movie_info.xpath('.//p//text()')
            for info in movie_detail_info:
                if info.startswith('◎片\u3000\u3000名'):
                    movie_name = info[5:].strip()
                    movie['name'] = movie_name
                elif info.startswith('◎译\u3000\u3000名'):
                    movie_trans_name = info[5:].strip()
                    movie['trans_name'] = movie_trans_name
                elif info.startswith('◎产\u3000\u3000地'):
                    movie_place = info[5:].strip()
                    movie['place'] = movie_place
                elif info.startswith('◎类\u3000\u3000别'):
                    movie_type = info[5:].strip()
                    movie['type'] = movie_type
                elif info.startswith('◎语\u3000\u3000言'):
                    movie_language = info[5:].strip()
                    movie['language'] = movie_language
                elif info.startswith('◎年\u3000\u3000代'):
                    movie_year = info[5:].strip()
                    movie['year'] = movie_year
                elif info.startswith('◎片\u3000\u3000长'):
                    movie_length = info[5:].strip()
                    movie['length'] = movie_length
                elif info.startswith('◎导\u3000\u3000演'):
                    movie_director = info[5:].strip()
                    movie['director'] = movie_director
                elif info.startswith('◎主\u3000\u3000演'):
                    movie_actor = info[5:].strip()
                    movie['actor'] = movie_actor
            movie['download'] = movie_download
            movie['image'] = movie_image
        except:
            logging.error('Make Error when getting info from page - ' + info_url)
            return
        with open(self.cur_dir + '2_all_info.txt', 'a+', encoding='utf-8') as fp:
            fp.write(str(movie) + '\n')

    def get_tv_info(self, info_url):
        """
        获取电视剧详情页中的信息，类型：电视剧、综艺-2
        根据info_url提供的TV详情页中获取相应的信息：名称、年代、产地、集数、类型、语言、导演、主演员、下载地址、海报
        :param info_url:
        :return:
        """
        tv = {}
        try:
            tv_page = requests.get(info_url, headers=self.headers, proxies=self.proxy, timeout=30)
        except:
            logging.error('requests ' + info_url + ' is FAIL!')
            return
        try:
            tv_html = etree.HTML(tv_page.content.decode('gbk'))
        except:
            logging.error('lxml analysis ' + info_url + ' is FAIL!')
            return
        try:
            tv_info = tv_html.xpath('//div[@id="Zoom"]')[0]
            # 获取TV的海报以及图片展现
            tv_image = tv_info.xpath('.//img/@src')
            # 获取TV的每集的下载地址
            tv_downloads_info = tv_info.xpath('.//table//a')
            tv_downloads = {}
            for info in tv_downloads_info:
                tv_downloads[info.xpath('./text()')[0].strip()] = info.xpath('./@href')[0].strip()
            # 获取TV的其他信息
            tv_detail_info = tv_info.xpath('.//p//text()')
            for info in tv_detail_info:
                if info.startswith('◎片\u3000\u3000名'):
                    tv_name = info[5:].strip()
                    tv['name'] = tv_name
                elif info.startswith('◎产\u3000\u3000地'):
                    tv_place = info[5:].strip()
                    tv['place'] = tv_place
                elif info.startswith('◎类\u3000\u3000别'):
                    tv_type = info[5:].strip()
                    tv['type'] = tv_type
                elif info.startswith('◎语\u3000\u3000言'):
                    tv_language = info[5:].strip()
                    tv['language'] = tv_language
                elif info.startswith('◎年\u3000\u3000代'):
                    tv_year = info[5:].strip()
                    tv['year'] = tv_year
                elif info.startswith('◎集\u3000\u3000数'):
                    tv_numbers = info[5:].strip()
                    tv['numbers'] = tv_numbers
                elif info.startswith('◎导\u3000\u3000演'):
                    tv_director = info[5:].strip()
                    tv['director'] = tv_director
                elif info.startswith('◎主\u3000\u3000演'):
                    tv_actor = info[5:].strip()
                    tv['actor'] = tv_actor
            tv['downloads'] = tv_downloads
            tv['image'] = tv_image
        except:
            logging.error('Make Error when getting info from page - ' + info_url)
            return
        with open(self.cur_dir + '2_all_info.txt', 'a+', encoding='utf-8') as fp:
            fp.write(str(tv) + '\n')

    def get_game_info(self, info_url):
        """
        获取游戏详情页信息，类型：游戏-3
        根据info_url传送来的具体游戏详情页，爬取指定的游戏信息
        包括：中文名称、游戏类型、游戏语言、下载地址、游戏截图、游戏简介
        :param info_url: 游戏详情页面URL
        :return:
        """
        game = {}
        try:
            game_page = requests.get(info_url, headers=self.headers, proxies=self.proxy, timeout=30)
        except:
            logging.error('requests ' + info_url + ' is FAIL!')
            return
        try:
            game_html = etree.HTML(game_page.content.decode('gbk'))
        except:
            logging.error('lxml analysis ' + info_url + ' is FAIL!')
            return
        try:
            game_info = game_html.xpath('//div[@id="Zoom"]')[0]
            # 游戏的宣传图和游戏画面图
            game_image = game_info.xpath('.//img/@src')
            # 游戏下载地址（迅雷下载、HTTP下载）
            game_download = game_info.xpath('.//a/text()')[0]
            # 游戏介绍：名称、类型、语言、简介
            game_name_type_language_detail = game_info.xpath('.//p//text()')
            game_detail = ''
            for index, info in enumerate(game_name_type_language_detail):
                if info.strip().startswith('中文名称:'):
                    game_name = info.split(': ')[1].strip()
                    game['name'] = game_name
                elif info.strip().startswith('游戏类型:'):
                    game_type = info.split(': ')[1].strip()
                    game['type'] = game_type
                elif info.strip().startswith('游戏语言:'):
                    game_language = info.split(': ')[1].strip()
                    game['language'] = game_language
                elif info.strip().startswith('游戏简介'):
                    continue
                else:
                    if info.strip().startswith('下载地址'):
                        break
                    game_detail += info.strip('\xa0').strip(' ')

            game['download'] = game_download
            game['image'] = game_image
            game['detail'] = game_detail
        except:
            logging.error('Make Error when getting info from page - ' + info_url)
            return
        with open(self.cur_dir+'2_all_info.txt', 'a+', encoding='utf-8') as fp:
            fp.write(str(game) + '\n')


if __name__ == '__main__':
    """
    测试代码
    """
    # 代理IP地址
    PROXY = {
        'http': '106.75.164.15:3128'
    }
    # 请求头信息
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Referer': 'http://www.ygdy8.net/html/gndy/dyzz/index.html'
    }
    category = DyttCategoryAllUrls('http://www.dytt8.net/html/tv/hytv/index.html', './info/huayudianshi/',
                                   headers=HEADERS, proxy=PROXY, type_flag=2)
    # category.start()
    # 测试获取游戏详情页
    # category.get_game_info('http://www.dytt8.net//html/newgame/20171225/55883.html')
    # 测试获取电影详情页
    # category.get_movie_info('http://www.ygdy8.net/html/gndy/dyzz/20181005/57549.html')
    # 测试获取电视剧详情页
    category.get_tv_info('http://www.dytt8.net/html/tv/hytv/20180926/57526.html#')
