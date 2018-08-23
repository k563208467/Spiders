# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import time
import re
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request
from tutorial.items import PaperItem
from pymongo import MongoClient



class PnasSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ["https://www.nature.com"]
    start_urls = ('https://scholar.google.com/citations?user=MXgWgmEAAAAJ&hl=en&oi=ASCII',
                  )
    client = MongoClient('localhost',27017)
    db = client.runoob
    collection = db.scholarReal

    def start_requests(self):
        reqs = []
        for context in self.collection.find({"orderNum":{ '$gt':0,'$lt':10000}}):
            # doi_temp = context['doi'].replace('doi:','')
            id_temp = context['ID']
            url = context['authorurl']
            req = scrapy.Request(url,meta={'context':context})
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
        item = PaperItem()
        context = response.meta['context']
        y = []
        n = []
        p = []
        result = []
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        name = soup.find('div',attrs={"class":"gsc_md_hist_w"})
        if name is None:
            result = " "
        else:
            years = name.find_all('span',attrs={"class":"gsc_g_t"})
            if years is None:
                result = " "
            else:
                numbers = name.find_all('a',attrs={"class":"gsc_g_a"})
                if numbers is None:
                    result = " "
                else:
                    for number in numbers:
                        data = number.string
                        n.append(data)
                    for year in years:
                        time = year.string
                        y.append(time)
                    for i in range(len(n)):
                        res = str(y[i]) + " " + str(n[i])
                        result.append(res)
        self.collection.update({"ID":context['ID']},{'$set':{"refhistory":result}})
        ds = soup.find_all('td',attrs={"class":"gsc_rsb_std"})
        if ds is None:
            p = " "
        else:
            for d in ds:
                pro = d.string
                p.append(pro)
        self.collection.update({"ID":context['ID']},{'$set':{"propertys":p}})






