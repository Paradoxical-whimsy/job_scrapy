# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    #定义公司
    company = scrapy.Field()

    #定义链接
    url = scrapy.Field()

    #定义职位
    title = scrapy.Field()

    #定义工资
    salary = scrapy.Field()

    #定义职位描述
    job_description = scrapy.Field()
