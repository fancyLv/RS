# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import datetime

import pymysql


class AnjukePipeline(object):
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self.sql = """REPLACE INTO price (`province`,`city`,`date`,`price`,`compare`,`update_time`) VALUES (%s,%s,%s,%s,%s,%s)"""

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('HOST', 'localhost'),
            port=crawler.settings.get('PORT', 3306),
            user=crawler.settings.get('USER'),
            password=crawler.settings.get('PASSWORD'),
            database=crawler.settings.get('DATABASE')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                    database=self.database)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        item['update_time'] = datetime.datetime.now()  # datetime.datetime.utcnow()
        self.cur.execute(self.sql, (
            item['province'], item['city'], item['date'], item['price'], item['compare'], item['update_time']))
        self.conn.commit()
        return item
