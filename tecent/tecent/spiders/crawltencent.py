# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from tecent.items import TecentSpiderItem


class CrawltencentSpider(CrawlSpider):
    name = 'crawltencent'
    allowed_domains = ['tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0']

    page_lx = LinkExtractor(allow=("start=\d+"))

    rules = (
        Rule(page_lx, callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        for each in response.xpath('//*[@class="even"]|//*[@class="odd"]'):
            try:
                name = each.xpath('./td[1]/a/text()').extract()[0]
            except:
                name = ''
            try:
                link = each.xpath('./td[1]/a/@href').extract()[0]
            except:
                link = ''
            try:
                type = each.xpath('./td[2]/text()').extract()[0]
            except:
                type = ''
            try:
                num = each.xpath('./td[3]/text()').extract()[0]
            except:
                num = ''
            try:
                pos = each.xpath('./td[4]/text()').extract()[0]
            except:
                pos = ''
            try:
                time = each.xpath('./td[5]/text()').extract()[0]
            except:
                time = ''

            item = TecentSpiderItem()
            item['name'] = name
            item['link'] = link
            item['type'] = type
            item['num'] = num
            item['pos'] = pos
            item['time'] = time

            yield item
