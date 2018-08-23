# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TutorialSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class MSPageMiddleware(object):
    def process_request(self,request,spider):
        if request.meta.has_key('PhantomJS'):
                print"PhantomJS is starting..."
                dcap = dict(DesiredCapabilities.PHANTOMJS)
                dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
                dcap["phantomjs.page.settings.cookie"] = ("msacademic=d05c2157-9e54-48ff-ab2b-43864b29430b; ai_user=Ll7Cm|2017-08-29T08:29:14.651Z; ARRAffinity=03dbaf7ebccf3a5270373d2bf50d0eea48778d1e5597aa06ff24fffe7ddcb12c; ai_session=ATGmx|1507543708952.43|1507548269298.4")
                dcap["phantomjs.page.settings.loadImages"] = False
                browser = webdriver.PhantomJS(desired_capabilities=dcap)
                browser.implicitly_wait(5)
                browser.get(request.url)
                print "beginning to get"
                time.sleep(8)
                shows = browser.find_elements_by_link_text("Show More")
                for show in shows:
                    show.click()
                time.sleep(1)
                content = browser.page_source
                # browser.quit()
                return HtmlResponse(browser.current_url, body=content, encoding='utf-8', request=request)
