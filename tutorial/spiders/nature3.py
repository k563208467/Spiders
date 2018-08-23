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
from scrapy.selector import Selector
from pymongo import MongoClient



class PnasSpider(scrapy.Spider):
    name = 'nature3'
    allowed_domains = ["https://www.nature.com"]
    start_urls = ('https://cn.bing.com/academic/search?q=10.1038/488592a',
                  )
    client = MongoClient('localhost',27017)
    db = client.runoob
    collection = db.nature_groups_index_10

    def start_requests(self):
        reqs = []
        for context in self.collection.find({},["title","doi"]):
            doi_temp = context['doi'].replace('doi:','')
            url = 'https://api.altmetric.com/v1/doi/'+doi_temp+'?callback=_altmetric'
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
        if response.status == 404:#处理api不存在的情况
            print "No Data"
        else:
            a = response.body
            Murl =  a.split('details_url":"')
            if Murl:
                Murl = Murl[-1][0:-3]

                request = scrapy.Request(url=Murl, callback=self.par_cite, headers=headers, meta={'context':context}, dont_filter=True)
                yield request
            else:
                print "Url Error"


    def par_cite(self,response):
        context = response.meta['context']
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Cookie":"ARRAffinity=640e8c039577bfc2eba717140df600caa663ec7bae8bb5a6a5091f563581f452"
        }
        TAPS = {                  #一个映射,‘0’是没有解析的。
        'blogs':'blogs',
        'wikipedia':'wikipedia',
        'twitter':'twitter',
        'facebook':'facebook',
        'google':'google',
        'news':'news',
        }
        reqs = []
        sel = Selector(response)
        Mentioned = sel.xpath('//*[@class="mention-counts"]//text()').extract()
        li= set(Mentioned[0::4])
        for i in li:
            if i == "googleplus":
                i = "google"
            request = scrapy.Request(
                url=response.url + '/'+ i,
                callback=self.parse_detail,
                headers=headers,
                meta={'context':context,'i':i},
                dont_filter=True
                )
            reqs.append(request)

        return reqs

    def parse_detail(self,response):
        context = response.meta['context']
        social = response.meta['i']
        sel = Selector(response)

        if social == 'blogs':
            full = get_blogs(sel,response)
            self.collection.update({"doi":context['doi']},{'$set':{"blogs":full}})


        if social == 'twitter':
            full = get_twitters(sel,response)
            self.collection.update({"doi":context['doi']},{'$set':{"twitter":full}})


        if social == 'facebook':
            full = get_facebook(sel,response)
            self.collection.update({"doi":context['doi']},{'$set':{"facebook":full}})


        if social == 'wikipedia':
            full = get_wikipedia(sel,response)
            self.collection.update({"doi":context['doi']},{'$set':{"wikipedia":full}})


        if social == 'news':
            full = get_news(sel,response)
            self.collection.update({"doi":context['doi']},{'$set':{"news":full}})

        if social == 'google':
            full = get_google(sel,response)
            self.collection.update({"doi":context['doi']},{'$set':{"google":full}})





def get_blogs(sel,response):
    full = dict()
    summary = sel.xpath('//*[@class="section-summary"]/*[@class="text"]//text()').extract()
    full["summary"] = summary
    blogs = []
    data = response.body
    soup = BeautifulSoup(data,"lxml")
    bls = soup.find_all('article',"post blogs")
    for tw in bls:
        t = dict()
        title = tw.find('div',"content").h3.get_text()
        publish = tw.find('div',"content").h4.get_text()
        content = tw.find('p',"summary").get_text()
        time = tw.find('time').get_text()
        t["title"]=title
        t["publish"]=publish
        t["content"] = content
        t["time"] = time
        blogs.append(t)
        full['blogs'] = blogs
    return full

def get_twitters(sel,response):
    summary = sel.xpath('//*[@class="section-summary"]/*[@class="text"]//text()').extract()
    full = dict()
    full["summary"] = summary
    twitter = []
    data = response.body
    soup = BeautifulSoup(data,"lxml")
    tws = soup.find_all('article',"post twitter")
    for tw in tws:
        t = dict()
        name = tw.find('div',"name").get_text()
        handle = tw.find('div',"handle").get_text()
        follower = tw.find('div',"follower_count").span.get_text()
        content = tw.find('div',"content").p.get_text()
        time = tw.find('time').get_text()
        t["name"]=name
        t["handle"]=handle
        t["followernum"] = follower
        t["content"] = content
        t["time"] = time
        twitter.append(t)
    full['twitter'] = twitter
    return full

def get_facebook(sel,response):
    summary = sel.xpath('//*[@class="section-summary"]/*[@class="text"]//text()').extract()
    full = dict()
    full["summary"] = summary
    facebook = []
    data = response.body
    soup = BeautifulSoup(data,"lxml")
    tws = soup.find_all('article',"post facebook")
    for tw in tws:
        t = dict()
        name = tw.find('div',"content with_image").h4.get_text()
        content = tw.find('p',"summary").get_text()
        time = tw.find('time').get_text()
        t["name"]=name
        t["content"] = content
        t["time"] = time
        facebook.append(t)
    full['facebook'] = facebook
    return full

def get_wikipedia(sel,response):
    summary = sel.xpath('//*[@class="section-summary"]/*[@class="text"]//text()').extract()
    full = dict()
    full["summary"] = summary
    wikipedia = []
    data = response.body
    soup = BeautifulSoup(data,"lxml")
    tws = soup.find_all('article',"post wikipedia")
    for tw in tws:
        t = dict()
        citiao = tw.find('div',"content with_image").a.h3.get_text()
        by_name = tw.find('div',"content with_image").h4.a.get_text()
        by_name_url = tw.find('div',"content with_image").h4.a['href']
        content = tw.find('p',"summary").get_text()
        time = tw.find('time').get_text()
        t['by_name'] = by_name
        t['by_name'] = by_name_url
        t["citiao"]=citiao
        t["content"] = content
        t["time"] = time
        wikipedia.append(t)
    full['wikipedia'] = wikipedia
    return full

def get_news(sel,response):
    summary = sel.xpath('//*[@class="section-summary"]/*[@class="text"]//text()').extract()
    full = dict()
    full["summary"] = summary
    news = []
    data = response.body
    soup = BeautifulSoup(data,"lxml")
    tws = soup.find_all('article',"post msm")
    for tw in tws:
        t = dict()
        title = tw.find('div',"content with_image").h3.get_text()
        by_name = tw.find('div',"content with_image").h4.get_text()
        content = tw.find('p',"summary").get_text()
        time = tw.find('time').get_text()
        t['by_name'] = by_name
        t["title"]=title
        t["content"] = content
        t["time"] = time
        news.append(t)
    full['news'] = news
    return full


def get_google(sel,response):
    summary = sel.xpath('//*[@class="section-summary"]/*[@class="text"]//text()').extract()
    full = dict()
    full["summary"] = summary
    googleplus = []
    data = response.body
    soup = BeautifulSoup(data,"lxml")
    tws = soup.find_all('article',"post gplus")
    for tw in tws:
        t = dict()
        by_name = tw.find('div',"content with_image").h4.a
        if by_name:
            by_name = by_name.get_text()
        else:
            by_name = None
        content = tw.find('p',"summary").get_text()
        time = tw.find('time').get_text()
        t['by_name'] = by_name
        t["content"] = content
        t["time"] = time
        googleplus.append(t)
    full['googleplus'] = googleplus
    return full

