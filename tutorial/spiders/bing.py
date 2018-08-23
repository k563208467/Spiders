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
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class PhysSpider(scrapy.Spider):
    name = 'bing'
    allowed_domains = ["http://cn.bing.com"]
    # start_urls = ('http://cn.bing.com/academic/search?q=aerospace&first=0&FORM=PONR',)


    def start_requests(self):
        reqs = []
        for i in range(0,10):
            m = i*10
            url = 'https://www.bing.com/academic/search?q=Reversing+Paralysis&first=%d&FORM=PENR6'%m
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
        item = BingItem()
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        list_temp = soup.find('ol',attrs={"id":"b_results"})
        lists = list_temp.find_all('li',attrs={"class":"aca_algo"})
        for list in lists:
            temp_url = list.h2.a.get('href')
            fullUrl = 'http://cn.bing.com'+temp_url
            item['fullUrl'] = fullUrl
            request = scrapy.Request(url=fullUrl, callback=self.parse_fullInfo, headers=headers, meta={'item': copy.deepcopy(item)}, dont_filter=True)
            yield request

    def parse_fullInfo(self,response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Cookie":"	ipv6=hit=1; SNRHOP=I=&TS=; _EDGE_S=mkt=zh-cn&ui=zh-cn&F=1&SID=20270FEEF40066C53C190503F5A16792; _EDGE_V=1; MUID=26C0B9CFE30C60C73C31B322E2AD61EE; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=EE8CD838728A4B3A90A6C041BC2BFB2D&dmnchg=1; SRCHUSR=DOB=20170829; _SS=SID=20270FEEF40066C53C190503F5A16792&HV=1504091535; MUIDB=26C0B9CFE30C60C73C31B322E2AD61EE; SRCHHPGUSR=WTS=63639688275&NEWWND=1&NRSLT=-1&SRCHLANG=&AS=1&NNT=1&HIS=1&HAP=0; AcaBatchCitePop=CLOSE=1; _EDGE_CD=u=zh-cn"
        }
        item = response.meta['item']
        author = []
        keywords = []
        soup = BeautifulSoup(response.body_as_unicode(),"html.parser")
        result = soup.find('ol',attrs={"class":"aca_base"})
        '''标题'''
        item['Title'] = result.find('li',attrs={"class":"aca_title"}).get_text()
        '''作者信息'''
        author_temp = soup.find('span',text="作　　者")
        author_par = author_temp.find_parent("div")
        author_con = author_par.find('div',attrs={"class":"aca_desc b_snippet"})
        authorlists = author_con.find_all('a')
        for authorlist in authorlists:
            name = authorlist.string
            author.append(name)
        item['Author'] = author
        '''摘要信息'''
        abstract_temp = soup.find('span',text="摘　　要")
        if abstract_temp is None:
            abstract = ""
        else:
            abstract_par = abstract_temp.find_parent("div")
            abstract_con = abstract_par.find('div',attrs={"class":"aca_desc b_snippet"})
            abstract = abstract_con.get_text()
        item['Abstract'] = abstract
        '''关键词信息（领域）'''
        keys_temp = result.find('li',attrs={"class":"aca_fos"})
        keys = keys_temp.find_all('span',attrs={"class":"aca_badge"})
        if keys_temp is None:
            keywords = ""
        else:
            for key in keys:
                keyword = key.string
                keywords.append(keyword)
        item['Keywords'] = keywords
        '''发表时间'''
        date = self.getInfo("发表日期",soup)
        item['Date'] = date
        '''期刊（会议）信息'''
        pub = self.getInfo("期　　刊",soup)
        item['Publisher'] = pub
        '''卷号'''
        vol = self.getInfo("卷　　号",soup)
        item['Volume'] = vol
        '''期号'''
        issue = self.getInfo("期　　号",soup)
        item['Issue'] = issue
        '''页码范围'''
        pages = self.getInfo("页码范围",soup)
        item['Pages'] = pages
        '''被引量'''
        citeNum = self.getInfo("被 引 量",soup)
        item['citeNum'] = citeNum
        '''DOI'''
        doi = self.getInfo("DOI",soup)
        item['Doi'] = doi
        temp_url = response.url + "&first=0&count=50&rt=2"
        temp_url2 = response.url + "&first=0&count=50&rt=1"
        ref_url1 = temp_url.replace("profile","papers")
        ref_url2 = temp_url2.replace("profile","papers")
        request = scrapy.Request(url=ref_url1, callback=self.par_ref, headers=headers, meta={'item': copy.deepcopy(item)}, dont_filter=True)
        request2 = scrapy.Request(url=ref_url2, callback=self.par_url, headers=headers, meta={'item': copy.deepcopy(item)}, dont_filter=True)
        yield request
        yield request2



    def par_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        refUrlLists = []
        refUrlResults = soup.find_all('a')
        for refUrlResult in refUrlResults:
            refUrl = "http://cn.bing.com"+refUrlResult.get('href')
            refUrlLists.append(refUrl)
            with open("./citeUrl.txt","a") as f:
                f.write(refUrl+'\n')


    def par_ref(self,response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        }
        item = response.meta['item']
        authors = item['Author']
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        results = soup.find_all('tr')
        ref = []
        refUrlLists = []
        refUrlResults = soup.find_all('a')
        for refUrlResult in refUrlResults:
            refUrl = "http://cn.bing.com"+refUrlResult.get('href')
            refUrlLists.append(refUrl)
            with open("./refUrl.txt","a") as f:
                f.write(refUrl+'\n')

        for result in results:
            temp = []
            lists = result.find_all('td')
            for list in lists:
                t = list.get_text()
                temp.append(t)
            ref.append(temp)
        item['Reference'] = ref
        urllist = []
        authorInfo = []
        x = len(authors)
        for author in authors:
            url = "http://cn.bing.com/academic/search?q="+author+"&mkt=zh-cn"
            urllist.append(url)
            request = scrapy.Request(url=url, callback=self.parse_info, headers=headers, meta={'item': item,'author':author,'x':x,'info':authorInfo}, dont_filter=True)
            yield request

    def parse_info(self,response):
        item = response.meta['item']
        author = response.meta['author']
        authorInfo = response.meta['info']
        x = response.meta['x']
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        temp = soup.find('div',attrs={"id":"b_content"})
        info_temp = temp.find('ol',attrs={"id":"b_context"})
        auth = info_temp.find('div',attrs={"class":"aca_card_fact"})
        if auth is None:
            authInfo = ""
        else:
            authInfo = author + auth.get_text()
        authorInfo.append(authInfo)
        # if len(self.authorInfo) != x:
        #     print "contitue crawling"
        # else:
        item['AuthorInfo'] = authorInfo
        yield item

    def getInfo(self, str ,soup):
        temp = soup.find('span',text=str)
        if temp is None:
            result = ""
        else:
            parent = temp.find_parent("div")
            content = parent.find('span',attrs={"class":"aca_content"})
            result = content.string
        return result


