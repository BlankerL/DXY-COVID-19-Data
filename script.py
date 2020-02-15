"""
@ProjectName: DXY-2019-nCoV-Crawler
@FileName: script.py
@Author: Jiabao Lin
@Date: 2020/1/31
"""
from git import Repo
from pymongo import MongoClient
import os
import json
import time
import logging
import datetime
import requests
import pandas as pd


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

uri = '**Confidential**'
client = MongoClient(uri)
db = client['2019-nCoV']

collections = {
    'DXYOverall': 'overall',
    'DXYArea': 'area',
    'DXYNews': 'news',
    'DXYRumors': 'rumors'
}
time_types = ('pubDate', 'createTime', 'modifyTime', 'dataInfoTime', 'crawlTime', 'updateTime')


def git_manager(changed_files):
    repo = Repo(path=os.path.split(os.path.realpath(__file__))[0])
    repo.index.add(changed_files)
    repo.index.commit(message='{datetime} - Change detected!'.format(datetime=datetime.datetime.now()))
    origin = repo.remote('origin')
    origin.push()
    logger.info('Pushing to GitHub successfully!')


class DB:
    def __init__(self):
        self.db = db

    def count(self, collection):
        return self.db[collection].count_documents(filter={})

    def dump(self, collection):
        return self.db[collection].aggregate(
            pipeline=[
                {
                    '$sort': {
                        'updateTime': -1,
                        'crawlTime': -1
                    }
                }
            ]
        )


class Listener:
    def __init__(self):
        self.db = DB()

    def run(self):
        while True:
            self.listener()
            time.sleep(3600)

    def listener(self):
        changed_files = list()
        for collection in collections:
            json_file = open(
                os.path.join(
                    os.path.split(os.path.realpath(__file__))[0], 'json', collection + '.json'),
                'r', encoding='utf-8'
            )
            static_data = json.load(json_file)
            json_file.close()
            while True:
                request = requests.get(url='https://lab.isaaclin.cn/nCoV/api/' + collections.get(collection))
                if request.status_code == 200:
                    current_data = request.json()
                    break
                else:
                    continue
            if static_data != current_data:
                self.json_dumper(collection=collection, content=current_data)
                changed_files.append('json/' + collection + '.json')
                self.csv_dumper(collection=collection)
                changed_files.append('csv/' + collection + '.csv')
                logger.info('{collection} updated!'.format(collection=collection))
        if changed_files:
            git_manager(changed_files=changed_files)

    def json_dumper(self, collection, content):
        json_file = open(
            os.path.join(
                os.path.split(os.path.realpath(__file__))[0], 'json', collection + '.json'),
            'w', encoding='utf-8'
        )
        json.dump(content, json_file, ensure_ascii=False, indent=4)
        json_file.close()

    def csv_dumper(self, collection):
        if collection == 'DXYArea':
            structured_results = list()
            results = self.db.dump(collection=collection)
            for province_dict in results:
                if province_dict.get('cities', None):
                    for city_counter in range(len(province_dict['cities'])):
                        city_dict = province_dict['cities'][city_counter]
                        result = dict()
                        result['provinceName'] = province_dict['provinceName']
                        result['provinceEnglishName'] = province_dict['provinceEnglishName']
                        result['cityName'] = city_dict['cityName']
                        result['cityEnglishName'] = city_dict['cityEnglishName']

                        result['province_confirmedCount'] = province_dict['confirmedCount']
                        result['province_suspectedCount'] = province_dict['suspectedCount']
                        result['province_curedCount'] = province_dict['curedCount']
                        result['province_deadCount'] = province_dict['deadCount']

                        result['city_confirmedCount'] = city_dict['confirmedCount']
                        result['city_suspectedCount'] = city_dict['suspectedCount']
                        result['city_curedCount'] = city_dict['curedCount']
                        result['city_deadCount'] = city_dict['deadCount']

                        result['updateTime'] = datetime.datetime.fromtimestamp(province_dict['updateTime']/1000)

                        structured_results.append(result)
            df = pd.DataFrame(structured_results)
            df.to_csv(
                path_or_buf=os.path.join(
                    os.path.split(os.path.realpath(__file__))[0], 'csv', collection + '.csv'),
                index=False, encoding='utf_8_sig'
            )
        else:
            df = pd.DataFrame(data=self.db.dump(collection=collection))
            for time_type in time_types:
                if time_type in df.columns:
                    df[time_type] = df[time_type].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000) if not pd.isna(x) else '')
            df.to_csv(
                path_or_buf=os.path.join(
                    os.path.split(os.path.realpath(__file__))[0], 'csv', collection + '.csv'),
                index=False, encoding='utf_8_sig'
            )


if __name__ == '__main__':
    listener = Listener()
    listener.run()
