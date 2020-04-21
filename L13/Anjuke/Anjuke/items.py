# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class AnjukeItem(Item):
    province = Field()
    city = Field()
    date = Field()
    price = Field()
    compare = Field()
    update_time = Field()
