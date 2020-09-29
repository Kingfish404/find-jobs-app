# coding:utf-8
# 这里面是爬boss直聘网的代码
# @auther jinyu
# @date 2020-09-29

import re
import requests
import os
import random
import time
import pandas

from SpiderData import *

class MySpider:
    # 爬虫-boss直聘网

    targetName = 'zhipin'

    targetDir = '/docs/data/'

    def __init__(self) -> None:
        self.init()

    def init(self):
        if(not os.path.exists(os.getcwd()+'/spider/data')):
            os.mkdir(os.getcwd()+'/spider/data')

    def UA(self):
        """ 随机生成合适的UA,用于设置爬虫的参数 """
        ua = random.choice(uapools)
        return {'User-Agent': ua}

    def run(self):
        pass

    def run_getDetail(self):
        pass

    def processData(self):
        pass

    def createWordCloud(self):
        pass

    def setTime(self):
        pass

if __name__ == '__main__':
    # 创建爬虫对象
    spider = MySpider()

    # 爬取职位url
    spider.run()

    # 爬取职位细节,在这一步之前请先运行MySpider的run()方法
    spider.run_getDetail()

    # 对职位细节进行数据清洗
    spider.processData()

    # 根据职位keyword生成词云
    spider.createWordCloud()