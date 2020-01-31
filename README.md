# 2019新型冠状病毒疫情时间序列数据仓库

本项目为2019新型冠状病毒（2019-nCoV）疫情状况的时间序列数据仓库，数据来源为[丁香园](https://3g.dxy.cn/newh5/view/pneumonia)。

近期数位高校师生与我联系，希望用这些数据做科研之用。然而并不熟悉API的使用和JSON数据的处理，因此做了这个数据仓库，直接推送大部分统计软件可以直接打开的csv文件，希望能够减轻各位的负担。

数据由[2019新型冠状病毒疫情实时爬虫](https://github.com/BlankerL/DXY-2019-nCoV-Crawler)获得。

目前代码在测试阶段，因此每小时检测一次更新，若有更新则推送至数据仓库中，未来会根据推送情况调整更新频率。

文件列表：
1. 全国数据[DXYOverall.csv](https://github.com/BlankerL/DXY-2019-nCoV-Data/blob/master/DXYOverall.csv)
2. 地区数据[DXYArea.csv](https://github.com/BlankerL/DXY-2019-nCoV-Data/blob/master/DXYArea.csv)
3. 新闻数据[DXYNews.csv](https://github.com/BlankerL/DXY-2019-nCoV-Data/blob/master/DXYNews.csv)
4. 谣言数据[DXYRumors.csv](https://github.com/BlankerL/DXY-2019-nCoV-Data/blob/master/DXYRumors.csv)

其中：地区数据[DXYArea.csv](https://github.com/BlankerL/DXY-2019-nCoV-Data/blob/master/DXYArea.csv)仅包括丁香园中国地区精确至地级市的数据，港澳台/西藏的数据精确度仅到省级，不包含在此文件中。如有需要可以修改脚本内Listen类的[dumper函数](https://github.com/BlankerL/DXY-2019-nCoV-Data/blob/8e21a7e27604a9d2b1dcf0fa3d0266aa68576753/script.py#L71)，来自定义数据提取的存储方式。

由于本人精力有限，不接受数据定制。如对数据有更多的要求，烦请自行处理。

**祝大家一切都好。**
