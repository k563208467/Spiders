# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pymongo import MongoClient
from scrapy.conf import settings

class TutorialPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings[ 'MONGODB_SERVER' ],
            settings[ 'MONGODB_PORT' ]
        )
        db = connection[settings['MONGODB_DB1']]
        db2 = connection[settings['MONGODB_DB2']]
        self.test1 = db[settings['MONGODB_COLLECTION']]
        self.test2 = db2[settings['MONGODB_COLLECTION']]

        # self.coll = db[settings['MONGODB_COLLECTION7']]
        # self.coll2 = db[settings['MONGODB_COLLECTION7']]
        # self.peo = db[settings['MONGODB_COLLECTION3']]
        # self.MSpeo = db[settings['MONGODB_COLLECTION4']]
        # self.nature = db[settings['MONGODB_COLLECTION5']]
        # self.nature2 = db[settings['MONGODB_COLLECTION6']]
        # self.pnas = db[settings['MONGODB_COLLECTION8']]


    def process_item(self, item, spider):
        if spider.name == 'bing':
            self.test1.update({'title': item['Title']},{'$set':dict(item)},True)
        if spider.name == 'bing2':
            self.test1.update({'title': item['Title']},{'$set':dict(item)},True)
        if spider.name == 'bing4':
            self.test2.update({'name': item['Name']},{'$set':dict(item)},True)
        # if spider.name == 'MicroSoftPeople':
        #     self.MSpeo.update({'name': item['Name']},{'$set':dict(item)},True)
        # if spider.name == 'nature':
        #     self.nature.update({'title': item['Title']},{'$set':dict(item)},True)
        # if spider.name == 'nature2':
        #     self.nature2.update({'title': item['Title']},{'$set':dict(item)},True)
        # if spider.name == 'pnas':
        #     self.pnas.update({'title': item['Title']},{'$set':dict(item)},True)
        return item

