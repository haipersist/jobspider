#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import redis
import cPickle as P
import time


class PyRedis():

    config={
             'local':{
                    'host':'127.0.0.1',
                    'port':6379,
                    'db':0,
                    'password':'admin'
                    },
             'virtual':{
                    'host':'192.168.6.128',
                    'port':6379,
                    'db':0,
                    'password':'*******'
                    },
            }


    def __init__(self,host):
        self.host = host
        self.__connect()


    def __connect(self):
        self.conn = redis.Connection(host=self.config[self.host]['host'],
                                     port=self.config[self.host]['port'],
                                     db=self.config[self.host]['db'],
                                     password=self.config[self.host]['password'])

        # the rs can excute all operations for different data types
        self.rs = redis.Redis(host=self.config[self.host]['host'],
                              port=self.config[self.host]['port'],
                              db=self.config[self.host]['db'],
                              password=self.config[self.host]['password'])


    # any command used in redis client can be regarded as a string to be executed
    def query(self,cmd):
        self.conn.send_command(cmd)
        return self.conn.read_response()

    def pipe_exec(self,**kargs):
        pipe=self.rs.pipeline()
        for key in kargs:
            if hasattr(self.rs,key):
                apply(getattr(self.rs,key),kargs[key])
        pipe.execute()


    def set(self,name,data):
        #set one hash table which contains several fields
        ''' for tuple or list:
        1.first serialization of data to string,
        2.then store it in string format'''
        if isinstance(data,(basestring,bytes)):
            self.rs.set(name,data)
        elif isinstance(data,list or tuple):
            data=P.dumps(data)
            self.rs.set(name,data)
        elif isinstance(data,dict):
            if self.rs.hmset(name,data):
                print 'store OK'
            else:
                print 'set fail'
        else:
            print 'incorrect data type'
            return None

    def dictget(self,name,select='all'):
        ''' First by cmd "hgetall" get dict,if error occurs,
        that means it is serialized by pickle,need by get'''
        try:
            if select=='all':
                return self.rs.hgetall(name)
            elif isinstance(select,list or tuple):
                return self.rs.hmget(name,select)
        except:
            result=self.rs.get(name)
            if not result:
                return None
            try:
                return P.loads(result)
            except:
                sys.exit()

    def set_hash_field(self,name,key,data):
        #when the data is not string,we need to serilizate it.
        if not isinstance(data,basestring):
            data = P.dumps(data)
        self.rs.hmset(name,{key:data})

    def get_hash_field(self,name,key=None):
        if key is not None:
            result = self.rs.hmget(name,key)
            if len(result) == 1:
                result = result[0]
                try:
                    data = P.loads(result)
                except:
                    data = result
        else:
             data = self.rs.hgetall(name)
        return data







def test(key):

    myredis = PyRedis('local')
    if myredis.rs.llen(key) >=5 and (time.time() - float(myredis.rs.lindex(key,4)))<=3600:
        print 'sorry,but you are forbidden'
        sys.exit(0)
    else:
        myredis.rs.lpush(key,time.time())
        print 'login success'




def hash_redis():
    s=[1,2,5]
    r = PyRedis('local')
    data = [{'title':[1,4],'link':'ssss'}]
    r.set_hash_field('job','51',data)
    result = r.get_hash_field('Job')
    print result





if __name__=="__main__":

    hash_redis()


