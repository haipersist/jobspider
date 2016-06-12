from datetime import date
from baseclass.database import Database
from baseclass.utils.store_data import Job_Data

def get_latest_data():
    today = date.today().strftime("%Y-%m-%d")
    sql = 'select title,website,link,company from jobs'
    where = 'create_day="%s" and website in ("51job","dajie","byr")' % today
    db = Database('Job')
    return db.query_dic(sql,where)






if __name__ == "__main__":
    for job in get_latest_data():
        print job['create_day'],job['company'],job['website']
