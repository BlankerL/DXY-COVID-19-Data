# COVID-19/2019-nCoV Time Series Infection Data Warehouse

[简体中文](README.md) | English

COVID-19/2019-nCoV time series infection data warehouse, the data source is [Ding Xiang Yuan](https://3g.dxy.cn/newh5/view/pneumonia).

**Researchers**  
Recently, many college teachers and students contacted me, 
hoping to use these data for scientific research. 
However, not everyone is familiar with the use of APIs and the format of JSON, 
so here is the [data warehouse](https://github.com/BlankerL/DXY-COVID-19-Data) 
to publish the latest data in CSV format, 
which can be easily processed and loaded by most software.

The data is obtained by [COVID-19 Infection Data Realtime Crawler](https://github.com/BlankerL/DXY-COVID-19-Crawler). 

At 0:00 every day, the program will execute on time and the data will be pushed into
[Release](https://github.com/BlankerL/DXY-COVID-19-Data/releases/latest).

**Due to the limitation of the server's bandwidth, starting from March 19, 2020, 
`/nCoV/api/overall` and `/nCoV/api/area` do not response time-series data.
You can fetch time-series data in [json](json) folder.
If you call the API with `latest=0`, please modify the request parameters, 
otherwise, you do not need to do any modification.**

Data customization is not accepted. 
If you have more requirements for data, please handle it on your own.

## Data Description
1. As mentioned in [Issue #21](https://github.com/BlankerL/DXY-COVID-19-Data/issues/21), 
Some data are duplicated. For example, in Henan Province, 
there is a city-level document recording Nanyang (Dengzhou inclusive) and Dengzhou.
Therefore, the data of "Dengzhou" will be double-counted once during the summation.

### Noise Data
1. At present, some time series data in Zhejiang and Hubei are found containing noises. 
The possible reason is the manually processed data were recorded by mistake.
2. [Issue #110](https://github.com/BlankerL/DXY-COVID-19-Data/issues/110) 
reported the reversal of the number of confirmed cases in Changchun and Jilin City in Jilin Province, 
updated on March 15 by Dingxiang Yuan. To ensure data integrity, 
I have not modified the data, so please adjust it manually when you use it if considered necessary. 

The crawler just crawl what it sees, do not deal with any noise data. 
Therefore, if you use the data for scientific research, please preprocess and clean the data properly. 

In the meantime, I opened an [issue](https://github.com/BlankerL/DXY-COVID-19-Crawler/issues/34) 
for you to report the potential noise data. I will check and remove them periodically. 

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
3. [Avens666/COVID-19-2019-nCoV-Infection-Data-cleaning-](https://github.com/Avens666/COVID-19-2019-nCoV-Infection-Data-cleaning-)  
   Features: See [here](https://github.com/Avens666/COVID-19-2019-nCoV-Infection-Data-cleaning-/blob/master/README.md)

**Wish you all the best.**
