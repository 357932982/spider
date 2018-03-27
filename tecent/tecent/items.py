# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TecentSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    type = scrapy.Field()
    num = scrapy.Field()
    pos = scrapy.Field()
    time = scrapy.Field()


class CrawltencentSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    type = scrapy.Field()
    num = scrapy.Field()
    pos = scrapy.Field()
    time = scrapy.Field()
