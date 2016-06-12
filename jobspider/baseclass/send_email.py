#!/usr/bin/env python
#encoding:utf8
'''
Author: whb
e-mail:hbnnlong@163.com
Date:2016-04-21
'''

import email
import time
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
import smtplib
import os
import sys
import ConfigParser
import ast
import commands


class SendMail():

    def __init__(self,mail_type):
        self.mail_type = mail_type
        self._send_server = os.environ.get('MAIL_SERVER')
        print self._send_server
        Jobspider = commands.getoutput('echo $Jobspider')
        self._cfg_path = '/'.join([Jobspider,'config/send_email.cfg'])
        self._smtp = smtplib.SMTP(self._send_server)
        self.set_config()
        self.user = os.environ.get('MAIL_SENDER')
        self.passwd = os.environ.get('MAIL_PASSWORD')
        print self.user,self.passwd

    def set_config(self):
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(self._cfg_path)
        self.to_addrs =ast.literal_eval(self.cfg.get(self.mail_type,'addrs'))
        self.subject = self.cfg.get(self.mail_type,'subject')
        #self.txt = self.cfg.get(self.mail_type,'txt')

    def send_email(self,filename=None,msghtml=None,msgtxt=None):
        ms = MIMEMultipart()
        Addrs = [email.utils.formataddr((False,addr)) for addr in self.to_addrs]
        ms['To'] = ','.join(Addrs)
        ms['From'] = self.user
        ms['Subject'] = self.subject
        ms['Date'] = email.utils.formatdate(time.time(),True)
        #ms.attach(MIMEText(self.txt))
        if msghtml:
            ms.attach(MIMEText(msghtml,'html','utf8'))
   
        if filename:
            attat = MIMEText(file(filename,'rb').read(),'base64','utf8')
            attat["Content-Type"]='application/octet-stream'
            attat['Content-Disposition']='attatcnment;filename="%s" '%filename
            ms.attach(attat)
        
        if msgtxt:
            ms.attach(MIMEText(msgtxt,'plain','utf8'))    
        self._smtp.login(self.user,self.passwd)
        try:
            self._smtp.sendmail(self.user,Addrs,ms.as_string())
            self._smtp.quit()
            return
        except Exception,e:
            print str(e)


def test():
    S_mail = SendMail('Job')
    S_mail.send_email(msghtml='test')



if __name__=="__main__":

    test()

