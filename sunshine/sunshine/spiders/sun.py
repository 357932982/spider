# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sunshine.items import CrawlsunItem


class SunSpider(CrawlSpider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']

    # 每一页的匹配规则
    pagelink = LinkExtractor(allow='type=4')
    # 每个帖子的匹配规则
    contentlink = LinkExtractor(allow=r'/html/question/\d+/\d+.shtml')

    rules = (
        Rule(pagelink, process_links='deal_links', follow=True),
        Rule(contentlink, callback='parse_item'),
    )

    def deal_links(self, links):
        # for each in links:
            # each.url = each
            # print(each.url)
        return links

    def parse_item(self, response):
        item = CrawlsunItem
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
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
