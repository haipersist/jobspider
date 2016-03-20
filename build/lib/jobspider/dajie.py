#!/usr/bin/python
# -*- coding:utf-8 -*-


from baseclass.base_spider import Base_Spider
import re
import time


class DJ_Spider(Base_Spider):

    def __init__(self,website):
        super(DJ_Spider,self).__init__(website)

    def parse(self,url):
        json_str = self.get_content(url,url_type='json')
        metadata = json_str['data']['list']
        data=[]
        for md in metadata:
            item = {}
            try:
                item[u'链接'] = md['liHref']
                item[u'主题'] = md['jobName']
                item[u'公司'] = md['compName']
                item[u'日期'] = md['time']
                item[u'介绍'] = ':'.join([u'月薪',md['salary']])
                item[u'主页'] = md['compHref']
            except KeyError,e:
                print str(e)
            data.append(item)
        return [item for item in data if item]

    def pages_parse(self,keyword):
        for page in xrange(1,15):
            url = 'http://so.dajie.com/job/ajax/search/filter?jobsearch=1&pagereferer=&ajax=1&keyword=%s&page=%d&order=0&from=user&salary=&recruitType=3,4&city=110000&_CSRFToken='%(keyword,page)
            print url
            #print urllib2.urlopen(url).read()
            #data = self.parse(url)
            #yield data




if __name__=="__main__":

    dj = DJ_Spider('dajie')
    #dj.write_title()
    for item in dj.pages_parse('python'):
        print item
    #dj.save()





