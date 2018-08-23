# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import time
import re
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request
from tutorial.items import NatureItem
from pymongo import MongoClient



class PnasSpider(scrapy.Spider):
    name = 'nature4'
    allowed_domains = ["https://www.nature.com"]
    start_urls = ('https://cn.bing.com/academic/search?q=10.1038/488592a',
                  )
    client = MongoClient('localhost',27017)
    db = client.runoob
    collection = db.pnas

    def start_requests(self):
        reqs = []
        for context in self.collection.find({},["title","doi"]):
            # doi_temp = context['doi'].replace('doi:','')
            doi_temp = context['doi']
            url = "https://cn.bing.com/academic/search?q="+doi_temp
            req = scrapy.Request(url,meta={'context':context})
            reqs.append(req)
        return reqs


    def parse(self,response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Cookie":"ARRAffinity=640e8c039577bfc2eba717140df600caa663ec7bae8bb5a6a5091f563581f452"
        }
        context = response.meta['context']
        for i in range(0,10):
            m = i*100
            temp_url = response.url + "&first=%d&count=100&rt=2"%m
            ref_url = temp_url.replace("profile","papers")
            request = scrapy.Request(url=ref_url, callback=self.par_cite, headers=headers, meta={'context': context}, dont_filter=True)
            yield request


    def par_cite(self,response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Cookie":"ARRAffinity=640e8c039577bfc2eba717140df600caa663ec7bae8bb5a6a5091f563581f452"
        }
        reqs = []
        context = response.meta['context']
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        results = soup.find_all('tr')
        # signal_temp = soup.find('div')
        # signal = signal_temp.get('data-stopload')
        for result in results:
            url_temp = result.td.ul.li.a.get('href')
            url = "https://cn.bing.com" + url_temp
            request = scrapy.Request(url=url, callback=self.par_list, headers=headers, meta={'context': context}, dont_filter=True)
            reqs.append(request)
        return reqs
        # if signal == "1":
        #         print "**************************************Over->Next****************************************"
        #         yield None

    def par_list(self,response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Cookie":"ARRAffinity=640e8c039577bfc2eba717140df600caa663ec7bae8bb5a6a5091f563581f452"
        }
        context = response.meta['context']
        soup = BeautifulSoup(response.body_as_unicode(),"html.parser")
        list_temp = soup.find('ol',attrs={"id":"b_results"})
        list = list_temp.find('li',attrs={"class":"aca_algo"})
        temp_url = list.h2.a.get('href')
        fullUrl = 'http://cn.bing.com'+temp_url
        request = scrapy.Request(url=fullUrl, callback=self.par_details, headers=headers, meta={'context': context}, dont_filter=True)
        yield request

    def par_details(self,response):
        context = response.meta['context']
        author = []
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        result = soup.find('ol',attrs={"class":"aca_base"})
        title = result.find('li',attrs={"class":"aca_title"}).get_text()

        author_temp = soup.find('span',text="作　　者")
        author_par = author_temp.find_parent("div")
        author_con = author_par.find('div',attrs={"class":"aca_desc b_snippet"})
        authorlists = author_con.find_all('a')
        for authorlist in authorlists:
            name = authorlist.string
            author.append(name)
        citeNum = self.getInfo("被 引 量",soup)
        date = self.getInfo("发表日期",soup)
        pub = self.getInfo("期　　刊",soup)
        doi = self.getInfo("DOI",soup)
        data = dict(title=title,time=date,publisher=pub,authors=author,doi=doi,citeNum=citeNum)
        content = self.collection.find_one({"doi":context['doi']},["Cite","Title"])
        if ('Cite' in content.keys()):
            a = content['Cite']
            a.append(data)
        else:
            a = []
            a.append(data)
        self.collection.update({"doi":context['doi']},{'$set':{"Cite":a}})


    def getInfo(self, str ,soup):
        temp = soup.find('span',text=str)
        if temp is None:
            result = ""
        else:
            parent = temp.find_parent("div")
            content = parent.find('span',attrs={"class":"aca_content"})
            result = content.string
        return result
