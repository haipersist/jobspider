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
from utils.store_data import Job_Data



class Spider():

    spiders = {
        'byr':BYR_Spider('byr','X-Requested-With','Host','Referer'),
        'lagou':LG_Spider('lagou'),
        'zhilian':ZL_Spider('zhilian'),
        '51job':Job51_Spider('51job','Host','Cookie')
               }
    def __init__(self,keyword,store_type='json'):
        self.keyword = keyword
        self.store_type = store_type

    def get_single_data(self,spiname):
        self.spider = self.spiders[spiname]
        return self.spider.pages_parse(self.keyword)

    def single_run(self,spiname):
        db = Job_Data(self.store_type)
        for data in self.get_single_data(spiname):
            db.store(data)

    def multi_run(self,spiname):
        db = Job_Data(self.store_type)
        for data in self.get_single_data(spiname):
            lock.acquire()
            db.store(data)
            lock.release()

    def producer(self):
        p = Pool()
        sites = ['zhilian', '51job','byr','lagou']
        for site in sites:
            p.apply_async(self.multi_run,args=(site,))
        p.close()
        p.join()







if __name__=="__main__":
    lock = Manager().Lock()
    spider = Spider('python')
    spider.single_run('lagou')
    #spider.producer()







