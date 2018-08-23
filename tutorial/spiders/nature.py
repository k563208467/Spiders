# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import time
from bs4 import BeautifulSoup
from scrapy import FormRequest
from scrapy import Request
from tutorial.items import NatureItem
from selenium import webdriver
from scrapy import log
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class PnasSpider(scrapy.Spider):
    name = 'nature'
    allowed_domains = ["https://www.nature.com"]
    start_urls = ('https://www.nature.com/search?article_type=research&journal=nature&order=relevance&page=1',
                  )


    # def start_requests(self):
    #     reqs = []
    #
    #     for i in range(1,2):
    #         url = "https://www.nature.com/search?article_type=research&journal=nature&order=relevance&page=%d"%i
    #         req = scrapy.Request(url,dont_filter=True)
    #         reqs.append(req)
    #     return reqs


    def parse(self, response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest",
            # "Cookie":"user.uuid=5a01aae3-e377-4e07-a07b-1b31f4dcffa7; __gads=ID=cb96fea7a634dd1b:T=1500515613:S=ALNI_Mb6mXrSZbm5xG_m1qJMqdWVG_YLPw; _polar_tu=*_%22mgtn%22_@2Q_u_@_daa4bf27-fa6f-4be5-9f3b-176a11ceb142_Q_n_@3Q_s_@1Q_sc_@*_v_@2Q_a_@2+Q_ss_@_%22otd9t5_Q_sl_@_%22otd9t5_Q_sd_@*+Q_v_@_2%5B288ebcc_Q_vc_@*_e_@1+Q_vs_@_%22otd9t5_Q_vl_@_%22otd9t5_Q_vd_@*+Q_vu_@_b90a8da825664a9c7f9d4ca17048600e_Q_vf_@_%22j5bsocdp_+; ebBurstingTime_.www.nature.com=1500517176113; ebNewHistory_.www.nature.com=21656454%3A1500517176113%3A11%3A1500515627073%3A11; idp_session=sVERSION_1295e5fdd-fba0-4a37-b57b-7dd2ff2ab6ed; idp_session_http=hVERSION_15cbc5053-2dd2-4780-aded-4a1ef383119e; idp_marker=a5bd50f5-3cb2-4da5-b2b0-aeaef8346cbc; SaneID=10.1.1.224.1502697284816074; referral_cookie=82; euCookieNotice=accepted; JSESSIONID=n4rkcyns6gv11akz8yb26achu; requestURL=http://www.nature.com/nams/svc/athenslogin; WT_FPC=id=5da88257-3cd3-49f1-b265-189ed5fcfc00:lv=1502748727673:ss=1502746783342; NatureRegistrationLogin=563208467@gx.sva&|60aVXbcA7/ic6&|0; __ar_v4=; _ga=GA1.2.1421928346.1500515609; _gid=GA1.2.1425480635.1502697288; ki_t=1500515613373%3B1502763916618%3B1502795627887%3B5%3B232; ki_r=; __VCAP_ID__=262a6c4e-8bf7-4f29-632e-6404d122c17f"
            "Cookie":"	WT_FPC=id=313257c9-deb7-459c-98a3-c839a98ede65:lv=1502820088432:ss=1502816699698; _ga=GA1.2.1772081262.1500348035; ki_t=1500348101531%3B1502863504189%3B1502866612361%3B4%3B28; ki_r=; __gads=ID=8dae930bd158f027:T=1500348105:S=ALNI_MZvrWnxouBHmGmcVzzDA-FB5qSN8g; idp_session_http=hVERSION_192b689a0-dd51-4bc1-a592-b9fa40cbc931; idp_marker=e3323f52-bd1b-476b-9b19-b4030c361e3a; __VCAP_ID__=39c0598b-40a6-4be9-4b11-93905a1cbdbd; JSESSIONID=nqmvaskesp0z1g3ivbvbvixud; SaneID=10.1.1.227.1502796007162479; __ar_v4=; _gid=GA1.2.1397929322.1502796014; referral_cookie=82; persistent_test=563208467@gx.sva&|60aVXbcA7/ic6&|0; login=563208467@gx.sva&|60aVXbcA7/ic6&|0; user.uuid=aa0877c09a7a72a14f9370ef73173b0e35c0b462"
        }
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        resultList = soup.find_all(attrs={"class":"h3 extra-tight-line-height"})
        item = NatureItem()
        for result in resultList:
            try:
                url = result.a.get('href')
                item['fullUrl'] = url
                request = scrapy.Request(url=url, callback=self.parse_fullInfo, headers=headers, meta={'item': item}, dont_filter=True)
                # request = scrapy.Request(url=url, callback=self.parse_full, headers=headers, meta={'item': item}, dont_filter=True)
                yield request
            except:
                print "Can not find fullInfoUrl"

    '''plan A'''
    def parse_fullInfo(self,response):
            headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest",
            "Cookie":"user.uuid=5a01aae3-e377-4e07-a07b-1b31f4dcffa7; __gads=ID=cb96fea7a634dd1b:T=1500515613:S=ALNI_Mb6mXrSZbm5xG_m1qJMqdWVG_YLPw; _polar_tu=*_%22mgtn%22_@2Q_u_@_daa4bf27-fa6f-4be5-9f3b-176a11ceb142_Q_n_@3Q_s_@1Q_sc_@*_v_@2Q_a_@2+Q_ss_@_%22otd9t5_Q_sl_@_%22otd9t5_Q_sd_@*+Q_v_@_2%5B288ebcc_Q_vc_@*_e_@1+Q_vs_@_%22otd9t5_Q_vl_@_%22otd9t5_Q_vd_@*+Q_vu_@_b90a8da825664a9c7f9d4ca17048600e_Q_vf_@_%22j5bsocdp_+; ebBurstingTime_.www.nature.com=1500517176113; ebNewHistory_.www.nature.com=21656454%3A1500517176113%3A11%3A1500515627073%3A11; idp_session=sVERSION_1295e5fdd-fba0-4a37-b57b-7dd2ff2ab6ed; idp_session_http=hVERSION_15cbc5053-2dd2-4780-aded-4a1ef383119e; idp_marker=a5bd50f5-3cb2-4da5-b2b0-aeaef8346cbc; SaneID=10.1.1.224.1502697284816074; referral_cookie=82; euCookieNotice=accepted; JSESSIONID=n4rkcyns6gv11akz8yb26achu; requestURL=http://www.nature.com/nams/svc/athenslogin; WT_FPC=id=5da88257-3cd3-49f1-b265-189ed5fcfc00:lv=1502748727673:ss=1502746783342; NatureRegistrationLogin=563208467@gx.sva&|60aVXbcA7/ic6&|0; __ar_v4=; _ga=GA1.2.1421928346.1500515609; _gid=GA1.2.1425480635.1502697288; ki_t=1500515613373%3B1502763916618%3B1502795627887%3B5%3B232; ki_r=; __VCAP_ID__=262a6c4e-8bf7-4f29-632e-6404d122c17f"
        }
            soup = BeautifulSoup(response.body_as_unicode(),"lxml")
            item = response.meta['item']
            authors = []
            keys = []
            references = []
        # try:
            a_temp = soup.find('div',attrs={"id":"abstract"})
            if a_temp is None:
                temp = soup.find('div',attrs={"class":"section first no-nav no-title first-no-nav"})
            else:
                temp = a_temp
            temp_1 = temp.find('div',attrs={"class":"content"})
            '''plan A B for Abstract'''
            item['Abstract'] = temp_1.p.get_text(strip=True)
            '''标题 Only'''
            item['Title'] = soup.find('h1',attrs={"class":"article-heading"}).get_text()
            au_temp = soup.find('ul',attrs={"class":"authors citation-authors"})
            authorList = au_temp.find_all('a',attrs={"class":"name"})
            for author in authorList:
                au_result = author.span.get_text()
                authors.append(au_result)
            '''作者 Only'''
            item['Author'] = authors
            info_temp = soup.find('dl',attrs={"class":"citation"})
            '''期刊'''
            PublisherOrConference = info_temp.find(attrs={"class":"journal-title"}).get_text()
            if PublisherOrConference is None:
                item['PublisherOrConference'] = ""
            else:
                item['PublisherOrConference'] = info_temp.find(attrs={"class":"journal-title"}).get_text()
            '''详情'''
            Volume = info_temp.find('dd',attrs={"class":"volume"})
            if Volume is None:
                item['Volume'] = ""
            else:
                item['Volume'] = Volume.get_text(strip=True)
            '''页面'''
            Pages = info_temp.find('dd',attrs={"class":"page"})
            if Pages is None:
                item['Pages'] = ""
            else:
                item['Pages'] = Pages.get_text()
            '''doi'''
            doi = info_temp.find('dd',attrs={"class":"doi"})
            if doi is None:
                item['doi'] = ""
            else:
                item['doi'] = doi.get_text()
            '''发表时间'''
            Time = info_temp.time.get('datetime')
            if Time is None:
                item['Time'] = ""
            else:
                item['Time'] = info_temp.time.get('datetime')
            '''关键词'''
            key_temp = soup.find('div',attrs={"class":"article-keywords inline-list cleared"})
            if key_temp is None:
                keys = ""
            else:
                keywords = key_temp.find_all('li')
                for keyword in keywords:
                    key_result = keyword.get_text()
                    keys.append(key_result)
            item['Keywords'] = keys
            '''引文'''
            ref_temp = soup.find('ol',attrs={"class":"references"})
            if ref_temp is None:
                references = ""
            else:
                refs = ref_temp.find_all('li')
                for ref in refs:
                    ref_del_0 = ref.get_text()
                    ref_del_1 = ref_del_0.replace('PubMed','')
                    ref_del_1.strip()
                    ref_del_2 = ref_del_1.replace('CAS','')
                    ref_del_2.strip()
                    ref_del_3 = ref_del_2.replace('ISI','')
                    ref_del_3.strip()
                    ref_del_4 = ref_del_3.replace('Article','')
                    ref_del_4.strip()
                    ref_result = ref_del_4.replace('Show context','')
                    references.append(ref_result)

            while '\n' in references:
                references.remove('\n')
            item['Reference'] = references

            '''作者信息'''
            auinfos = []
            auinfo_tag = soup.find('div',attrs={"id":"author-affiliations"})
            if auinfo_tag is None:
                auinfos = ""
            else:
                aunfo_temp = auinfo_tag.find('ol',attrs={"class":"affiliations"})
                infos = aunfo_temp.find_all('li')
                for info in infos:
                    auinfo = info.get_text()
                    auinfos.append(auinfo)
            item['AuthorInfo'] = auinfos

            metrics_tag = soup.find('li',attrs={"class":"article-metrics"})
            metrics = metrics_tag.a.get('href')
            metrics_url = "https://www.nature.com"+metrics
            request = scrapy.Request(url=metrics_url, callback=self.parse_metrics, headers=headers, meta={'item': item}, dont_filter=True)
            yield request

            # doi_temp = str(doi).replace('doi:','')
            # cite_url = 'http://xueshu.baidu.com/s?wd=' + doi_temp
            # request = scrapy.Request(url=cite_url, callback=self.parse_cite, headers=headers, meta={'item': item}, dont_filter=True)


        # except:
        #     print "Can not get full Info"
    #
    # '''plan B'''
    # def parse_full(self,response):
    #     headers = {
    #         "Accept":"*/*",
    #         "Accept-Encoding":"gzip, deflate",
    #         "Accept-Language":"zh-CN,zh;q=0.8",
    #         "Connection":"keep-alive",
    #         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    #         "X-Requested-With":"XMLHttpRequest",
    #         "Cookie":"user.uuid=5a01aae3-e377-4e07-a07b-1b31f4dcffa7; __gads=ID=cb96fea7a634dd1b:T=1500515613:S=ALNI_Mb6mXrSZbm5xG_m1qJMqdWVG_YLPw; _polar_tu=*_%22mgtn%22_@2Q_u_@_daa4bf27-fa6f-4be5-9f3b-176a11ceb142_Q_n_@3Q_s_@1Q_sc_@*_v_@2Q_a_@2+Q_ss_@_%22otd9t5_Q_sl_@_%22otd9t5_Q_sd_@*+Q_v_@_2%5B288ebcc_Q_vc_@*_e_@1+Q_vs_@_%22otd9t5_Q_vl_@_%22otd9t5_Q_vd_@*+Q_vu_@_b90a8da825664a9c7f9d4ca17048600e_Q_vf_@_%22j5bsocdp_+; ebBurstingTime_.www.nature.com=1500517176113; ebNewHistory_.www.nature.com=21656454%3A1500517176113%3A11%3A1500515627073%3A11; idp_session=sVERSION_1295e5fdd-fba0-4a37-b57b-7dd2ff2ab6ed; idp_session_http=hVERSION_15cbc5053-2dd2-4780-aded-4a1ef383119e; idp_marker=a5bd50f5-3cb2-4da5-b2b0-aeaef8346cbc; SaneID=10.1.1.224.1502697284816074; referral_cookie=82; euCookieNotice=accepted; JSESSIONID=n4rkcyns6gv11akz8yb26achu; requestURL=http://www.nature.com/nams/svc/athenslogin; WT_FPC=id=5da88257-3cd3-49f1-b265-189ed5fcfc00:lv=1502748727673:ss=1502746783342; NatureRegistrationLogin=563208467@gx.sva&|60aVXbcA7/ic6&|0; __ar_v4=; _ga=GA1.2.1421928346.1500515609; _gid=GA1.2.1425480635.1502697288; ki_t=1500515613373%3B1502763916618%3B1502795627887%3B5%3B232; ki_r=; __VCAP_ID__=262a6c4e-8bf7-4f29-632e-6404d122c17f"
    #     }
    #     soup = BeautifulSoup(response.body_as_unicode(),"lxml")
    #     item = response.meta['item']
    #     info_temp = soup.find('font',attrs={"face":"times, times new roman, serif"}).get_text()
    #     item['FullInfo'] = info_temp


    def parse_metrics(self,response):
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest",
            "Cookie":"user.uuid=5a01aae3-e377-4e07-a07b-1b31f4dcffa7; __gads=ID=cb96fea7a634dd1b:T=1500515613:S=ALNI_Mb6mXrSZbm5xG_m1qJMqdWVG_YLPw; _polar_tu=*_%22mgtn%22_@2Q_u_@_daa4bf27-fa6f-4be5-9f3b-176a11ceb142_Q_n_@3Q_s_@1Q_sc_@*_v_@2Q_a_@2+Q_ss_@_%22otd9t5_Q_sl_@_%22otd9t5_Q_sd_@*+Q_v_@_2%5B288ebcc_Q_vc_@*_e_@1+Q_vs_@_%22otd9t5_Q_vl_@_%22otd9t5_Q_vd_@*+Q_vu_@_b90a8da825664a9c7f9d4ca17048600e_Q_vf_@_%22j5bsocdp_+; ebBurstingTime_.www.nature.com=1500517176113; ebNewHistory_.www.nature.com=21656454%3A1500517176113%3A11%3A1500515627073%3A11; idp_session=sVERSION_1295e5fdd-fba0-4a37-b57b-7dd2ff2ab6ed; idp_session_http=hVERSION_15cbc5053-2dd2-4780-aded-4a1ef383119e; idp_marker=a5bd50f5-3cb2-4da5-b2b0-aeaef8346cbc; SaneID=10.1.1.224.1502697284816074; referral_cookie=82; euCookieNotice=accepted; JSESSIONID=n4rkcyns6gv11akz8yb26achu; requestURL=http://www.nature.com/nams/svc/athenslogin; WT_FPC=id=5da88257-3cd3-49f1-b265-189ed5fcfc00:lv=1502748727673:ss=1502746783342; NatureRegistrationLogin=563208467@gx.sva&|60aVXbcA7/ic6&|0; __ar_v4=; _ga=GA1.2.1421928346.1500515609; _gid=GA1.2.1425480635.1502697288; ki_t=1500515613373%3B1502763916618%3B1502795627887%3B5%3B232; ki_r=; __VCAP_ID__=262a6c4e-8bf7-4f29-632e-6404d122c17f"
        }
        item = response.meta['item']

        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
        # dcap["phantomjs.page.settings.cookie"] = ("msacademic=d05c2157-9e54-48ff-ab2b-43864b29430b; ai_user=Ll7Cm|2017-08-29T08:29:14.651Z; ARRAffinity=03dbaf7ebccf3a5270373d2bf50d0eea48778d1e5597aa06ff24fffe7ddcb12c; ai_session=ATGmx|1507543708952.43|1507548269298.4")
        # dcap["phantomjs.page.settings.loadImages"] = False
        # browser = webdriver.PhantomJS(desired_capabilities=dcap)
        # browser.implicitly_wait(1)
        # browser.get(response.url)
        # time.sleep(1)
        # soup = BeautifulSoup(browser.page_source,"lxml")
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        metricData = []
        TwitterMap = {}
        metric_tag= soup.find('div',attrs={"class":"altmetric-key"})
        if metric_tag is None:
            metricData = ""
        else:
            metrics = metric_tag.ul.find_all('li',attrs={"class":"altmetric"})
            for metric in metrics:
                data = metric.get_text()
                metricData.append(data)
        item['MetricData'] = metricData

        means_tag = soup.find('div',attrs={"class":"altmetric-context"})
        if means_tag is None:
            means = ""
        else:
            means = means_tag.get_text(strip=True)
        item['MetricMeans'] = means

        cite_tag = soup.find('ul',attrs={"class":"citation-summary cleared"})
        WosCite_tag = cite_tag.find(attrs={"data-link-type":"web of science"})
        if WosCite_tag is None:
            woscite = ""
        else:
            woscite = WosCite_tag.get_text(strip=True)
        item['WosCite'] = woscite

        CRCite_tag = cite_tag.find(attrs={"data-link-type":"crossref"})
        if CRCite_tag is None:
            crcite = ""
        else:
            crcite = CRCite_tag.get_text(strip=True)
        item['CRCite'] = crcite

        ScopusCite_tag = cite_tag.find(attrs={"data-link-type":"scopus"})
        if ScopusCite_tag is None:
            scopuscite = ""
        else:
            scopuscite = ScopusCite_tag.get_text(strip=True)
        item['ScopusCite'] = scopuscite

        # map_tag = soup.find(attrs={"class":"twitter-demographic-table"})

        context_url = response.url+"/news"
        request = scrapy.Request(url=context_url, callback=self.parse_context, headers=headers, meta={'item': item}, dont_filter=True)
        yield request


    def parse_context(self,response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        contexts = {}
        Content = []
        list_tag = soup.find('div',attrs={"class":"metrics-module citation-list"})
        if list_tag is None:
            item['Contexts'] = "Null"
        else:
            list_temp = list_tag.find('ol',attrs={"class":"results-list"})
            lists = list_temp.find_all('li')
            for list in lists:
                time_tag = list.find('span',attrs={"class":"date"})
                if time_tag is None:
                    Time = ""
                else:
                    Time = time_tag.get_text(strip=True)
                title_tag = list.find('h3',attrs={"class":"at1"})
                if title_tag is None:
                    title = ""
                else:
                    title = time_tag.get_text()
                content_tag = list.find('p')
                if content_tag is None:
                    content = ""
                else:
                    content = content_tag.get_text()
                publisher_tag = list.find('span',attrs={"class":"metric-authors"})
                if publisher_tag is None:
                    publisher = ""
                else:
                    publisher = publisher_tag.get_text()

                contexts = dict(time=Time,title=title,content=content,publisher=publisher)
                Content.append(contexts)

            item['Contexts'] = Content
        yield item








    # def parse_cite(self,response):
    #     item = response.meta['item']
    #     soup = BeautifulSoup(response.body_as_unicode(),"lxml")
    #     try:
    #         cite = soup.find('div',attrs={'class':'ref_wr'}).get_text(strip=True)
    #         item['Cite'] = cite
    #         yield item
    #     except:
    #         print "Can't get CiteNum"














