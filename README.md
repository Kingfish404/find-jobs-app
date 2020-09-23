# Find Jobs APP

使用爬虫爬取职位信息

## 实验题目

1. python环境的安装以及职位详情页链接爬取。
    要求爬取的职位有：数据挖掘,图像算法工程师,java后端,互联网产品经理；每个职位工作地区至少有：北京，上海，深圳，广州，武汉，杭州。有兴趣的同学可以在url添加更多参数即添加更多筛选条件，比如行业，薪资等条件筛选出更精确的信息。最终每个职位要求至少爬取500个详情页链接

2. 爬取职位要求与数据清洗
    将提取的职位要求存储到txt中，每个职位的职位要求以空行进行分割
    对职位要求数据进行清洗，采取分词，特殊符号去除，停用词去除等步骤去除数据中对于当前职位要求无价值的信息

### 加分项

1. 使用代理IP解决网站的反爬虫机制  
2. 根据最终实验清洗出的数据做一下词云、柱状图，饼状图等，即让用户可以直观感受到相应职位的要求  
3. 完善功能形成职位需求分析APP或网页版应用，允许用户随机选择职位、地区、薪资，行业等筛选条件，APP给出最终的词云、柱状图或饼状图分析结果  

## 爬取目标

Boss直聘，据说反爬技术很强
https://www.zhipin.com/wuhan/

前程无忧
https://www.51job.com/

猎聘网
https://www.liepin.com/zhaopin

## 使用的库

[request](https://requests.readthedocs.io/zh_CN/latest/user/quickstart.html)


## 目录
```shell
.
├── README.md
│   ├── data.cpython-38.pyc
│   └── request.cpython-38.pyc
├── example_spider.py
└── spider - 爬虫文件夹
    ├── SpiderData.py
    ├── app.ipynb
    ├── data -最终数据文件夹
    └── smallApp.ipynb
```