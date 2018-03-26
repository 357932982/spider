# -*- coding: utf-8 -*-
import scrapy

from sunshine.items import CrawlsunItem


class CrawlsunSpider(scrapy.Spider):
    name = 'crawlsun'
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page='
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        # 取出每个页面里帖子的链接
        links = response.xpath('//td/a[@class="news14"]/@href').extract()
        # 迭代每个发帖子的请求，调用parse_item方法
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)
        # 设置页码终止条件，并且每次发送新的页面请求调用parse方法处理
        if self.offset < 87840:
            self.offset += 30
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    def parse_item(self, response):
        item = CrawlsunItem()
        title1 = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract()[0]
        item['title'] = title1.split("\xa0\xa0")[0].split("：")[-1]
        item['number'] = title1.split(" ")[-1].split(":")[-1]
        content = response.xpath('//div[@class="contentext"]/text()').extract()

        if len(content) == 0:
            item['content'] = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
            # content为列表，通过join方法拼接为字符串，并去除首尾空格
            item['content'] = "".join(content).strip()
        else:
            item['content'] = "".join(content).strip()
        item['url'] = response.url
        yield item
