# -*- coding:utf-8 -*-

import pymongo
import configparser 
import string, os, sys

class my_db:
    def __init__(self,coll='test'):
        self.getConf()
        client = pymongo.MongoClient(self.db_host ,self.db_port)
        self.db = client[self.db_name]
        self.db.authenticate(self.db_user, self.db_passwd)
        self.db_coll = self.db[coll]

    def getConf(self):
        cf = configparser.ConfigParser()
        cf.read(os.getcwd()+'/db.conf')
        self.db_host = cf.get("mongodb", "HOST") 
        self.db_port = cf.getint("mongodb", "PORT")
        self.db_name = cf.get('mongodb',"DB")
        self.db_user = cf.get("mongodb", "USER") 
        self.db_passwd = cf.get("mongodb", "PASSWD") 

    def saveData(self,data,db_id='uid'):        # 传入需要保存的数据和检查重复的字段
        self.db_coll.update({db_id:data[db_id]},{'$set':data},True)
    