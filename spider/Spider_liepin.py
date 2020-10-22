# coding:utf-8
# 这里面是爬猎聘网的代码
# @auther jinyu
# @date 2020-09-24

import requests
import random
import re
import os
import time
import pandas as pd
import jieba
from jieba import analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from SpiderData import *


class MySpider:
    # 爬虫-猎聘网

    targetName = 'liepin'

    targetDir = '/docs/data/'

    # 猎聘网基础url
    url = 'https://www.liepin.com/zhaopin/?'
    # 待爬取的职位
    jobs = ['数据挖掘', '图像算法工程师', 'java后端', '互联网产品经理']
    # 待爬取的城市,和对应的dqs
    citys = ['北京', '上海', '深圳', '广州', '武汉', '杭州']
    cityIds = ['010', '020', '050090', '050020', '170020', '070020']

    # 用于匹配职位链接的Regular express
    regExpUrl = '<a[^>]*href=\"(https://www.liepin.com/job[^"]*)\"[^>]*'
    # 用于匹配职位
    regExpRequire = '<div class=\"content content-word\">[\s\S]*?(?<=任职资格|任职要求)[:：]?([\s\S]*?)(?<=<br/>)?</div>'

    def __init__(self) -> None:
        self.init()

    def UA(self):
        """ 随机生成合适的UA,用于设置爬虫的参数 """
        ua = random.choice(uapools)
        return {'User-Agent': ua}

    def init(self):
        if(not os.path.exists(os.getcwd()+'/spider/data')):
            os.mkdir(os.getcwd()+'/spider/data')

    def run(self):
        # 爬取职位详情

        try:
            for job in self.jobs:
                # 选择不同的城市e
                print('当前职位:', job)

                url_target = self.url+'key='+job

                f = open(os.getcwd()+'/spider/data/' +
                         self.targetName+'_Job-'+job+'.csv', 'w')
                f.write('"url","city"\n')

                for i in range(len(self.citys)):
                    # 选择不同的城市

                    # 当前已经爬取的职位
                    jobNum = 0

                    # 当前的爬取页面
                    curPage = 0

                    while jobNum < 100:
                        url_target_final = url_target+'&dqs=' + \
                            self.cityIds[i]+'&curPage='+str(curPage)

                        print('当前爬取的url:', url_target_final)

                        # 通过requests的get方法爬取数据，自动切换User-agents
                        data_orgin = requests.get(
                            url=url_target_final, headers=self.UA())

                        # 将爬取到的信息用utf-8编码
                        data_html = data_orgin.content.decode("utf-8")

                        # 判断是是否成功爬取到了html内容
                        if '<!DOCTYPE html>' in data_html and job in data_html:
                            print('get data success!')
                        else:
                            print('get data failed!')

                        # 通过正则表达式获取职位url
                        data_reGet = re.compile(
                            self.regExpUrl).findall(data_html)

                        for url_a in data_reGet:
                            print(url_a)
                            f.write(url_a+' , '+self.citys[i]+' \n')
                            jobNum = jobNum+1
                            time.sleep(0.01)

                        curPage = curPage+1
                        if curPage > 20:
                            jobNum = 1000
                time.sleep(random.randint(1, 4))
                f.close()

        except IOError:
            print('无法建立csv文件')
        except Exception as e:
            print(e.args)
        finally:
            print('Get url finish!')

        print('run end')

    def run_getDetail(self):
        # 获取职位细节

        # 最多爬的url
        maxNum = 5

        for job in self.jobs:
            # 遍历各个职位
            print('当前职位:', job)

            for city in self.citys:
                try:
                    csvData = pd.read_csv(
                        os.getcwd()+'/spider/data/'+self.targetName+'_Job-'+job+'.csv')

                    f = open(os.getcwd()+'/spider/data/' +
                             self.targetName+'_require-'+job+'_city-'+city+'.txt', 'w')

                    numOfUrl = 0

                    for i in range(csvData.shape[0]):

                        if numOfUrl > maxNum:
                            break

                        # 判断当前是否到了当前城市
                        if(not city in csvData.city[i]):
                            continue

                        numOfUrl = numOfUrl+1

                        url_target_final = csvData.url[i]

                        url_target_final = str(
                            url_target_final).replace(' ', '')

                        # 通过requests的get方法爬取数据，自动切换User-agents
                        data_orgin = requests.get(
                            url=url_target_final, headers=self.UA())

                        # 将爬取到的信息用utf-8编码
                        data_html = data_orgin.content.decode("utf-8")

                        # 判断是是否成功爬取到了html内容
                        if '<!DOCTYPE html>' in data_html and job in data_html:
                            print('get '+url_target_final+'data success!')
                        else:
                            print('get '+url_target_final+' data failed!')

                        # 通过正则表达式获取职位要求
                        data_reGet = re.compile(
                            self.regExpRequire).findall(data_html)

                        # 输出匹配到的结果
                        for data_detail in data_reGet:
                            theStr = str(data_detail)
                            if(theStr != ''):
                                theStr = theStr.replace('<br/>', '\n')
                                f.write(theStr)
                                print(theStr)
                        time.sleep(0.1)

                    time.sleep(random.randint(1, 5)*0.1)
                    f.close()
                except IOError:
                    print('找不到职位的csv文件，请先运行run()方法')
                except Exception as e:
                    print(e.args)
                finally:
                    print('Get detail finish!')

        print('run_getDetail end')

    def processData(self):
        # 对职位细节进行数据清洗

        # 词云关键词提取权重,越小越少
        MyTopK = 100

        try:
            for job in self.jobs:

                print('当前职位:', job)

                for city in self.citys:

                    f = open(os.getcwd()+'/spider/data/' +
                             self.targetName+'_keyword-'+job+'_city-'+city+'.txt', 'w')

                    str_jobRequire = str()

                    with open(os.getcwd()+'/spider/data/' +
                              self.targetName+'_require-'+job+'_city-'+city+'.txt') as txtFile:
                        while(True):
                            str_line = txtFile.readline()

                            if not str_line:
                                break

                            str_jobRequire = str_jobRequire+str_line

                    str_jobRequire = str_jobRequire.replace('\n\n', '\n')
                    str_jobRequire = str_jobRequire.replace(' ', '')

                    # 去除序号与结尾
                    str_jobRequire = re.sub(
                        r'([0-9 a-z]+[\.\、,，)）])|（ [0-9]+ ）|[;；]', '', str_jobRequire)

                    # 去除不重要的标点
                    str_jobRequire = re.sub(r'[，、。【】（）/]', ' ', str_jobRequire)

                    # 结巴分词
                    # keywords = jieba.cut(str_jobRequire,cut_all=False)

                    # TF-IDF
                    TF_IDF = analyse.extract_tags
                    keywords = TF_IDF(str_jobRequire, topK=MyTopK)

                    num_word = 0

                    for key in keywords:
                        print(key, end=' ')
                        num_word = num_word+1
                        f.write(key+' ')
                        if num_word % 10 == 0:
                            f.write('\n')

                    f.write('\n')

                    print('\n\n')

                    f.close()

                time.sleep(0.1)
        except IOError as e:
            print('无法打开职位细节文件,请提前运行run_getDetail()')
        except Exception as e:
            print(e.args)
        finally:
            print('processData finish!')

        print('processData end')

    def createWordCloud(self):
        try:
            for job in self.jobs:
                for city in self.citys:

                    with open(os.getcwd()+'/spider/data/' +
                              self.targetName+'_keyword-'+job+'_city-'+city+'.txt', 'r') as txtFile:
                        str_keyword = str()

                        while(True):
                            str_line = txtFile.readline()
                            if not str_line:
                                break
                            if str_line == '':
                                continue
                            str_keyword = str_keyword + str_line

                        print(str_keyword)

                        wordcloud = WordCloud(font_path='./font/PingFang.ttc',
                                              background_color="white").generate(str_keyword)

                        plt.imshow(wordcloud, interpolation='bilinear')
                        plt.axis("off")
                        # plt.show()

                        plt.savefig(os.getcwd() + self.targetDir +
                                    self.targetName+'_wordCloud-'+job+'_city-'+city+'.png')

        except IOError:
            print('Open File Error')

        except Exception as e:
            print(e.args)
        finally:
            print('createWordCloud Finish!')

        print('createWordCloud end')

    def setTime():
        pass


if __name__ == '__main__':
    # 创建爬虫对象
    spider = MySpider()

    # 爬取职位url
    # spider.run()

    # 爬取职位细节,在这一步之前请先运行MySpider的run()方法
    spider.run_getDetail()

    # 对职位细节进行数据清洗
    spider.processData()

    # 根据职位keyword生成词云
    spider.createWordCloud()
