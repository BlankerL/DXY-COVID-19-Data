# 2019-nCoV Time Series Infection Data Warehouse

[简体中文](README.md) | English

2019-nCoV time series infection data warehouse, the data source is [Ding Xiang Yuan](https://3g.dxy.cn/newh5/view/pneumonia).

**Researchers**  
Recently, many college teachers and students contacted me, 
hoping to use these data for scientific research. 
However, not everyone is familiar with the use of APIs and the format of JSON, 
so here is the [data warehouse](https://github.com/BlankerL/DXY-2019-nCoV-Data) 
to publish the latest data in CSV format, 
which can be easily processed and loaded by most software.

The data is obtained by [2019-nCoV Infection Data Realtime Crawler](https://github.com/BlankerL/DXY-2019-nCoV-Crawler).

The project is under beta test, so the data will be published in every hours. 
The frequency will be adjusted in the future. 

CSV File List：
1. Overall Data [DXYOverall.csv](csv/DXYOverall.csv)
2. Regional Data [DXYArea.csv](csv/DXYArea.csv)
3. News [DXYNews.csv](csv/DXYNews.csv)
4. Rumors [DXYRumors.csv](csv/DXYRumors.csv)

Regional data ([DXYArea.csv](csv/DXYArea.csv))
only contains all the city-level data. 
Data from Hong Kong SAR, Macao SAR, Tai Wan and Tibet are province-level, 
and not city-level data available from DXY, so they are not in this file. 

If needed, you can modify the [dumper function](https://github.com/BlankerL/DXY-2019-nCoV-Data/blob/8e21a7e27604a9d2b1dcf0fa3d0266aa68576753/script.py#L71)
to customize your own files. 

JSON File List:
Due to the instability of API,
this project will also push latest static JSONs into the `json` folder. 
Data from JSON files are exactly the same as the data responded from the API.


Data customization is not accepted. 
If you have more requirements for data, please handle it on your own.


## Reference

### Packages
1. If you would like to analyze the data with [R](https://www.r-project.org/),
you can refer to [pzhaonet/ncovr](https://github.com/pzhaonet/ncovr).
This project will help you to directly load data into R from either GitHub Data Warehouse or API. 

### Analysis
1. [jianxu305/nCov2019_analysis](https://github.com/jianxu305/nCov2019_analysis)  
   Features: See [here](https://github.com/jianxu305/nCov2019_analysis/blob/master/src/demo.pdf).
2. [lyupin/Visualize-DXY-2019-nCov-Data](https://github.com/lyupin/Visualize-DXY-2019-nCov-Data)  
   Features: See [here](https://github.com/lyupin/Visualize-DXY-2019-nCov-Data/blob/master/readme.md).

## Noise Data
At present, some time series data in Zhejiang and Hubei are found containing noises. 
The possible reason is the manually processed data were recorded by mistake. 

The crawler just crawl what it sees, do not deal with any noise data. 
Therefore, if you use the data for scientific research, please preprocess and clean the data properly. 

In the meantime, I opened an [issue](https://github.com/BlankerL/DXY-2019-nCoV-Crawler/issues/34) 
for you to report the potential noise data. I will check and remove them periodically. 

**Wish you all the best.**
