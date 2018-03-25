# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class MyspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ItcastPipeline(object):
    # 初始化方法，可选
    def __init__(self):
        # 创建了一个文件
        self.file_name = open("tescher.json", "wb")

    # process_item方法必须写，用来处理item数据
    def process_item(self, item, spider):
        json_text = json.dumps(dict(item), ensure_ascii=False)+'\n'
        self.file_name.write(json_text.encode("utf-8"))

    def close_spider(self, spider):
        self.file_name.close()
