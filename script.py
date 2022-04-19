"""
@ProjectName: DXY-2019-nCoV-Crawler
@FileName: script.py
@Author: Jiabao Lin
@Date: 2020/1/31
"""
from github3 import login, session
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import json
import time
import logging
import datetime
import pandas as pd


# Load environment parameters
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Database connection
client = MongoClient(os.getenv('MONGO_URI'))
db = client['2019-nCoV']

collections = {
    'DXYOverall': 'overall',
    'DXYArea': 'area',
    'DXYNews': 'news',
    'DXYRumors': 'rumors'
}

files = (
    'csv/DXYOverall.csv', 'csv/DXYArea.csv', 'csv/DXYNews.csv', 'csv/DXYRumors.csv',
    'json/DXYOverall.json', 'json/DXYArea.json', 'json/DXYNews.json', 'json/DXYRumors.json'
)

time_types = ('pubDate', 'createTime', 'modifyTime', 'dataInfoTime', 'crawlTime', 'updateTime')


class DB:
    def __init__(self):
        self.db = db

    def count(self, collection: str):
        return self.db[collection].count_documents(filter={})

    def dump(self, collection: str):
        return self.db[collection].aggregate(
            pipeline=[
                {
                    '$sort': {
                        'updateTime': -1,
                        'crawlTime': -1
                    }
                }
            ],
            allowDiskUse=True
        )


class Listener:
    def __init__(self):
        self.db = DB()

    def run(self):
        while True:
            self.updater()
            time.sleep(
                (
                    # Update every 24 hours
                    datetime.timedelta(hours=24) - (datetime.datetime.now() - datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
                ).total_seconds()
            )

    @staticmethod
    def github_manager():
        # GitHub connection
        github = login(token=os.getenv('GITHUB_TOKEN'))
        github.session = session.GitHubSession(default_read_timeout=10, default_connect_timeout=10)
        repository = github.repository(owner='BlankerL', repository='DXY-COVID-19-Data')
        release = repository.create_release(
            tag_name='{tag_name}'.format(
                tag_name=datetime.datetime.today().strftime('%Y.%m.%d')
            )
        )
        for file in files:
            logger.info('Uploading: ' + file.split('/')[-1])
            release.upload_asset(
                content_type='application/text',
                name=file.split('/')[-1],
                asset=open(
                    file=os.path.join(
                        os.path.split(os.path.realpath(__file__))[0], file
                    ),
                    mode='rb'
                )
            )

    def updater(self):
        for collection in collections:
            cursor = self.db.dump(collection=collection)
            self.csv_dumper(collection=collection, cursor=cursor)
            logger.info(collection + '.csv dumped!')

            cursor = self.db.dump(collection=collection)
            self.db_dumper(collection=collection, cursor=cursor)
            logger.info(collection + '.json dumped!')

        self.github_manager()

    def csv_dumper(self, collection: str, cursor):
        if collection == 'DXYArea':
            structured_results = list()
            for document in cursor:
                if document.get('cities', None):
                    for city_counter in range(len(document['cities'])):
                        city_dict = document['cities'][city_counter]
                        structured_results.append(self.dict_parser(document=document, city_dict=city_dict))
                else:
                    structured_results.append(self.dict_parser(document=document))

            df = pd.DataFrame(structured_results)
            df.to_csv(
                path_or_buf=os.path.join(
                    os.path.split(os.path.realpath(__file__))[0], 'csv', collection + '.csv'),
                index=False, encoding='utf_8_sig', float_format="%i"
            )
        elif collection == 'DXYOverall':
            df = pd.DataFrame(data=cursor)
            for time_type in time_types:
                if time_type in df.columns:
                    df[time_type] = df[time_type].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000) if not pd.isna(x) else '')
            del df['_id']
            del df['infectSource']
            del df['passWay']
            del df['virus']
            df.to_csv(
                path_or_buf=os.path.join(
                    os.path.split(os.path.realpath(__file__))[0], 'csv', collection + '.csv'),
                index=False, encoding='utf_8_sig', date_format="%Y-%m-%d %H:%M:%S"
            )
        else:
            df = pd.DataFrame(data=cursor)
            for time_type in time_types:
                if time_type in df.columns:
                    df[time_type] = df[time_type].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000) if not pd.isna(x) else '')
            df.to_csv(
                path_or_buf=os.path.join(
                    os.path.split(os.path.realpath(__file__))[0], 'csv', collection + '.csv'),
                index=False, encoding='utf_8_sig', date_format="%Y-%m-%d %H:%M:%S"
            )

    @staticmethod
    def db_dumper(collection: str, cursor):
        data = list()
        if collection != 'DXYArea':
            for document in cursor:
                document.pop('_id')
                if document.get('comment'):
                    document.pop('comment')
                data.append(document)
        else:
            for document in cursor:
                document.pop('_id')
                document.pop('statisticsData', None)
                document.pop('showRank', None)
                document.pop('operator', None)
                data.append(document)

        json_file = open(
            os.path.join(
                os.path.split(
                    os.path.realpath(__file__))[0], 'json', collection + '.json'
            ),
            'w', encoding='utf-8'
        )
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        json_file.close()

    @staticmethod
    def dict_parser(document: dict, city_dict: dict = None) -> dict:
        result = dict()

        try:
            result['continentName'] = document['continentName']
            result['continentEnglishName'] = document['continentEnglishName']
        except KeyError:
            result['continentName'] = None
            result['continentEnglishName'] = None

        result['countryName'] = document['countryName']

        try:
            result['countryEnglishName'] = document['countryEnglishName']
        except KeyError:
            result['countryEnglishName'] = None

        result['provinceName'] = document['provinceName']
        result['provinceEnglishName'] = document.get('provinceEnglishName')
        result['province_zipCode'] = document.get('locationId')
        result['province_confirmedCount'] = document['confirmedCount']
        result['province_suspectedCount'] = document['suspectedCount']
        result['province_curedCount'] = document['curedCount']
        result['province_deadCount'] = document['deadCount']

        if city_dict:
            result['cityName'] = city_dict['cityName']
            result['cityEnglishName'] = city_dict.get('cityEnglishName')
            result['city_zipCode'] = city_dict.get('locationId')
            result['city_confirmedCount'] = city_dict['confirmedCount']
            result['city_suspectedCount'] = city_dict['suspectedCount']
            result['city_curedCount'] = city_dict['curedCount']
            result['city_deadCount'] = city_dict['deadCount']

        result['updateTime'] = datetime.datetime.fromtimestamp(int(document['updateTime']/1000))

        return result


if __name__ == '__main__':
    listener = Listener()
    listener.run()
