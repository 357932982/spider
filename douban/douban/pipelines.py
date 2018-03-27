# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class DoubanmoviePipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        db_name = settings["MONGODB_DBNAME"]
        sheet_name = settings['MONGODB_SHEETNAME']

        # 创建数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mysb = client[db_name]
        # 指定存放数据的表名
        self.sheet = mysb[sheet_name]

    def process_item(self, item, spider):
        data = dict(item)
        self.sheet.insert(data)
        return item
