# -*- coding: utf-8 -*-
import scrapy
import json
import requests
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request
from tutorial.items import PnasItem


class PnasSpider(scrapy.Spider):
    name = 'pnas'
    allowed_domains = ["http://www.pnas.org"]
    start_urls = ('http://www.pnas.org/content/by/section/Biochemistry?FIRSTINDEX=0',)


    def start_requests(self):
        reqs = []
        for i in range(0,6873):
            m = i*10
            url = 'http://www.pnas.org/search?tmonth=&pubdate_year=&submit=yes&submit=yes&submit=Submit&andorexacttitle=and&format=standard&firstpage=&fmonth=&title=&hits=10&tyear=2018&titleabstract=&volume=&sortspec=relevance&andorexacttitleabs=and&tocsectionid=all&author2=&andorexactfulltext=and&fyear=2000&author1=&doi=&fulltext=&FIRSTINDEX=%d'%m
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
            "X-Requested-With":"XMLHttpRequest"
        }
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        resultList = soup.find_all(attrs={"class":"cit-views"})
        for result in resultList:
            abstractUrlList = result.find(attrs={"class":"first-item"})
            for abstractTag in abstractUrlList:
                abstractHref = abstractTag.get('href')
                abstractUrl='http://www.pnas.org'+abstractHref
                try:
                    temp = abstractUrl.replace("abstract","full")
                    fullInfoUrl = temp.replace("extract","full")
                    request = scrapy.Request(url=abstractUrl, callback=self.parse_abstract, headers=headers, dont_filter=True)
                    request.meta['fullUrl'] = fullInfoUrl
                    request.meta['abstractUrl'] = abstractUrl
                    yield request
                except:
                    print "Nothing in the Page"


    def parse_abstract(self, response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }
        fullInfoUrl = response.meta['fullUrl']
        AbstractUrl = response.meta['abstractUrl']
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        item = PnasItem()
        article_tag = soup.find('h1', id="article-title-1")
        if article_tag is None:
            item['Title'] = ""
        else:
            item['Title'] = article_tag.get_text()

        # temp = soup.find('div', attrs={"class":"section abstract"}).get_text()
        # if temp is None:
        #     item['Abstract'] = soup.find('p',attrs={"class":"flushleft"}).get_text()
        # else:
        #     item['Abstract'] = temp
        abs_tag = soup.find('div', attrs={"class": "section abstract"})
        if abs_tag is None:
            item['Abstract']= ""
        else:
            item['Abstract']= abs_tag.get_text(strip=True)


        item['fullUrl'] = fullInfoUrl
        item['abstractUrl'] = AbstractUrl
        request = scrapy.Request(url=fullInfoUrl, callback=self.parse_fullInfo, headers=headers, meta={'item': item}, dont_filter=True)
        yield request

        # item['Abstract'] = soup.find_all("div","p", class_=["section abstract", "flushleft"]).get_text(strip=True)



    def parse_fullInfo(self, response):
        item = response.meta['item']
        abstractUrl = item['abstractUrl']
        authorInfoUrl = abstractUrl + '?tab=author-info'
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "Referer":authorInfoUrl,
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")

        citList = soup.find_all('div',attrs={"class":"cit-metadata"})
        if citList is None:
            item['Reference'] = ""
        else:
            result = []
            for cit in citList:
                temp = cit.get_text(strip=True)
                temp_2 = "<"+temp.strip()+">"
                result.append(temp_2)
            item['Reference'] = result

        time_tag = soup.find('span', attrs={"class": "slug-pub-date"})
        if time_tag is None:
            item['Time'] = ""
        else:
            item['Time'] = time_tag.get_text(strip=True)

        volume_tag = soup.find('span', attrs={"class": "slug-vol"})
        if volume_tag is None:
            item['Volume'] = ""
        else:
            item['Volume'] = volume_tag.get_text(strip=True)

        issue_tag = soup.find('span', attrs={"class": "slug-issue"})
        if issue_tag is None:
            item['Issue'] = ""
        else:
            item['Issue'] = issue_tag.get_text(strip=True)

        page_tag = soup.find('span', attrs={"class": "slug-pages"})
        if page_tag is None:
            item['Pages'] = ""
        else:
            item['Pages'] = page_tag.get_text(strip=True)

        pub_tag = soup.find('abbr', attrs={"class": "slug-jnl-abbrev"})
        if pub_tag is None:
            item['PublisherOrConference'] = ""
        else:
            item['PublisherOrConference'] = pub_tag.get_text(strip=True)

        doi_tag = soup.find('span', attrs={"class": "slug-doi"})
        if doi_tag is None:
            item['doi'] = ""
        else:
            item['doi'] = doi_tag.get_text(strip=True)

        request = scrapy.Request(url=authorInfoUrl, callback=self.parse_authorInfo, headers=headers, meta={'item': item}, dont_filter=True)
        yield request



    def parse_authorInfo(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body_as_unicode(), "lxml")
        headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
        }
        authorResult = []
        detailResult = []
        authorInfo = soup.find("ol",attrs={"class", "contributor-list"})
        if authorInfo is None:
            item['Author'] = ""
            item['AuthorInfo'] = ""
        else:
            authorList = authorInfo.find_all("li", attrs={"class": "contributor"})
            lastInfo = authorInfo.find("li", attrs={"class": "last"})
            lastName = "<"+lastInfo.find("span", attrs={"class", "name"}).get_text()+">"

            for author in authorList:
                authorName = author.find("span", attrs={"class", "name"}).get_text()
                infoNum = author.find_all("a",attrs={"class":"xref-aff"})
                id = []
                for info in infoNum:
                    num = info.get_text()
                    id.append(num)
                temp = "<"+authorName+ str(id) +">"
                authorResult.append(temp)
            authorResult.append(lastName)
            item['Author'] = authorResult
            details = soup.find_all("li",attrs={"class": "aff"})
            for detail in details:
                detailInfo = "<"+detail.get_text(strip=True)+">"
                detailResult.append(detailInfo)
            item['AuthorInfo'] = detailResult
        cite_url = 'http://xueshu.baidu.com/s?wd=' + item['doi']
        request = scrapy.Request(url=cite_url, callback=self.parse_cite, headers=headers, meta={'item': item}, dont_filter=True)
        yield request



    def parse_cite(self,response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        cite_tag = soup.find('div',attrs={'class':'ref_wr'})
        if cite_tag is None:
            item['CiteNum'] = ""
        else:
            item['CiteNum'] = cite_tag.get_text(strip=True)
        yield item













