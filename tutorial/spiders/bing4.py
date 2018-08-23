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



class PhysSpider(scrapy.Spider):
    name = 'bing4'
    allowed_domains = ["http://cn.bing.com"]
    # start_urls = ('http://cn.bing.com/academic/profile?id=2097239364',)


    def start_requests(self):
        reqs = []
        with open("./BingShipAuthorUrl.txt","r") as f:
            for line in f.readlines():
                line = line.replace('\n','')
                url = line
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
        topics = []
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        name = soup.find('div',attrs={"class":"b_focusTextMedium"}).get_text()
        item['Name'] = name
        mechanism_temp = soup.find('li',attrs={"class":"aca_Affiliation"})
        if mechanism_temp is None:
            mechanism = ""
        else:
            mechanism = mechanism_temp.find('span',attrs={"class":"aca_abs_content"}).get_text()
        item['Mechanism'] = mechanism
        homePage_temp = soup.find('li',attrs={"class":"aca_Homepage"})
        if homePage_temp is None:
            homePage = ""
        else:
            homePage = homePage_temp.find('span',attrs={"class":"aca_abs_content"}).a.get('href')
        item['HomePage'] = homePage
        researchTopics_temp = soup.find('li',attrs={"class":"aca_ResearchInterests"})
        if researchTopics_temp is None:
            researchTopics = ""
        else:
            researchTopics = researchTopics_temp.find('span',attrs={"class":"aca_abs_content"}).get_text()
        item['ResearchTopics'] = researchTopics
        temp = soup.find('ol',attrs={"class":"aca_right"})
        paperNum_temp = temp.find('div',attrs={"class":"overview_column"})
        paperNum = paperNum_temp.get_text()
        item['PaperNum'] = paperNum
        citeNum_temp = paperNum_temp.next_sibling
        citeNum = citeNum_temp.get_text()
        item['CiteNum'] = citeNum

        url_temp = response.url+"&first=0&count=10&st=3"
        url = url_temp.replace("profile","papers")
        request = scrapy.Request(url=url, callback=self.parse_co, headers=headers, meta={'item': copy.deepcopy(item)}, dont_filter=True)
        yield request

    def parse_co(self,response):
        item = response.meta['item']
        coAuthors = []
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        temp = soup.find('tbody')
        temp_1 = temp.find_all('ul')
        for i in temp_1:
            first_tag = i.find('li')
            second_tag = first_tag.next_sibling
            coAuthor_temp = second_tag.get_text()
            coAuthors.append(coAuthor_temp)
        item['CoAuthors'] = coAuthors
        yield item







