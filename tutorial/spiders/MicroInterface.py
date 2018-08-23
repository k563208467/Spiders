# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import time
import copy
import re
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request
from tutorial.items import PersonItem
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class PhysSpider(scrapy.Spider):
    name = 'MicroInterface'
    # allowed_domains = ["https://academic.microsoft.com"]
    start_urls = ('https://www.baidu.com/',)


    def parse(self, response):
        # try:
            headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        }
            with open("./MsAeroUrl.txt","r") as f:
                for line in f.readlines():
                    # try:
                        dcap = dict(DesiredCapabilities.PHANTOMJS)
                        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
                        dcap["phantomjs.page.settings.cookie"] = ("msacademic=d05c2157-9e54-48ff-ab2b-43864b29430b; ai_user=Ll7Cm|2017-08-29T08:29:14.651Z; ARRAffinity=03dbaf7ebccf3a5270373d2bf50d0eea48778d1e5597aa06ff24fffe7ddcb12c; ai_session=ATGmx|1507543708952.43|1507548269298.4")
                        dcap["phantomjs.page.settings.loadImages"] = False
                        browser = webdriver.PhantomJS(desired_capabilities=dcap)
                        # browser.set_page_load_timeout(10)
                        browser.implicitly_wait(10)
                        line = line.replace('\n','')
                        url = line
                        request = Request(url)
                        browser.get(request.url)
                        ssid = browser.session_id
                        a = re.findall(r"detail/(\d+)?",url)
                        b = re.findall(r"=(\d+)?",url)
                        c = a[0]
                        d = b[0]
                        interface = "https://academic.microsoft.com/api/browse/GetEntityDetails?entityId="+c+"&inRelationToEntityId="+d+"&correlationId="+ssid
                        req = scrapy.Request(url=interface, callback=self.parse_data, headers=headers, dont_filter=True)
                        yield req

    def parse_data(self,response):
        print response.body
