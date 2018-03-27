# -*- coding: utf-8 -*-
import scrapy


class Renren2Spider(scrapy.Spider):
    name = 'renren2'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/PLogin.do']

    def parse(self, response):

        yield scrapy.FormRequest.from_response(
            response,
            formdata={"email": "357932982@qq.com", "password": "yms1989YMS1214"},
            callback=self.parse_page
        )

    def parse_page(self, response):
        url = "http://www.renren.com/414560930/profile"
        yield scrapy.Request(url, callback=self.parse_newpage)

    def parse_newpage(self, response):
        with open('renren.html', 'wb') as f:
            f.write(response.body)
