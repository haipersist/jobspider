#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
run spider in two different ways

it can run in single spider ,selected from BYR,Lagou,Zhilian,51Job or
run in multiprocessing


Default,the data that spider crawls will be stored into json file ,of course,you can
store into MySQL,excel or redis by setting store type.

"""


import time,timeit
import datetime
from multiprocessing import Pool,Manager
from byr import BYR_Spider
from lagou import LG_Spider
from zhilian import ZL_Spider
from job51 import Job51_Spider
from dajie import DJ_Spider
from utils.store_data import Job_Data
from utils.get_cookies import get_cookie



class Spider():

    spiders = {
        'byr':BYR_Spider('byr','X-Requested-With','Host','Referer'),
        'lagou':LG_Spider('lagou'),
        'zhilian':ZL_Spider('zhilian'),
        '51job':Job51_Spider('51job','Host','Cookie'),
         'dajie':DJ_Spider('dajie','X-Requested-With','Host','Referer','Cookie')
               }
    def __init__(self,keyword,store_type='json'):
        self.keyword = keyword
        self.store_type = store_type

    def get_single_data(self,spiname):
        self.spider = self.spiders[spiname]
        data = self.spider.pages_parse(self.keyword)
        return data

    def single_run(self,spiname):
        db = Job_Data(self.store_type)
        for data in self.get_single_data(spiname):
            db.store(data)

    def single_print(self,spiname):
        for data in self.get_single_data(spiname):
            for item in data:
                for key,value in item.items():
                    print "%s : %s" %(key,value),
                print '\n'

    def multi_run(self,spiname,lock):
        db = Job_Data(self.store_type)
        for data in self.get_single_data(spiname):
            lock.acquire()
            #print data
            db.store(data)
            lock.release()


def crawl(sitename,lock):
    spider = Spider('python')
    spider.multi_run(sitename,lock)

def producer():
    lock = Manager().Lock()
    p = Pool()
    sites = ['zhilian', '51job','byr','lagou','dajie']
    for site in sites:
        p.apply_async(crawl,args=(site,lock))
    p.close()
    p.join()







if __name__=="__main__":
    spider = Spider('python')
    for item in  spider.get_single_data('dajie'):
        print item
    #producer()







