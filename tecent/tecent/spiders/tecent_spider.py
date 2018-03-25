# -*- coding: utf-8 -*-
import scrapy
from tecent.items import TecentSpiderItem


class TecentSpiderSpider(scrapy.Spider):
    name = 'tecent'
    allowed_domains = ['tecent.com']

    url = "https://hr.tencent.com/position.php?&start="

    off_set = 0

    start_urls = [url + str(off_set)]

    def parse(self, response):
        info = response.xpath('//tr[@class="even"]|//tr[@class="odd"]')

        # 初始化模型
        item = TecentSpiderItem()
        for each in info:
            item['name'] = each.xpath('./td[1]/a/text()').extract()[0]
            item['link'] = each.xpath('./td[1]/a/@href').extract()[0]
            # item['type'] = each.xpath('./td[2]/text()').extract()[0]
            item['num'] = each.xpath('./td[3]/text()').extract()[0]
            item['pos'] = each.xpath('./td[4]/text()').extract()[0]
            item['time'] = each.xpath('./td[5]/text()').extract()[0]

            yield item

        if self.off_set < 3870:
            self.off_set += 10

        yield scrapy.Request(self.url + str(self.off_set), callback=self.parse, dont_filter=True)
