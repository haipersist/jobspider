#!usr/bin/python
#encoding:utf8

from datetime import date
from baseclass.database import Database
from baseclass.utils.store_data import Job_Data



def get_renderg_data():
    today = date.today().strftime("%Y-%m-%d")            
    today = '2016-03-02'
    sql = 'select title,website,link,company from jobs'        
    where = 'create_day="%s" and (company LIKE "%润德骥图%" OR company LIKE "%re%")' % today
    db = Database('Job')
    return db.query_dic(sql,where)


class GoodJob():

    def __init__(self,day=None):
        if day is None:
            self.day = date.today().strftime("%Y-%m-%d")
        else:
            self.day = day
        self.sql = 'select title,link,company from jobs'
        self.base_where = 'create_day="%s"' % self.day
        self.db = Database('Job')
    

    def create_where(self,*awargs):
        companies = []
        for awarg in awargs:
            companies.append('company like "%s"'%awarg)
        return self.base_where +' and ('+ ' or '.join(companies) + ')'

    def get_renderg(self):
        awarg1,awarg2 = "%re%" ,"%润德骥图%"
        where = self.create_where(awarg1,awarg2)
        return self.db.query_dic(self.sql,where)
    
    def get_huaxia(self):
        awarg1 = "华夏基石"
        where = self.create_where(awarg1)
        return self.db.query_dic(self.sql,where)
   

if __name__ == "__main__":
    job = GoodJob('2016-06-07')
    d =[]
    r = job.get_renderg()
    y = job.get_huaxia()
    d.extend(r)
    print d


