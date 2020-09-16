import requests
from bs4 import BeautifulSoup

# 搜索关键字为“数据挖掘”，工作地区为北京的url
# dps为工作地区的参数，010为猎聘网为北京地区指定的区域号
url="https://www.liepin.com/zhaopin/?key=数据挖掘&dqs=010"

# 发起访问请求
page = requests.get(url = url)
# 输出返回信息 
print(page.url)
# 初始化 soup 对象,page.text为爬取到的带有html标签页面
soup = BeautifulSoup(page.text,"html.parser")
# 找到<h3>标签，实质是获取所有包含职位名称及链接的标签内容
soup = soup.find_all("h3")
#在每个<h3>中进行抽取链接信息
times =0
for i in soup:
	#有些<h3>标签不包含求职信息，做简要判断
    if i.has_attr("title"):
	    #抽取链接内容
        href=i.find_all("a")[0]["href"]
        print(href)
    if times ==1 :
        print("i = -----")
        print(i)

    times=times+1
