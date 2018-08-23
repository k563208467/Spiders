# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import time
import copy
import string
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request
from tutorial.items import PersonItem

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class BingSpider(scrapy.Spider):
    name = 'bing3'
    allowed_domains = ["http://cn.bing.com"]
    # start_urls = ('http://cn.bing.com/academic/search?q=aerospace&first=0&FORM=PONR',)

    def start_requests(self):
        reqs = []
        for i in range(0,1130):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=Oceanic+climate&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)
        for i in range(0,1000):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=Tide&filters=yearRange:1980-2017&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)
        for i in range(0,184):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=submarine&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)
        for i in range(0,718):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=hull&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)
        for i in range(0,1919):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=transportation&filters=yearRange:1970-2017&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)
        for i in range(0,768):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=Littoral+zone&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)
        for i in range(0,39):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=Seamanship&filters=yearRange:1970-2017&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)
        for i in range(0,173):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=maritime&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)
        for i in range(0,336):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=seabed&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)
        for i in range(0,10000):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=welding&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)
        for i in range(0,495):
            m = i*10
            url = 'https://cn.bing.com/academic/search?q=Intertidal+zone&first=%d&FORM=PENR6'%m
            req = scrapy.Request(url)
            reqs.append(req)


        return reqs


    def parse(self, response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Cookie":"ARRAffinity=640e8c039577bfc2eba717140df600caa663ec7bae8bb5a6a5091f563581f452"
        }
        item = PersonItem()
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        list_temp = soup.find('ol',attrs={"id":"b_results"})
        lists = list_temp.find_all('li',attrs={"class":"aca_algo"})
        for list in lists:
            if list is None:
                print "No Link"
            else:
                temp = list.find('div',attrs={"class":"caption_author"})
                authors = temp.find_all('a')
                for author in authors:
                    temp_url = author.get('href')
                    url = "http://cn.bing.com"+temp_url
                    with open("./BingShipAuthorUrl.txt","a") as f:
                        f.write(url+'\n')


