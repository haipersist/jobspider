#!/usr/bin/env python
# -*- coding:utf-8 -*-



"""
store_data.py

the data needed sotred is in format:[{},{},{}],we can store them in Mysql ,json or Redis

"""

from baseclass.database import Database
import json



class Job_Data():

    def __init__(self,store_type='Mysql'):
        self.store_type = store_type

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
        self.db.insert_dic_by_list('jobs',data)

    def store_to_json(self,data,filename='job.json'):
        json_data = json.dumps(data)
        with file('job.json','a+') as json_file:
            json_file.write(json_data)

    def store_to_excel(self,data,filename='job.xlsx'):
        pass

    def store_to_redis(self,data,keyname='job'):
        pass

    

