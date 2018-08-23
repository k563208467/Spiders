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
    name = 'webofscience'
    allowed_domains = ["https://www.nature.com"]
    start_urls = ('http://apps.webofknowledge.com/AutoSave_UA_GeneralSearch_input.do?action=saveForm&SID=7CTaRMgAPHwTENlxztl&product=UA&search_mode=GeneralSearch',
                  )


    def start_requests(self):
        url = 'http://apps.webofknowledge.com/AutoSave_UA_GeneralSearch_input.do?action=saveForm&SID=7CTaRMgAPHwTENlxztl&product=UA&search_mode=GeneralSearch'
        doi = "10.1038/526196a",
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            cookies={"JSESSIONID":"8423207F8D40FA16CE93A1CF385D7421",},
            formdata = {"fieldCount" : "1", "action" : "search","SID" : "7CTaRMgAPHwTENlxztl","max_field_count" : "100","formUpdated" : "ture",
                        "value(input1)" : doi,"value(select1)":"DO","sa_params":"UA||7CTaRMgAPHwTENlxztl|http://apps.webofknowledge.com|'","period":"Range Selection"},
            callback = self.parse
        )


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
        print response.body
