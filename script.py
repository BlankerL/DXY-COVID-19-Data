"""
@ProjectName: DXY-2019-nCoV-Crawler
@FileName: script.py
@Author: Jiabao Lin
@Date: 2020/1/31
"""
from git import Repo
from pymongo import MongoClient
import os
import time
import datetime
import pandas as pd


uri = '**Confidential**'
client = MongoClient(uri)
db = client['2019-nCoV']

collections = ['DXYOverall', 'DXYArea', 'DXYNews', 'DXYRumors']


def git_manager(changed_files):
    repo = Repo(path=os.path.split(os.path.realpath(__file__))[0])
    repo.index.add(changed_files)
    repo.index.commit(message='{datetime} - Change detected!'.format(datetime=datetime.datetime.now()))
    origin = repo.remote('origin')
    origin.push()


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
        self.counter = dict()

    def run(self):
        while True:
            self.listener()
            time.sleep(60)

    def listener(self):
        changed_files = list()
        for collection in collections:
            if not self.counter.get(collection, None):
                self.counter[collection] = self.db.count(collection=collection)
            else:
                if self.counter[collection] != self.db.count(collection=collection):
                    self.dumper(collection=collection)
                    changed_files.append(collection + '.csv')
                    self.counter[collection] = self.db.count(collection=collection)
        if changed_files:
            git_manager(changed_files=changed_files)

    def dumper(self, collection):
        if collection == 'DXYArea':
            structured_results = list()
            results = self.db.dump(collection=collection)
            for province_dict in results:
                if province_dict.get('cities', None):
                    for city_counter in range(len(province_dict['cities'])):
                        city_dict = province_dict['cities'][city_counter]
                        result = dict()
                        result['provinceName'] = province_dict['provinceName']
                        result['cityName'] = city_dict['cityName']

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
                    os.path.split(os.path.realpath(__file__))[0], collection + '.csv'),
                index=False, encoding='utf_8_sig'
            )
        else:
            df = pd.DataFrame(data=self.db.dump(collection=collection))
            df.to_csv(
                path_or_buf=os.path.join(
                    os.path.split(os.path.realpath(__file__))[0], collection + '.csv'),
                index=False, encoding='utf_8_sig'
            )


if __name__ == '__main__':
    listener = Listener()
    listener.run()
