# -*- coding: utf-8 -*-
import scrapy

from job_spider.items import JobSpiderItem

class JobSpider(scrapy.Spider):
    name = 'job'
    
    #重写开始爬取的函数
    def start_requests(self):
        #已获取的地区代码
        area_code = {'北京': '010000', '上海': '020000', '广州': '030200', '深圳': '040000', '武汉': '180200', '西安': '200200', '杭州': '080200', '南京': '070200', '成都': '090200', '重庆': '060000', '东莞': '030800', '大连': '230300', '沈阳': '230200', '苏州': '070300', '昆明': '250200', '长沙': '190200', '合肥': '150200', '宁波': '080300', '郑州': '170200', '天津': '050000', '青岛': '120300', '济南': '120200', '哈尔滨': '220200', '长春': '240200', '福州': '110200', '珠三角': '01'}

        #网页的链接，关键词位置用{}代替，留待格式化
        url = 'https://search.51job.com/list/{}000000,0000,00,9,99,{}2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

        #定义最大页面数
        MAX_PAGE = 20

        #定义需要爬取的地区列表，列表里可以有多个地区
        area_list = ['北京', '上海']

        #定义职位名
        position = '会计' + ','

        if len(area_list) == 1:
            final_area = area_code[area_list[0]] + ','
        #若地区大于1个，把地区代码用%252C拼接起来
        else:
            final_area = '%252C'.join([area_code[area] for area in area_list]) + ','

        #遍历所有页面
        for page in range(1, MAX_PAGE+1):
            yield scrapy.Request(url.format(final_area, position, page), self.parse)

    def parse(self, response):
        
        #找到职位页面的链接
        a_list = response.xpath('.//div[@class="el"]/p/span/a/@href').extract()

        #遍历所有链接
        for a in a_list:
            yield scrapy.Request(a, self.get_data)

    #定义获取数据的函数
    def get_data(self, response):
        #定义存放数据的item
        item = JobSpiderItem()

        #获取公司名
        item['company'] = response.xpath('.//p[@class="cname"]/a/@title').extract_first()

        #获取链接
        item['url'] = response.url
        
        #获取职位名
        item['title'] = response.xpath('.//h1/@title').extract_first()

        #获取工资
        item['salary'] = response.xpath('.//div[@class="cn"]/strong/text()').extract_first()

        #获取职位描述
        job_description = ''.join(response.xpath('.//div[@class="bmsg job_msg inbox"]/*/text()').re('[\S]*'))

        if job_description:
            item['job_description'] = job_description
        else:
            item['job_description'] = ''.join(response.xpath('.//div[@class="bmsg job_msg inbox"]/text()').re('[\S]*'))

        #返回item
        yield item

                
        
        
