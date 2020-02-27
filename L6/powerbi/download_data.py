# -*- coding: utf-8 -*-
# @File  : download_data.py
# @Author: LVFANGFANG
# @Date  : 2020/2/26 8:24 下午
# @Desc  :

import time
import json
import requests
import pandas as pd


def get_html_text(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'lab.isaaclin.cn',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return 'Error'


# 将timestamp转换为日期类型
def timestamp_to_date(timestamp, format_string="%Y-%m-%d"):
    time_array = time.localtime(timestamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


def process_data(data):
    success = data['success']
    if success:
        result_data = []
        results = data['results']
        for result in results:
            provinceName = result['provinceName']
            # currentConfirmedCount = result['currentConfirmedCount']
            confirmedCount = result['confirmedCount']
            suspectedCount = result['suspectedCount']
            curedCount = result['curedCount']
            deadCount = result['deadCount']
            countryName = result['countryName']
            continentName = result.get('continentName')
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result['updateTime'] / 1000))
            if 'cities' in result and result['cities']:
                for city in result['cities']:
                    cityName = city['cityName']
                    confirmedCount = city['confirmedCount']
                    suspectedCount = city['suspectedCount']
                    curedCount = city['curedCount']
                    deadCount = city['deadCount']
                    temp_dict = {'province': provinceName, 'city': cityName, 'updateTime': updateTime,
                                 'confirmedCount': confirmedCount, 'suspectedCount': suspectedCount,
                                 'curedCount': curedCount, 'deadCount': deadCount, 'country': countryName,
                                 'continent': continentName}
                    result_data.append(temp_dict)
            else:
                temp_dict = {'province': provinceName, 'updateTime': updateTime,
                             'confirmedCount': confirmedCount, 'suspectedCount': suspectedCount,
                             'curedCount': curedCount, 'deadCount': deadCount, 'country': countryName,
                             'continent': continentName}

                result_data.append(temp_dict)

        df = pd.DataFrame(result_data)
        df['updateTime'] = pd.to_datetime(df['updateTime'])
        df.sort_values(by=['updateTime'], ascending=False, inplace=True)
        df['updateTime'] = df['updateTime'].dt.date
        df.drop_duplicates(subset=['province', 'city', 'updateTime', 'country', 'continent'], keep='first',
                           inplace=True)
        return df
    else:
        print('data error')

def auto_commit():
    pass


def main():
    url = 'https://lab.isaaclin.cn/nCoV/api/area?latest=0&province='
    file = 'ncov.csv'
    json_data = get_html_text(url)
    df = process_data(json_data)
    df.to_csv(file,index=None)
    auto_commit()



if __name__ == '__main__':
    main()
