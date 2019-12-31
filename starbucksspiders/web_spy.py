# -*- coding:utf-8 -*-

import re
import json
import time
import random
import requests
from user_agents import agents,ip_proxy

'''
网络访问会话设置
'''

class web_spy:                        
    def __init__(self,web_host=""):
        self.sess = self.session(web_host)
    
    def session(self,web_host):               
        session = requests.Session()
        session.headers = {                         # 伪装成浏览器的请求头
            'Host': web_host,
            'User-Agent': random.choice(agents)     # 随机使用 user-agent,防封 ip
        }
        #session.proxies = {'http': 'socks5://127.0.0.1:1080',  # 设置使用 socks5 代理
        #            'https': 'socks5://127.0.0.1:1080'} 
        session.proxies = ip_proxy
        return session
     
    def getHtml(self,url,code='utf-8'):             # 抓取一个 html 页面
        try:
            html = self.sess.get(url,timeout=30)
            html.raise_for_status()
            html.encoding = code
            return html
        except:
            return ''

    def time_url(self,tmp_str):                    # 在请求url后面加上时间戳
        tm = self.time_stamp()
        return tmp_str +'&_='+ str(tm)

    def time_stamp(self):                          # 返回时间戳
        return lambda: int(round(time.time() * 1000)) 

    def getApiData(self,text):                      # 去除无关字符，提取json子串
        try:
            temp_str = re.findall(r'{.*}',text)[0]  
            json_data = json.loads(temp_str)      # 转换为json数据
            return json_data
        except:
            return {}
