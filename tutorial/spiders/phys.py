# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import time
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request
from tutorial.items import PhysItem
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class PhysSpider(scrapy.Spider):
    name = 'phys'
    allowed_domains = ["https://http://www.sciencedirect.com"]
    start_urls = ('https://http://www.sciencedirect.com/science/journal/03701573/1?sdc=1',)


    def start_requests(self):
        reqs = []
        for i in range(690,700):
            m = i
            url = 'http://www.sciencedirect.com/science/journal/03701573/%d?sdc=1'%m
            req = scrapy.Request(url)
            reqs.append(req)

        return reqs

    def parse(self, response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Cookie":"	SD_ART_LINK_STATE=; expires=Thu, 01 Jan 1970 23:59:59 GMT; path=/; domain=.sciencedirect.com;MIAMISESSION=becb51d6-863d-11e7-8dab-00000aab0f6c:3680753329; path=/; domain=.sciencedirect.com; HttpOnlyTARGET_URL=fcf74dd786744d87fbaaaf8652a764ab4a79b0d3ed681139e910692376063105b57efc9f763ef87b0a40ff4500f368c3d23c4eaf68d359ec642650aed5fe5bb6; path=/; domain=.sciencedirect.com; HttpOnlyDEFAULT_SESSION_SUBJECT=; path=/; domain=.sciencedirect.com; HttpOnlybm_sv=4F8D18584A14F230238A6E28BE47070C~6MQMFZPKMU4yA5ZRg74G3hh1JWVRJPOko/pOYXEreTnccWcOu7ZqliVRYGAo6pfAn6We6kP7VTgIDwIcGy5JSWQujovy9FXCsPqI5+4P9ABiS+UtbJhIwDrDLK6tEb1Y6ch0D2xIzRdU6afcKPLw5QlixPLp3Qk/2tyu+NQrtfA=; Domain=.sciencedirect.com; Path=/; Max-Age=5207; HttpOnly"
        }
        item = PhysItem()
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        url_temp1 = soup.find('ol',attrs={"class":"articleList results"})
        url_temp2 = url_temp1.find('li',attrs={"class":"title"})
        url = url_temp2.a.get('href')
        item['fullUrl'] = url
        request = scrapy.Request(url=url, callback=self.parse_fullInfo, headers=headers, meta={'item': item}, dont_filter=True)
        yield request

    def parse_fullInfo(self,response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest",
        }
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
        dcap["phantomjs.page.settings.cookie"] = ("SD_ART_LINK_STATE=; expires=Thu, 01 Jan 1970 23:59:59 GMT; path=/; domain=.sciencedirect.com;MIAMISESSION=becb51d6-863d-11e7-8dab-00000aab0f6c:3680753329; path=/; domain=.sciencedirect.com; HttpOnlyTARGET_URL=fcf74dd786744d87fbaaaf8652a764ab4a79b0d3ed681139e910692376063105b57efc9f763ef87b0a40ff4500f368c3d23c4eaf68d359ec642650aed5fe5bb6; path=/; domain=.sciencedirect.com; HttpOnlyDEFAULT_SESSION_SUBJECT=; path=/; domain=.sciencedirect.com; HttpOnlybm_sv=4F8D18584A14F230238A6E28BE47070C~6MQMFZPKMU4yA5ZRg74G3hh1JWVRJPOko/pOYXEreTnccWcOu7ZqliVRYGAo6pfAn6We6kP7VTgIDwIcGy5JSWQujovy9FXCsPqI5+4P9ABiS+UtbJhIwDrDLK6tEb1Y6ch0D2xIzRdU6afcKPLw5QlixPLp3Qk/2tyu+NQrtfA=; Domain=.sciencedirect.com; Path=/; Max-Age=5207; HttpOnly")
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
        browser.get(response.url)
        print 'beginning to get'
        time.sleep(10)
        browser.find_element_by_link_text('Show more').click()
        soup = BeautifulSoup(browser.page_source,"lxml")
        browser.quit()
        item = response.meta['item']
        references = []
        keywords = []
        authors = []
        authorInfo = []
        pub_temp = soup.find('div',attrs={"class":"Publication"})
        item['PublisherOrConference'] = pub_temp.find('span',attrs={"class":"size-xl"}).get_text()
        ref_temp = soup.find('div',attrs={"class":"References"})
        ref_results = ref_temp.find_all('dd',attrs={"class":"reference"})
        for ref_result in ref_results:
            ref = '<'+ref_result.get_text(strip=True)+'>'
            references.append(ref)
        item['Reference'] = references
        key_temp = soup.find('div',attrs={"class":"Keywords"})
        key_results = key_temp.find_all('div',attrs={"class":"keyword"})
        for key_result in key_results:
            key = key_result.get_text(strip=True)
            keywords.append(key)
        title_temp = soup.find('h1',attrs={"class":"article-title"}).get_text()
        item['Title'] = title_temp
        item['Abstract'] = soup.find('div',attrs={"class":"abstract author"}).get_text()
        auth_temp = soup.find('div',attrs={"class":"author-group"})
        auth_results = auth_temp.find_all('a',attrs={"class":"author size-m workspace-trigger"})
        for auth_result in auth_results:
            author = auth_result.find('span',attrs={"class":"text given-name"}).get_text() + auth_result.find('span',attrs={"class":"text surname"}).get_text()
            authors.append(author)
        item['Author'] = authors
        info_temp = soup.find('div',attrs={"class":"publication-volume"})
        item['ArticleInfo'] = info_temp.find('span',attrs={"class":"size-m"}).get_text(strip=True)
        authorInfo_results = auth_temp.find_all('dl',attrs={"class":"affiliation"})
        for authorInfo_result in authorInfo_results:
            info = authorInfo_result.get_text()
            authorInfo.append(info)
        item['AuthorInfo'] = authorInfo

        cite_url = 'http://xueshu.baidu.com/s?wd=' + title_temp
        request = scrapy.Request(url=cite_url, callback=self.parse_cite, headers=headers, meta={'item': item}, dont_filter=True)
        yield request


    def parse_cite(self,response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        try:
            cite = soup.find('div',attrs={'class':'ref_wr'}).get_text(strip=True)
            item['Cite'] = cite
            yield item
        except:
            print "Can't get CiteNum"
