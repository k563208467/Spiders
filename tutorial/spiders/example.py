# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ["xicidaili.com"]
    start_urls = ('http://wwww.xicidaili.com/',)


    def start_requests(self):
        reqs = []
        for i in range(1,10):
            url = 'http://www.xicidaili.com/nn/%d'%i
            req = scrapy.Request(url)
            reqs.append(req)

        return reqs


    def parse(self, response):
        ip_list = response.xpath('//table[@id="ip_list"]')
        trs = ip_list[0].xpath('tr')
        items = []
        for ip in trs[1:]:
            pre_item = TutorialItem()
            pre_item['IP'] = ip.xpath('td[2]/text()').extract()
            pre_item['Port'] = ip.xpath('td[3]/text()').extract()
            pre_item['Position'] = ip.xpath('string(td[4])')[0].extract().strip()
            pre_item['Type'] = ip.xpath('td[6]/text()').extract()
            pre_item['Speed'] = ip.xpath('td[7]/div/@title').re('\d+\.\d*')
            pre_item['LAST_CHECK_TIME'] = ip.xpath('td[10]/text()').extract()

            items.append(pre_item)

        return items








