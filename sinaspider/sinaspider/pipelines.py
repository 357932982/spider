# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals


class SinaPipeline(object):
    def process_item(self, item, spider):
        son_url = item["son_url"]
        file_name = son_url[7:-6].replace('/', '_') + ".txt"

        with open(item["sub_file_name"] + "/" + file_name, "wb") as f:
            print(item['content'])
            f.write(item['content'].encode())
            f.close()
        return item
