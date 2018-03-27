# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanmovieItem


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['movie.douban.com']
    offset = 0
    url = "https://movie.douban.com/top250?start="
    start_urls = [url + str(offset)]

    def parse(self, response):
        item = DoubanmovieItem()
        movies = response.xpath('//div[@class="info"]')

        for each in movies:
            item["title"] = each.xpath('.//span[@class="title"][1]/text()').extract()[0]
            item["bd"] = each.xpath('.//div[@class="bd"]/p/text()').extract()[0]
            item["star"] = each.xpath('.//div[@class="bd"]//span[@class="rating_num"]/text()').extract()[0]
            quote = each.xpath('.//p[@class="quote"]/span/text()').extract()
            if len(quote) > 0:
                item["quote"] = quote
            yield item

        if self.offset < 225:
            self.offset += 25
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

