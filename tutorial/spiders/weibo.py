# -*- coding: UTF-8 -*-
from pymongo import MongoClient
# -*- coding: utf-8 -*-
import scrapy
import os
import json
import requests
import time
import copy
import string
#
# root = "C:\Users\ylaxfcy\py\data_google_scholar"
# list = os.listdir(root)
# temp = 0
# for i in list:
#     with open(root+"\\"+i,"r") as f:
#         lines = len(f.readlines())
#         temp += lines
#     print temp
