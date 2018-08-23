# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import time
import copy
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request
from tutorial.items import BingItem
from selenium.webdriver.common.keys import Keys
from scrapy import log
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class PhysSpider(scrapy.Spider):
    name = 'MicroSoft'
    # allowed_domains = ["https://academic.microsoft.com"]
    start_urls = ('https://www.baidu.com/',)



    # def start_requests(self):
    #     reqs = []
    #     for i in range(0,1):
    #         m = i*8
    #         url = 'https://academic.microsoft.com/#/search?iq=aerospace&q=aerospace&filters=&from=%d&sort=0'%m
    #         req = scrapy.Request(url)
    #         req.meta['dont_redirect'] = True
    #         reqs.append(req)
    #
    #     return reqs

    def parse(self, response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        }
        try:
            for i in range(164,2450):
                m = i*8
                url = "https://academic.microsoft.com/#/search?iq=@Aerospace@&q=Aerospace&filters=Y>1980&from=%d&sort=0"%m
                self.browser.get(url)
                print "beginning to get"
                time.sleep(8)
                soup = BeautifulSoup(self.browser.page_source,"lxml")
                temps = soup.find_all('span',attrs={"class":"paper-author-affiliation"})
                for temp in temps:
                    person_temp_url = temp.a.get('href')
                    person_url = "https://academic.microsoft.com/"+person_temp_url
                    with open("./MsAeroUrl.txt","a") as f:
                        f.write(person_url+'\n')
        except:
            self.browser.quit()
            return False

