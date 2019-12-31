# -*- coding:utf-8 -*-

import csv

from db import mongo_db


def starbucks():
    # 初始化数据库
    starbucks_db = mongo_db(coll='ChinaStores')

    # 将数据写入到CSV文件中
    # 如果直接从 mongodb booster导出, 一旦有部分出现字段缺失，那么会出现结果错位的问题
    # newline='' 的作用是防止结果数据中出现空行，专属于python3
    with open(f"starbucks.csv", "w", newline="", encoding="utf-8") as csvfileWriter:
        writer = csv.writer(csvfileWriter)
        # 先写列名
        # 写第一行，字段名

        header = ["city", "address", "postalCode", "latitude", "longitude", "features", "hasArtwork",
                  "storeName", "storeNumber", "closeTime", "openTime"]

        writer.writerow(header)

        all_record_res = starbucks_db.findAll()

        # 写入多行数据
        i = 0

        for record in all_record_res:
            i = i + 1
            print(f"record = {record}")
            print(i)
            record_value_lst =[]

            address = record['address']
            coordinates = record['coordinates']
            today = record['today']
            print(today)
            record_value_lst.append(address["city"])

            if address['streetAddressLine1'] is not None:
                address_detail = str(address['streetAddressLine1'])
            if address['streetAddressLine2'] is not None:
                address_detail = str(address['streetAddressLine1']) \
                                 + str(address['streetAddressLine2'])
            if address['streetAddressLine3'] is not None:
                address_detail = str(address['streetAddressLine1']) \
                                 + str(address['streetAddressLine2']) \
                                 + str(address['streetAddressLine3'])

            record_value_lst.append(address_detail)
            record_value_lst.append(address['postalCode'])
            record_value_lst.append(coordinates['latitude'])
            record_value_lst.append(coordinates['longitude'])
            record_value_lst.append(record['features'])
            record_value_lst.append(record['hasArtwork'])
            record_value_lst.append(record['name'])
            record_value_lst.append(record['storeNumber'])
            if "{}" != str(today):
                record_value_lst.append(today['closeTime'])
                record_value_lst.append(today['openTime'])
            else:
                record_value_lst.append("")
                record_value_lst.append("")
            try:
                print("write csv file")
                writer.writerow(record_value_lst)

            except Exception as e:
                print(f"write csv exception.e = {e}")


if __name__ == '__main__':
    starbucks()
