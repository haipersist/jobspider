Author:Haibo wang.
Date:2016-03-23

you can visit me in my website:http://hbnnlove.sinaapp.com.




This spider is used to crawl job information from several famous websites.such as zhilian,job51,dajie,lagou and byr etc.
this module is very simple to use.for excample:



<pre><code>

from jobspider.spider import producer

 if __name__ == "__main__":

    #producer(store_type='MySQL')
    # run single spider
    spider = Spider('python')
	spider.single_run("lagou")

</code></pre>

 By default,after the programm ends,the data has been stored in json file. of course,you can store data to other files or databases,
 but you must has created corresponding table.you can add code in baseclass.utils.store_data py file.

 If you wanna to store data to MySQL.you should add user into MySQL.user whose username is admin,password:admin
 of course ,you should create table by yourself,the field includes:int id,title varchar,company varchar,linke varchar,
 salary,create_day,date.
 




 In addition,you can write yourself spider like this:

<pre><code>
 from jobspider.baseclass.base_spider import Base_Spider

 class DJ_Spider(Base_Spider):

    def __init__(self,website,*args):
        super(DJ_Spider,self).__init__(website,args)

    def parse(self,url):
        pass

    def pages_parse(self,keyword):
        for page in xrange(1,2):
            url = ''
            self.parse(url)


 if __name__=="__main__":
    dj = DJ_Spider('dajie','X-Requested-With','Host','Referer','Cookie')
    for item in dj.pages_parse('python'):
        print item

</code></pre>

 you should write the information of headers like X-http-request,cookie,host,referer into config/webinfo.cfg.

 as long as you can write code like that above,you can get data normally.


 At last, you can query result in my website:http://hbnnlove.sinaapp.com.

