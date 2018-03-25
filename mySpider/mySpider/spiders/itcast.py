# -*- coding: utf-8 -*-
import scrapy

from mySpider.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml',
                  'http://www.itcast.cn/channel/teacher.shtml#apython']

    def parse(self, response):
        # file_name = "teacher.html"
        # open(file_name, "wb").write(response.body)
        response_info = response.xpath('//div[@class="li_txt"]')

        items = []

        for each in response_info:
            # 将得到的数据封装到一个ItcastItem对象中去
            item = ItcastItem()
            name = each.xpath('h3/text()').extract()
            title = each.xpath('h4/text()').extract()
            info = each.xpath('p/text()').extract()

            item['name'] = name[0]
            item['title'] = title[0]
            item['info'] = info[0]

            items.append(item)

            yield item
        # return items
