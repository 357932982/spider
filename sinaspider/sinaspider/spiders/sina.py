# -*- coding: utf-8 -*-
import scrapy
import os

from sinaspider.items import SinaspiderItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # 先爬取最外层的标题和url
        items = []
        parent_urls = response.xpath('//div[@id="tab01"]/div/h3/a/@href').extract()
        parent_title = response.xpath('//div[@id="tab01"]/div/h3/a/text()').extract()
        # 再爬去小类的标题和url

        sub_urls = response.xpath('//div[@id="tab01"]/div/ul/li/a/@href').extract()
        sub_title = response.xpath('//div[@id="tab01"]/div/ul/li/a/text()').extract()

        # 最后爬去小类下面的文章的标题和内容
        for i in range(0, len(parent_title)):
            parent_file_name = "./Data/"+parent_title[i]

            # 如果目录不存在则新建
            if not os.path.exists(parent_file_name):
                os.makedirs(parent_file_name)


            # 爬取小类
            for j in range(0, len(sub_title)):
                # 检查小类是否是包含在大类中，判断url开头。
                is_belong = sub_urls[j].startswith(parent_urls[i])

                item = SinaspiderItem()
                # 存储大类
                item["parent_url"] = parent_urls[i]
                item["parent_title"] = parent_title[i]

                if is_belong:
                    sub_file_name = parent_file_name + "/" + sub_title[j]

                    # 如果目录不存在则创建
                    if not os.path.exists(sub_file_name):
                        os.makedirs(sub_file_name)

                    item["sub_url"] = sub_urls[j]
                    item["sub_title"] = sub_title[j]
                    item["sub_file_name"] = sub_file_name

                    items.append(item)

        for item in items:
            yield scrapy.Request(url=item["sub_url"], meta={'meta_1': item}, callback=self.second_parse)

    # 对于小类的url，继续爬取里面的文章
    def second_parse(self, response):
        # 提取上一级爬取的信息
        meta_1 = response.meta['meta_1']

        # 取出小类里面的所有链接
        son_urls = response.xpath('//a/@href').extract()

        items = []
        for i in range(0, len(son_urls)):
            # 检查每个链接是否是以大类的url开头，是否以.shtml结尾
            is_belong = son_urls[i].startswith(meta_1['parent_url']) and son_urls[i].endswith('.shtml')

            item = SinaspiderItem()
            if is_belong:
                item["parent_title"] = meta_1["parent_title"]
                item["parent_url"] = meta_1["parent_url"]
                item["sub_title"] = meta_1["sub_title"]
                item["sub_url"] = meta_1["sub_url"]
                item["sub_file_name"] = meta_1["sub_file_name"]
                item["son_url"] = son_urls[i]
                items.append(item)
        for item in items:
            yield scrapy.Request(url=item["son_url"], meta={"meta_2": item}, callback=self.detail_parse)

    # 获取文章和标题内容
    def detail_parse(self, response):
        item = response.meta['meta_2']
        content = ""
        head = response.xpath('//h1[@class="main-title"]/text()').extract()
        content_list = response.xpath('//div[@id="artibody"]/p/text()|//div[@id="article"]/p/text()').extract()
        # 将正文中的文本拼接起来
        print("--"*30)
        print(content_list)
        for content_item in content_list:
            content += content_item + "\n"

        # 去除那些没有标题的，整页都是图片的新闻
        item["head"] = head
        item["content"] = content

        yield item

