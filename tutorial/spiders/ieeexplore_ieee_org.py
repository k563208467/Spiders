# -*- coding: utf-8 -*-
import scrapy
import re
import json
from tutorial.items import IeeeItem

class IeeexploreIeeeOrgSpider(scrapy.Spider):
    name = 'ieee'
    allowed_domains = ['ieeexplore.ieee.org']
    # start_urls = ('http://ieeexplore.ieee.org/document/7185405/',)

    def start_requests(self):
        reqs=[]
        for i in range(7180000,7185405):
            url = 'http://ieeexplore.ieee.org/document/%d/'%i
            req = scrapy.Request(url)
            reqs.append(req)
        return reqs

    def parse(self, response):
        s = str(re.findall(r'global.document.metadata=.*',response.body))
        temp = s.replace("['global.document.metadata=","")
        result = temp.replace(";']","")
        with open("../item.json","a") as f:
            a = json.dumps(result,sort_keys=True,indent=4)

            f.write(a+'\n')
        print "写文件完成"

        # pre_item['Title'] = response.xpath("//h1/span[@class='ng-bingding']/text()").extract()
        # # for i in range(1,10):
        # #     pre_item['Author'] = response.xpath("//*[@id='LayoutWrapper']/div[6]/div[3]/div/div/div/div[2]/div/div/span[%d]/span/a/span/text()"%i).extract()
        # #     pre_item['AuthorInfo'] = response.xpath("//*[@id='LayoutWrapper']/div[6]/div[3]/div/div/div/div[2]/div/div/span[%d]/span/a/@qtip-text"%i).extract()
        # #     pre_item['Keywords'] = response.xpath("//*[@id='full-text-section']/div/div[2]/section/div[1]/section/div/ul/li[1]/div/span[%d]/a/text()"%i).extract()
        # pre_item['Author'] = response.xpath("//*[@id='LayoutWrapper']/div[6]/div[3]/div/div/div/div[2]/div/div/span[1]/span/a/span/text()").extract()
        # pre_item['AuthorInfo'] = response.xpath("//*[@id='LayoutWrapper']/div[6]/div[3]/div/div/div/div[2]/div/div/span[1]/span/a/@qtip-text").extract()
        # pre_item['Keywords'] = response.xpath("//*[@id='full-text-section']/div/div[2]/section/div[1]/section/div/ul/li[1]/div/span[1]/a/text()").extract()
        # pre_item['Abstract'] = response.xpath("/body/div[3]/div[6]/div[3]/div/section[3]/div/div[1]/div/div/div/text()").extract()
        # pre_item['PublisherOrConference'] = response.xpath("/body/div[3]/div[6]/div[3]/div/section[3]/div/div[1]/section/div[2]/a/text()").extract()
        # pre_item['Volume'] = response.xpath("//div[@class='u-pb-1 stats-document-abstract-publishedIn ng-scope']/span/span[1]/text()").extract()
        # pre_item['Issue'] = response.xpath("//*[@id='7185405']/div[2]/span/span[2]/a/text()").extract()
        # pre_item['Pages'] = response.xpath("//*[@id='7185405']/div[3]/div[1]/div[1]/text()[2]").extract()+response.xpath("//*[@id='7185405']/div[3]/div[1]/div[1]/span/text()").extract()
        # pre_item['Time'] = response.xpath("//*[@id='7185405']/div[3]/div[1]/div[2]/text()[3]").extract()
        # pre_item['Category'] = "IEEE"
        # return pre_item
