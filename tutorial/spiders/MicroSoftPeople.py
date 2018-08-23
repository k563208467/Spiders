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
from scrapy import log
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class PhysSpider(scrapy.Spider):
    name = 'MicroSoftPeople'
    # allowed_domains = ["https://academic.microsoft.com"]
    start_urls = ('https://www.baidu.com/',)
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
    dcap["phantomjs.page.settings.cookie"] = ("msacademic=d05c2157-9e54-48ff-ab2b-43864b29430b; ai_user=Ll7Cm|2017-08-29T08:29:14.651Z; ARRAffinity=03dbaf7ebccf3a5270373d2bf50d0eea48778d1e5597aa06ff24fffe7ddcb12c; ai_session=ATGmx|1507543708952.43|1507548269298.4")
    dcap["phantomjs.page.settings.loadImages"] = False
    browser = webdriver.PhantomJS(desired_capabilities=dcap)
    browser.implicitly_wait(8)

    def parse(self, response):
        # try:
            with open("./MsAeroUrl.txt","r") as f:
                for line in f.readlines():
                    try:
                        line = line.replace('\n','')
                        url = line
                        request = Request(url)
                        request.meta['PhantomJS'] = True
                        self.browser.get(request.url)
                        print "beginning to get"
                        time.sleep(8)
                        shows = self.browser.find_elements_by_link_text("Show More")
                        for show in shows:
                            show.click()
                        time.sleep(3)

                        item = PersonItem()
                        soup = BeautifulSoup(self.browser.page_source,"lxml")
                        '''姓名信息'''
                        name_temp = soup.find('h1',attrs={"class":"grey-title ma-sem-author"})
                        if name_temp is None:
                            name = ""
                        else:
                            name = name_temp.get_text()
                        item['Name'] = name

                        '''所在机构信息'''
                        mechanism_temp = soup.find('div',attrs={"class":"grey-title subheader"})
                        if mechanism_temp is None:
                            mechanism = ""
                        else:
                            mechanism = mechanism_temp.get_text(strip=True)
                        item['Mechanism'] = mechanism
                        '''论文发表总数'''
                        paperNum_temp = soup.find('div',attrs={"class":"pure-u-md-3-24 pure-u-5-24 digit"})
                        if paperNum_temp is None:
                            paperNum = ""
                        else:
                            paperNum = paperNum_temp.h1.get_text()
                        item['PaperNum'] = paperNum
                        '''论文被引总数'''
                        citeNum_temp = soup.find('div',attrs={"class":"pure-u-md-5-24 pure-u-7-24 digit"})
                        if citeNum_temp is None:
                            citeNum = ""
                        else:
                            citeNum = citeNum_temp.h1.get_text()
                        item['CiteNum'] = citeNum
                        '''合作学者信息'''
                        coAus = []
                        coAuthor_tag = soup.find(attrs={"class":"ulist-author"})
                        if coAuthor_tag is None:
                            coAus = ""
                        else:
                            coAuthor_temp = coAuthor_tag.find('ul',attrs={"class":"ulist-content"})
                            if coAuthor_temp is None:
                                coAus = ""
                            else:
                                coAuthors = coAuthor_temp.find_all('a')
                                for coAuthor in coAuthors:
                                    coAu = coAuthor.get_text()
                                    coAus.append(coAu)
                                    co_url = "https://academic.microsoft.com/"+coAuthor.get('href')
                                    with open("./MsAeroUrl2.txt","a") as f:
                                        f.write(co_url+'\n')
                        item['CoAuthors'] = coAus
                        '''研究领域信息'''
                        topics = []
                        topic_tag = soup.find(attrs={"class":"ulist-fieldOfStudy"})
                        if topic_tag is None:
                            topics = ""
                        else:
                            topic_temp = topic_tag.find('ul',attrs={"class":"ulist-content"})
                            if topic_temp is None:
                                topics = ""
                            else:
                                tops = topic_temp.find_all('a')
                                for top in tops:
                                    topic = top.get_text()
                                    topics.append(topic)
                        item['ResearchTopics'] = topics
                        yield item
                    except:
                        continue
        # except:
        #     self.browser.quit()
        #     print "Memory out"



