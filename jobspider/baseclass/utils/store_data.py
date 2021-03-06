#!/usr/bin/env python
# -*- coding:utf-8 -*-



"""
store_data.py

the data needed sotred is in format:[{},{},{}],we can store them in Mysql ,json or Redis

"""

#from baseclass.database import Database
import json
import os
from datetime import datetime,date
from  ..database import Database
from ..myredis import PyRedis



class Job_Data():

    def __init__(self,store_type='json'):
        self.store_type = store_type
        self.today = date.today().strftime("%Y-%m-%d")


    def store(self,data):
        if self.store_type == 'MySQL':
            self.store_to_mysql(data)
        elif self.store_type == 'json':
            self.store_to_json(data)
        elif self.store_type == 'excel':
            self.store_to_excel(data)
        elif self.store_type == 'redis':
            self.store_to_redis(data)

    def store_to_mysql(self,data):
        self.db = Database('Job')
        for item in data:
            item['create_day'] = self.today
        self.db.insert_dic_by_list('jobs',data)

    def store_to_json(self,data,filename='-'.join([date.today().strftime("%Y-%m-%d"),'job.json'])):
        basepath = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
        if os.name == 'nt':
            filepath = os.path.join(basepath,'%s'%filename)
            print 'json file is stored in %s' % filepath
        else:
            filepath = os.path.join('/tmp',filename)
            print 'json file is stored in %s ' % filepath
        for item in data:
            #print item['title'],item['link']
            json_data = json.dumps(item)
            with file(filepath,'a+') as json_file:
                json_file.write(json_data)
                json_file.write('\n')

    def store_to_excel(self,data,filename='job.xlsx'):
        pass

    def store_to_redis(self,data):
        r = PyRedis('local')
        keys=['51job','dajie','zhilian','byr','lagou']
        for key in keys:
            data_to_store = [item for item in data if item['website']==key]
            if data_to_store:
                r.set_hash_field('Job',key,data_to_store)

        

    

