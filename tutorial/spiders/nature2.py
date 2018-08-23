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
from scrapy import log


class PnasSpider(scrapy.Spider):
    name = 'nature2'
    allowed_domains = ["https://www.nature.com"]
    start_urls = ('https://www.nature.com/search?article_type=research&journal=nature&order=relevance&page=500',
                  )


    def start_requests(self):
        reqs = []

        for i in range(1,873):
            url = "https://www.nature.com/search?date_range=2000-2017&journal=natrevmats,nrmicro,nrm,nrneph,natrevphys,nrrheum,nrurol,nrdp,nsmb,natsustain&order=relevance&page=%d"%i
            req = scrapy.Request(url,dont_filter=True)
            reqs.append(req)
        return reqs


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
        # item = NatureItem()
        for result in resultList:
            url_temp = result.a.get('href')

            if re.findall(r"full/(\w+).",url_temp) == []:
                url_list = re.findall(r"abs/(\w+).",url_temp)
                if url_list == []:
                    url_result = re.findall(r"pdf/(\w+).",url_temp)
                else:
                    url_result = url_list
            else:
                url_result = re.findall(".*full/(.*).html.*",url_temp)
            url_num = url_result[0]
            url = "https://www.nature.com/articles/" + url_num
            # item['fullUrl'] = url
            request = scrapy.Request(url=url, callback=self.parse_fullInfo, headers=headers, meta={'handle_httpstatus_list': [301,302]}, dont_filter=True)
            request.meta['dont_redirect'] = True
            yield request


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
            item = NatureItem()
            item['fullUrl'] = response.url
            authors = []
            keys = []
            references = []
        # try:
            a_temp = soup.find('div',attrs={"class":"pl20 mq875-pl0 js-collapsible-section"})
            '''摘要'''
            if a_temp is None:
                abstract = ""
            else:
                abstract = a_temp.get_text()
            item['Abstract'] = abstract

            '''标题 Only'''
            item['Title'] = soup.find('h1',attrs={"class":"tighten-line-height small-space-below"}).get_text()

            '''作者名字'''
            aus = []
            au_temps = soup.find_all('li',attrs={"itemprop":"author"})
            if au_temps is None:
                aus = ""
            else:
                for au_temp in au_temps:
                    au = au_temp.get_text()
                    aus.append(au)
            item['Author'] = aus

            '''期刊信息'''
            info_temp = soup.find('ul',attrs={"class":"flex-box-item none border-gray-medium border-left-1 text14 ma0 pa0 pl10"})

            if info_temp is None:
                info_temp2 = soup.find('dl',attrs={"data-component":"article-info-list"})
                if info_temp2 is None:
                    item['PaperInfo'] = ""
                    item['doi'] = ""
                else:
                    PaperInfo = info_temp2.find_all('dd')
                    item['PaperInfo'] = PaperInfo[0].get_text()
                    item['doi'] = PaperInfo[1].get_text()
            else:
                PaperInfo = info_temp.find_all('li')
                item['PaperInfo'] = PaperInfo[0].get_text()
                item['doi'] = PaperInfo[1].get_text()

            if info_temp is None:
                item['Keywords'] = ""
            else:
                keys_tag = info_temp.find('ul',attrs={"class":"mb0 pa0 tiny-space-above inline-list text14"})
                if  keys_tag is None:
                    item['Keywords'] = ""
                else:
                    item['Keywords'] = keys_tag.get_text()

            '''引文'''
            ref_temp = soup.find('ol',attrs={"class":"clean-list ma0 standard-space-below indented-list"})

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

            item['Reference'] = references


            '''作者信息'''
            auinfos = []
            auinfo_temp = soup.find('div',attrs={"id":"author-information-content"})
            if auinfo_temp is None:
                auinfos = ""
            else:
                temp = auinfo_temp.find('ol',attrs={"class":"clean-list"})
                infos = temp.find_all('li')
                for info in infos:
                    auinfo = info.get_text()
                    auinfos.append(auinfo)
            item['AuthorInfo'] = auinfos

            metrics_url = response.url + "/metrics"
            request = scrapy.Request(url=metrics_url, callback=self.parse_metrics, headers=headers, meta={'item': item}, dont_filter=True)
            yield request

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

        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        metricData = []
    #     TwitterMap = {}
        metric_tag = soup.find('div',attrs={"class":"grid grid-8 last small-space-below"})

        if metric_tag is None:
            metricData = ""
        else:
            metrics = metric_tag.find_all('li')
            if metrics is None:
                metricData = ""
            else:
                for metric in metrics:
                    data = metric.get_text()
                    metricData.append(data)
        item['MetricData'] = metricData

        main_tag = soup.find('div',attrs={"class":"grid grid-6 grid-left-1 last mq875-grid-12 just-mq875-last mq875-kill-left standard-space-below"})
        if main_tag is None:
            means = ""
        else:
            means_tag = main_tag.find('div',attrs={"class":"grid grid-12 last"})
            if means_tag is None:
                means = ""
            else:
                means = means_tag.get_text(strip=True)
        item['MetricMeans'] = means

        cite_tag = soup.find('ul',attrs={"class":"clean-list ma0 pa0 cleared"})
        if cite_tag is None:
            woscite = ""
            crcite = ""
            scopuscite = ""
        else:
            WosCite_tag = cite_tag.find("li",attrs={"class":"grid grid-4"})
            if WosCite_tag is None:
                woscite = ""
            else:
                woscite = WosCite_tag.get_text(strip=True)
            item['WebOfScience'] = woscite

            CRCite_temp = cite_tag.find('h3',text="CrossRef")
            if CRCite_temp is None:
                crcite = ""
            else:
                CRCite_tag = CRCite_temp.find_parent()
                if CRCite_tag is None:
                    crcite = ""
                else:
                    crcite = CRCite_tag.get_text(strip=True)
            item['CrossRef'] = crcite

            ScopusCite_tag = cite_tag.find('li',attrs={"class":"grid grid-4 last"})
            if ScopusCite_tag is None:
                scopuscite = ""
            else:
                scopuscite = ScopusCite_tag.get_text(strip=True)
            item['Scopus'] = scopuscite

            article_data = {}
            article_list = []
            metricMentions = soup.find('div',attrs={"data-test":"metrics-mentions"})
            if metricMentions is None:
                article_list = ""
            else:
                context_temp = metricMentions.find('ul',attrs={"class":"serif clean-list ma0 pa0"})
                articles = context_temp.find_all('li')
                for article in articles:
                    title = article.find('a').get_text()
                    media = article.find('span').get_text()
                    article_data = dict(title=title,media=media)
                    article_list.append(article_data)
            item['Contexts'] = article_list

            twitterGraphs = []
            twitterGraph = soup.find('div',attrs={"data-test":"metrics-twitter"})
            if twitterGraph is None:
                twitterGraphList = ""
            else:
                twitterGraph_temp = twitterGraph.find('div',attrs={"class":"scroll-wrapper table-highlight"})
                twitterGraph_tag = twitterGraph_temp.find('tbody')
                countryTags = twitterGraph_tag.find_all('tr')
                for countryTag in countryTags:
                    country = countryTag.get_text()
                    twitterGraphs.append(country)
                twitterGraphList = twitterGraphs
            item['twitterDemographics']= twitterGraphList


            '''?'''
            url_temp = ScopusCite_tag.find('a')
            url_scopus = url_temp.get('href')
            request = scrapy.Request(url=url_scopus, callback=self.parse_scopus, headers=headers, meta={'item': item}, dont_filter=True)
            yield request


        # context_url = response.url+"/news"

    def parse_scopus(self,response):
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
        data = {}
        dataList = []
        soup = BeautifulSoup(response.body_as_unicode(),"lxml")
        main_tag = soup.find('ul',attrs={"id":"documentListUl"})
        if main_tag is None:
            item['ScopusCitedLiterature'] = ""
        else:
            tags = main_tag.find_all('li')
            for tag in tags:
                data_tag = tag.find('div',attrs={"class":"docMain"})
                if data_tag is None:
                    data = ""
                else:
                    title_tag = data_tag.find('span',attrs={"class":"docTitle"})
                    if title_tag is None:
                        title = ""
                    else:
                        title = title_tag.get_text()
                    authors_tag = data_tag.find('span',attrs={"class":" displayInlineBlock"})
                    if authors_tag is None:
                        authors = ""
                    else:
                        authors = authors_tag.get_text()
                    year_tag = data_tag.find('div',attrs={"class":"dataCol4"})
                    if year_tag is None:
                        year = ""
                    else:
                        year = year_tag.get_text()

                    publiser_tag = data_tag.find('div',attrs={"class":"dataCol5"})
                    if publiser_tag is None:
                        publiser = ""
                    else:
                        publiser = publiser_tag.get_text()

                    citeNum_tag = data_tag.find('div',attrs={"class":"dataCol6"})
                    if citeNum_tag is None:
                        citeNum = ""
                    else:
                        citeNum = citeNum_tag.get_text()

                    data = dict(title=title,authors=authors,year=year,publiser=publiser,citeNum=citeNum)
                dataList.append(data)
            item['ScopusCitedLiterature'] = dataList

        yield item




















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
