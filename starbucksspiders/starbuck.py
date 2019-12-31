# -*- coding:utf-8 -*-

'''
Get the stores' numbers of China cities from starbuk's offical website~
'''

import os
import sys
import csv
import json
import requests


from web_spy import web_spy
from db import my_db


'''
Read city code from csv file
'''
def getCityNameList():
    city_list = []
    city_f = 'data/BaiduMap_cityCode_1102.csv'
    with open(city_f,encoding='utf-8',mode='r') as csvfile:
        reader = csv.reader(csvfile)
        city_list = [row[1] for row in reader]
    return city_list


'''
get cities longitude and latitude
'''
def getLonAndLat(city):
    try:
        base_url = 'https://restapi.amap.com/v3/geocode/geo?address='
        pri_key = ''  #填入自己的api key
        url = base_url + str(city)+'&key='+pri_key
        html = requests.get(url)
        dict_file = html.json()
        city_geo = dict_file['geocodes'][0]['location']
        loc = city_geo.split(',',1)
        print("{} location is {}".format(city,loc))
        return loc             # return longitude and latitude
    except:
        return [ ]

'''
get starbuck stores details
'''

def getDetail(city_list):
    host = 'www.starbucks.com.cn'
    starbucks_spy = web_spy(host)
    starbucks_db = my_db(coll='ChinaStores')
    for city in city_list:
        try:
            lon_lat = getLonAndLat(city)
            if lon_lat == []:
                print("{} get location failed !".format(city))
                continue
            base_url = 'https://www.starbucks.com.cn/api/stores/nearby?lat='
            url_suffix = '&limit=1000&locale=ZH&features=&radius=100000'
            api_url = base_url+str(lon_lat[1]).strip()+'&lon='+str(lon_lat[0]).strip()+url_suffix
            html = starbucks_spy.getHtml(api_url)
            json_data = html.json()         
            stores= json_data['data']
            print("{} have {} stores.".format(city,len(stores)))
            for store in stores:
                try:
                    starbucks_db.saveData(store,db_id='id')
                    print("Store {} saved ~".format(store['id']))
                except:
                    continue
        except:
            print('{} failed !!!! '.format(city))
            continue

def main():
    city_list = getCityNameList()
    getDetail(city_list)
   
if __name__ == "__main__":
    main()
