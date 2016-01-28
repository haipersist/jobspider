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
import os
from multiprocessing import Pool,Manager
from byr import BYR_Spider
from lagou import LG_Spider
from zhilian import ZL_Spider
from job51 import Job51_Spider
from utils.store_data import Job_Data
from utils.setcolor import *


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

    def print_output(self,spiname):
        #In Linux,it will print data with colored
        for data in self.get_single_data(spiname):
            for item in data:
                for key,value in item.items():
                    if os.name == 'posix':
                        print '{0}:{1}'.format(red(key),value),
                    else:
                        print '{0}:{1}'.format(key,value),
                print '\n'

    def get_data(self,spiname):
        select = raw_input('you want put data into terminal or json(write terminal or json):')
        if select == 'terminal':
            self.print_output(spiname)
        elif select == 'json':
            self.single_run(spiname)
        else:
            print 'your input is incorrect,it must be terminal or json'

    def multi_run(self,spiname):
        print spiname
        self.single_run(spiname)


def crawl(spi,lock):
    spider = Spider('python')
    lock.acquire()
    spider.multi_run(spi)
    lock.release()


def producer(lock):
    p = Pool()
    sites = ['zhilian', '51job','byr','lagou']
    for site in sites:
        p.apply_async(crawl,args=(site,lock))
    p.close()
    p.join()






if __name__=="__main__":
    lock = Manager().Lock()
    spider = Spider('python')
    spider.get_data('zhilian')
    producer(lock)







