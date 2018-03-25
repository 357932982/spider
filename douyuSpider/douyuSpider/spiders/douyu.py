# -*- coding: utf-8 -*-
import scrapy
import json

from douyuSpider.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['capi.douyucdn.cn']

    off_set = 0
    url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="

    start_urls = [url + str(off_set)]

    def parse(self, response):
        data = json.loads(response.text)["data"]
        for each in data:
            item = DouyuItem()
            item["nick_name"] = each["nickname"]
            item["image_link"] = each["vertical_src"]

            yield item

        if self.off_set < 800:
            self.off_set += 20

        yield scrapy.Request(self.url + str(self.off_set), callback=self.parse)
