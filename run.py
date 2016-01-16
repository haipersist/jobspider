#!/usr/bin/python
# -*- coding:utf-8 -*-


import time,timeit
from multiprocessing import Pool,Manager
from jobspider import BYR_Spider,LG_Spider,ZL_Spider,Job51_Spider


lock = Manager().Lock()


def crawl(website,keyword='python'):
    spider = Job_Spider(keyword,website)
    jobdata = []
    for l in spider.parse():
        for item in l:
            jobdata.append(item)
    lock.acquire()
    spider.store_in_console(jobdata)
    lock.release()


def producer():
    p = Pool()
    sites = ['zhilian', 'job51','byr']
#p.map(crawl,sites)
    for website in sites:
        p.apply_async(crawl,args=(website,))
    p.close()
    p.join()
    print 'All processes Done!'



if __name__=="__main__":
    #do not add host
    #lg = LG_Spider('lagou')
    #print lg.headers
    #lg.pages_parse('python')
    #byr = BYR_Spider('byr','X-Requested-With','Host','Referer')
    #byr.pages_parse('python')
    #print byr.headers







