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

    def store_to_mysql(self,dbname,table,data):
        self.db = Database(dbname)
        self.table = table
        self.db.insert_dic_by_list(table,data)

    def store_to_json(self,data,filename='job.json'):
        json_data = json.dumps(data)
        with file('job.json','a+') as json_file:
            json_file.write(json_data)

    def write_to_excel(self,data,filename='job.xlsx'):
        pass

    def write_to_redis(self,data,keyname='job'):
        pass

    

