# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    IP = scrapy.Field()
    Port = scrapy.Field()
    Position = scrapy.Field()
    Type = scrapy.Field()
    Speed = scrapy.Field()
    LAST_CHECK_TIME = scrapy.Field()


class IeeeItem(scrapy.Item):
    Result = scrapy.Field()
    Title = scrapy.Field()
    Author = scrapy.Field()
    AuthorInfo = scrapy.Field()
    Abstract = scrapy.Field()
    PublisherOrConference = scrapy.Field()
    Volume = scrapy.Field()
    Issue = scrapy.Field()
    Pages = scrapy.Field()
    Time = scrapy.Field()
    Keywords = scrapy.Field()
    Category = scrapy.Field()

class PnasItem(scrapy.Item):
    Result = scrapy.Field()
    Title = scrapy.Field()
    Author = scrapy.Field()
    AuthorInfo = scrapy.Field()
    Abstract = scrapy.Field()
    PublisherOrConference = scrapy.Field()
    Volume = scrapy.Field()
    Issue = scrapy.Field()
    Pages = scrapy.Field()
    Time = scrapy.Field()
    Keywords = scrapy.Field()
    doi = scrapy.Field()
    Reference = scrapy.Field()
    fullUrl = scrapy.Field()
    abstractUrl = scrapy.Field()
    Extract = scrapy.Field()
    CiteNum = scrapy.Field()

class TestItem(scrapy.Field):
    Result = scrapy.Field()
    Cite = scrapy.Field()

class NatureItem(scrapy.Item):
    Title = scrapy.Field()
    Author = scrapy.Field()
    AuthorInfo = scrapy.Field()
    PaperInfo = scrapy.Field()
    Abstract = scrapy.Field()
    PublisherOrConference = scrapy.Field()
    Volume = scrapy.Field()
    Issue = scrapy.Field()
    Pages = scrapy.Field()
    Time = scrapy.Field()
    FullInfo = scrapy.Field()
    Keywords = scrapy.Field()
    doi = scrapy.Field()
    Reference = scrapy.Field()
    fullUrl = scrapy.Field()
    WebOfScience = scrapy.Field()
    CrossRef = scrapy.Field()
    Scopus = scrapy.Field()
    MetricData = scrapy.Field()
    MetricMeans = scrapy.Field()
    ArticlesCiting = scrapy.Field()
    Contexts = scrapy.Field()
    twitterDemographics = scrapy.Field()
    ScopusCitedLiterature = scrapy.Field()


class PhysItem(scrapy.Item):
    Title = scrapy.Field()
    Author = scrapy.Field()
    AuthorInfo = scrapy.Field()
    Abstract = scrapy.Field()
    PublisherOrConference = scrapy.Field()
    ArticleInfo = scrapy.Field()
    Keywords = scrapy.Field()
    Reference = scrapy.Field()
    fullUrl = scrapy.Field()
    Cite = scrapy.Field()

class BingItem(scrapy.Item):
    Title = scrapy.Field()
    Author = scrapy.Field()
    AuthorInfo = scrapy.Field()
    Abstract = scrapy.Field()
    Publisher = scrapy.Field()
    Volume = scrapy.Field()
    Issue = scrapy.Field()
    Pages = scrapy.Field()
    Date = scrapy.Field()
    Keywords = scrapy.Field()
    Doi = scrapy.Field()
    Reference = scrapy.Field()
    Citation = scrapy.Field()
    fullUrl = scrapy.Field()
    citeNum = scrapy.Field()

class PersonItem(scrapy.Item):
    Name = scrapy.Field()
    Mechanism = scrapy.Field()
    CiteNum = scrapy.Field()
    PaperNum = scrapy.Field()
    HomePage = scrapy.Field()
    ResearchTopics = scrapy.Field()
    PublishedConferences = scrapy.Field()
    PublishedJournals = scrapy.Field()
    CoAuthors = scrapy.Field()
    CoAffiliations = scrapy.Field()

class PaperItem(scrapy.Item):
    Title = scrapy.Field()
