# -*- coding: utf-8 -*-
import requests
import json
import os
import datetime
from search import *
import csv

def fetchStreamTopKeywords(date, rival1Id, rival2Id):
    dateRange = date + "|" + date
    refererUrl = "https://sycm.taobao.com/ci/monitor/itemcompare"

    TOP_TYPE_STREAM = 1
    TOP_TYPE_DEAL = 2
    topType = TOP_TYPE_STREAM
    url = "https://sycm.taobao.com/ci/item/compare/topkeywords.json"
    querystring = {"deviceType":2,"topType":topType,"seType":"taobao","dateType":"day","dateRange":dateRange,"needSelf":"false","rival1Id":rival1Id,"rival2Id":rival2Id,"_":1532857215509,"token":"baa876795"}

    # replace cookie
    cookie = '''cna=cna;t=t'''

    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        'accept': "*/*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'Cache-Control': "no-cache",
        'referer': refererUrl,
        'cookie': cookie
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_string = response.text
    result = search_from_dict(json.loads(json_string))

    data = result.data

    rival1 = data.rival1
    rival2 = data.rival2

    return (rival1, rival2)

    # with open(date + '_' + str(rival1Id) + '_stream_key_words.csv', 'w+', newline='') as csvfile:
    #     for rival in rival1:
    #         print(rival.keyword.value + "," + str(rival.uv.value))

    #         writer = csv.writer(csvfile)
    #         writer.writerow([rival.keyword.value , rival.uv.value])

    # # print('\n\n')
    # # writer.writerow([rival.keyword.value , rival.uv.value])

    # with open(date + '_' + str(rival2Id) + '_stream_key_words.csv', 'w+', newline='') as csvfile:
    #     for rival in rival2:
    #         print(rival.keyword.value + "," + str(rival.uv.value))

    #         writer = csv.writer(csvfile)
    #         writer.writerow([rival.keyword.value , rival.uv.value])



def main():
    begin = datetime.date(2018,7,1)
    end = datetime.date.today()
    for i in range((end - begin).days):
        day = begin + datetime.timedelta(days=i)
        # fetchStreamTopKeywords(str(day))

if __name__ == '__main__':
    main()

