# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']

    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'
    # FromRequest是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url=url,
            formdata={"email": "357932982@qq.com", "password": "yms1989YMS1214"},
            callback=self.parse_page
        )

    def parse_page(self, response):
        with open("renren.html", 'wb') as f:
            f.write(response.body)
