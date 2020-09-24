# 这里面是爬猎聘网的代码
# @auther jinyu
# @date 2020-09-24

import requests
import random
import re
import os
import time
import csv
from SpiderData import *

class MySpider:
    # 爬虫-猎聘网

    targetName = 'liepin'

    # 猎聘网基础url
    url = 'https://www.liepin.com/zhaopin/?'

    # 待爬取的职位
    jobs = ['数据挖掘','图像算法工程师','java后端','互联网产品经理']
    # 待爬取的城市,和对应的dqs
    citys = ['北京','上海','深圳','广州','武汉','杭州']
    cityIds = ['010','020','050090','050020','170020','070020']

    # 用于匹配职位链接的Regular express
    regExpUrl = '<a[^>]*href=\"(https://www.liepin.com/job[^"]*)\"[^>]*'

    # 用于匹配职位
    regExpRequire = '<div class=\"content content-word\">[\s\S]*?(?<=任职资格|任职要求)[:：]?([\s\S]*?)</div>'

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
        for job in self.jobs:
            # 选择不同的城市e
            print('当前职位:',job)

            url_target = self.url+'key='+job

            f = open(os.getcwd()+'/spider/data/'+self.targetName+'_Job-'+job+'.csv','w')
            f.write('"url","city"\n')

            for i in range(len(self.citys)):
                # 选择不同的城市

                # 当前已经爬取的职位
                jobNum =0

                # 当前的爬取页面
                curPage=0

                while jobNum<100:
                    url_target_final = url_target+'&dqs='+self.cityIds[i]+'&curPage='+str(curPage)

                    print('当前爬取的url:',url_target_final)

                    # 通过requests的get方法爬取数据，自动切换User-agents
                    data_orgin = requests.get(url=url_target_final,headers=self.UA())

                    # 将爬取到的信息用utf-8编码
                    data_html = data_orgin.content.decode("utf-8")

                    # 判断是是否成功爬取到了html内容
                    if '<!DOCTYPE html>' in data_html and job in data_html:
                        print('get data success!')
                    else:
                        print('get data failed!')
                    
                    # 通过正则表达式获取职位url
                    data_reGet = re.compile(self.regExpUrl).findall(data_html)

                    for url_a in data_reGet:
                        print(url_a)
                        f.write(url_a+' ,'+self.citys[i]+' \n')
                        jobNum=jobNum+1
                        time.sleep(0.01)
                    
                    curPage=curPage+1
                    if curPage>20:
                        jobNum=1000
            time.sleep(random.randint(1,4))
            f.close()

            print('Get url finish!')
    
    def run_getDetail(self):
        # 获取职位细节

        # 最多爬的url
        maxNum = 20
        for job in self.jobs:
            # 遍历各个职位
            print('当前职位:',job)

            with open(os.getcwd()+'/spider/data/'+self.targetName+'_Job-'+job+'.csv') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                numOfUrl = 0
                for row in spamreader:

                    numOfUrl = numOfUrl+1
                    if numOfUrl ==1:
                        # 忽略掉第一行
                        continue
                    elif numOfUrl > maxNum:
                        break
                    
                    url_target_final = row[0]

                    # 通过requests的get方法爬取数据，自动切换User-agents
                    data_orgin = requests.get(url=url_target_final,headers=self.UA())

                    # 将爬取到的信息用utf-8编码
                    data_html = data_orgin.content.decode("utf-8")

                    # 判断是是否成功爬取到了html内容
                    if '<!DOCTYPE html>' in data_html and job in data_html:
                        print('get '+url_target_final+' data success!')
                    else:
                        print('get '+url_target_final+' data failed!')

                    # 通过正则表达式获取职位要求
                    data_reGet = re.compile(self.regExpRequire).findall(data_html)

                    # 输出匹配到的结果
                    for data_detail in data_reGet:
                        theStr = str(data_detail)
                        theStr = theStr.replace('<br/>','\n')
                        print(theStr)

                    time.sleep(0.1)
        
        print('Get detail finish!')

if __name__ == '__main__':
    # 创建爬虫对象
    spider = MySpider()

    # 爬取职位url
    # spider.run()

    # 爬取职位细节,在这一步之前请先运行MySpider的run()方法
    spider.run_getDetail()

