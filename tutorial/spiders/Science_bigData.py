# -*- coding: utf-8 -*-
import scrapy
class ExampleSpider(scrapy.Spider):
    name = 'bigdata'
    allowed_domains = ["science.sciencemag.org"]
    start_urls = ('http://science.sciencemag.org/content/343/6176/1203',)


    # def start_requests(self):
    #     reqs = []
    #     for i in range(1,10):
    #         url = 'http://science.sciencemag.org/content/343/6176/%d'%i
    #         req = scrapy.Request(url)
    #         reqs.append(req)
    #
    #     return reqs


    def parse(self, response):
        pass
