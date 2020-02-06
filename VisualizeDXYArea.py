import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import timedelta, date

# 对普通使用者而言，只作如下一处修改，使用 python 运行本文件，即可生成“累计确诊数”和“单日新增确诊数”的趋势图。
# 将希望绘制趋势图的城市名添加到下一行中
cityNames = ['武汉', '黄冈', '孝感']

fn_DXYArea = './csv/DXYArea.csv'

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 'Arial'

mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['legend.fontsize'] = 12
mpl.rcParams['axes.labelsize'] = 12

mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'

def select_record_until_certain_time_in_one_day(times_in, hour_target, minute_target):
    deltas = [[egg[0], timedelta(hours = hour_target - egg[1], minutes = minute_target - egg[2]).seconds] for egg in times_in]
    deltas = np.array(deltas)

    i2_min_tmp = -1
    delta_min = 99999999
    for i2 in range(deltas.shape[0]):
        delta_tmp = deltas[i2, :]
        if delta_tmp[1] > 0 and delta_tmp[1] < delta_min:
            i2_min_tmp = i2
            delta_min = delta_tmp[1]
    
    return deltas[i2_min_tmp, 0]

def select_record_until_certain_time_on_each_day(dat_in, hour_target = 12, minute_target = 0, key = 'updateTime'):
    indices_tmp = []
    
    datetime_old = pd.to_datetime(dat_in.iat[0, 4])
    day_old = datetime_old.day
    
    hour_old = datetime_old.hour
    minute_old = datetime_old.minute
    times_in_day = [[0, hour_old, minute_old]]
    
    #print([day_old, hour_old, minute_old])    
    
    for i in range(1, dat_in.shape[0]):
        datetime_tmp = pd.to_datetime(dat_in.iat[i, 4])
        #print(datetime_tmp)
        
        day_tmp, hour_tmp, minute_tmp = datetime_tmp.day, datetime_tmp.hour, datetime_tmp.minute
        
        if day_tmp == day_old:
            #print('Append')
            times_in_day.append([i, hour_tmp, minute_tmp])        
        else:
            #print('Select')
            index_tmp = select_record_until_certain_time_in_one_day(times_in_day, hour_target, minute_target)            
            indices_tmp.append(index_tmp)
            
            day_old = day_tmp
            times_in_day = [[i, hour_tmp, minute_tmp]]
            
    #print('Finalize')
    index_tmp = select_record_until_certain_time_in_one_day(times_in_day, hour_target, minute_target)            
    indices_tmp.append(index_tmp)
    
    return dat_in.iloc[indices_tmp, :]

def extract_by_city(df_in, cityName, calc_increment = True, show = True):
    df_1 = df_in[df_in['cityName'] == cityName]

    df_2 = df_1.iloc[::-1, 6:11]
    #print(df_2)

    df_3 = select_record_until_certain_time_on_each_day(df_2)
    #print(df_3)

    datetimes = pd.to_datetime(df_3.loc[:, 'updateTime'])

    dates = [row[1].date() for row in datetimes.items()]

    df_4 = df_3.iloc[:,[0,2,3,4]]

    df_5 = df_4.rename(columns={'updateTime': 'updateDate'})
    df_5.loc[:, 'updateDate'] = dates
    
    if calc_increment:
        df_5['confirmedIncrement'] = df_5['city_confirmedCount']
        df_5.iloc[0, 4] = 0
        if df_5.shape[0] > 1:
            for i_row in range(1, df_5.shape[0]):
                df_5.iloc[i_row, 4] = df_5.iloc[i_row, 0] - df_5.iloc[i_row - 1, 0]
                
    if show:
        print(df_5)
    
    return df_5

def plot_datasets(dat_in, show = False, savefig = True):
    nDat = len(dat_in)
    
    # matplotlib date format object
    hfmt = mpl.dates.DateFormatter('%m/%d')

    fig, ax = plt.subplots()
    for i in range(nDat):
        df_tmp = dat_in[i]
        ax.plot(df_tmp['updateDate'], df_tmp['city_confirmedCount'], '.-', label = cityNames[i])

    ax.xaxis.set_major_formatter(hfmt)
    plt.legend()
    #plt.xlabel('日期')
    plt.ylabel('累计确诊数')
    ylims = ax.get_ylim()
    ax.set_ylim([0, ylims[1]])
    if savefig:
        plt.savefig('累计确诊数.png', dpi = 300)
    if show:
        plt.show()
    plt.close()

    fig, ax = plt.subplots()
    for i in range(nDat):
        df_tmp = dat_in[i]
        ax.plot(df_tmp['updateDate'], df_tmp['confirmedIncrement'], '.-', label = cityNames[i])

    ax.xaxis.set_major_formatter(hfmt)
    plt.legend()
    plt.ylabel('单日新增确诊数')
    ylims = ax.get_ylim()
    ax.set_ylim([0, ylims[1]])
    if savefig:
        plt.savefig('单日新增确诊数.png', dpi = 300)
    if show:
        plt.show()
    plt.close()
    
    if savefig:
        print('已保存趋势图至本目录：\n1.累计确诊数.png\n2.单日新增确诊数.png')

    return

df_orig = pd.read_csv(fn_DXYArea)

nCity = len(cityNames)

datasets = []
for i in range(nCity):
    df_tmp = extract_by_city(df_orig, cityNames[i], show = False)
    datasets.append(df_tmp)

plot_datasets(datasets)