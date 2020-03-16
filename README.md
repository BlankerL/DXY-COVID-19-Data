# 2019新型冠状病毒疫情时间序列数据仓库

简体中文 | [English](README.en.md)

本项目为2019新型冠状病毒（COVID-19/2019-nCoV）疫情状况的时间序列数据仓库，数据来源为[丁香园](https://3g.dxy.cn/newh5/view/pneumonia)。

近期数位高校师生与我联系，希望用这些数据做科研之用。然而并不熟悉API的使用和JSON数据的处理，因此做了这个数据仓库，直接推送大部分统计软件可以直接打开的csv文件，希望能够减轻各位的负担。

数据由[2019新型冠状病毒疫情实时爬虫](https://github.com/BlankerL/DXY-COVID-19-Crawler)获得，每小时检测一次更新，若有更新则推送至数据仓库中。

#### CSV文件列表
1. 全国数据[DXYOverall.csv](csv/DXYOverall.csv)
2. 地区数据[DXYArea.csv](csv/DXYArea.csv)（包含英文城市名）
3. 新闻数据[DXYNews.csv](csv/DXYNews.csv)
4. 谣言数据[DXYRumors.csv](csv/DXYRumors.csv)

自[`4db432f`](https://github.com/BlankerL/DXY-COVID-19-Data/commit/4db432fda233a701a3a7569e08ab20db083987b1)开始，DXYArea.csv包含中国境内省市级、港澳台地区及海外数据。另外，也可以参考[这个问题](https://github.com/BlankerL/DXY-COVID-19-Crawler/issues/67)，来定制自己的数据集。

#### JSON文件列表
由于API接口时常不稳定，因此此项目也会定时向`json`文件夹中推送静态的JSON文件更新。JSON文件与API中提供的JSON完全一致。

由于本人精力有限，不接受数据定制。如对数据有更多的要求，烦请自行处理。

## 数据说明
1. 部分数据存在重复统计的情况，如[Issue #21](https://github.com/BlankerL/DXY-COVID-19-Data/issues/21)中所述，河南省部分市级数据存在"南阳（含邓州）"及"邓州"两条数据，因此在求和时"邓州"的数据会被重复计算一次。

### 数据异常
目前发现浙江省/湖北省部分时间序列数据存在数据异常，可能的原因是丁香园数据为人工录入，某些数据可能录入错误，比如某一次爬虫获取的浙江省治愈人数为537人，数分钟后被修改回正常人数。

本项目爬虫仅从丁香园公开的数据中获取并储存数据，并不会对异常值进行判断和处理，因此如果将本数据用作科研目的，请自己对数据进行清洗。同时，我已经在Issue中开放了[异常数据反馈通道](https://github.com/BlankerL/DXY-COVID-19-Crawler/issues/34)，可以直接在此问题中反馈潜在的异常数据，我会定期检查并处理。

## 更多功能

### 扩展插件
1. 如果您希望使用R语言对数据进行分析，可以参考[pzhaonet/ncovr](https://github.com/pzhaonet/ncovr)项目，该项目整合通过GitHub数据仓库/API数据提取两种模式。

### 数据分析
1. [jianxu305/nCov2019_analysis](https://github.com/jianxu305/nCov2019_analysis)  
   功能：参考[此处](https://github.com/jianxu305/nCov2019_analysis/blob/master/src/demo.pdf)。
2. [lyupin/Visualize-DXY-2019-nCov-Data](https://github.com/lyupin/Visualize-DXY-2019-nCov-Data)  
   功能：参考[此处](https://github.com/lyupin/Visualize-DXY-2019-nCov-Data/blob/master/readme.md)。
3. [Avens666/COVID-19-2019-nCoV-Infection-Data-cleaning-](https://github.com/Avens666/COVID-19-2019-nCoV-Infection-Data-cleaning-)  
   功能：参考[此处](https://github.com/Avens666/COVID-19-2019-nCoV-Infection-Data-cleaning-/blob/master/README.md)

**祝大家一切都好。**
