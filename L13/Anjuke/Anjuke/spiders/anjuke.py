# -*- coding: utf-8 -*-
import calendar
import datetime

import scrapy
from scrapy.http import Request

from Anjuke.items import AnjukeItem


class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://www.anjuke.com/fangjia/']

    def parse(self, response):
        # 首页
        for url in response.css('.elem-l > a::attr(href)').extract():
            yield Request(url=url, callback=self.parse_province_list)

    def parse_province_list(self, response):
        # 各省历年数据列表页
        for url in response.css('h3 > a::attr(href)').extract():  # 更多
            yield Request(url, callback=self.parse_city_listl)

    def parse_city_listl(self, response):
        # 各市列表页
        for url in response.css('.boxstyle1 ul > li > a::attr(href)').extract():
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        province = response.css('.crumb > a::text').re('(?:\d+)(.+)(?:房价)')[-1]
        city = response.css('.fjlist-box h3::text').re('\d+年(.+?)房价')[0]
        results = response.css('.boxstyle2')
        for i in results[0].css('ul li'):
            item = AnjukeItem()
            year, month = i.css('b').re('\d+')
            day = calendar.monthrange(int(year), int(month))[1]
            item['date'] = datetime.datetime(int(year), int(month), day).strftime('%Y-%m-%d')
            item['price'] = i.css('span').re('[\d\.]+')[0] if i.css('span').re('[\d\.]+') else None
            item['compare'] = i.css('em::text').extract_first()
            item['province'] = province
            item['city'] = city
            yield item
