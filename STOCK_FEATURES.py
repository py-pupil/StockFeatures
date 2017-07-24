# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 22:05:39 2017

@author: WANG
"""
import tushare as ts
import matplotlib.pylab as plt
import pandas as pd
pd.set_option('display.precision',2)
import numpy as np
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import time
import datetime as dt

def STOCK_FEATURES(Universe,factor = None, *parameters,path_or_net=True,start, 
                   end,norm=False,parameter,standardize=False):
    for code in Universe:
        if 'ILLIQ' in factor:
            return GET_ILLIQ(code,path_or_net,start,end,standardize,parameter)
        if 'PROFIT' in factor:
            return GET_PROFIT(code,path_or_net,start,end)
#STOCK_FEATURES（暂用名称）作为指标计算的主函数，然后调用下面各个函数，分别计算技术指标；

def GET_ILLIQ(code,path_or_net,start,end,standardize,parameter=5):
#GET_ILLIQ是用来获得非流动性指标的函数
    if path_or_net != False:
        try:
            P_temp = pd.read_csv(path_or_net,encoding='GB18030', 
             delimiter = ',',index_col = 'date')
        except:
            raise ('Patherror')
    else:
        P_temp = DataFrame(ts.get_hist_data(code,start = start.strftime('%Y-%m-%d'), 
                            end = end.strftime('%Y-%m-%d')),index_col='date')    
#上方代码用于获得价格数据（暂时只接受‘日’线数据）
#依照制定路径或者网络数据获得价格数据，然后成为DataFrame格式文件，方便后续处理
    P_temp['ILLIQ'] = 0
    for i in np.arange(P_temp.shape[0]):
        P_sector = P_temp.ix[i:i+parameter-1]
        P_temp.ix[i,'ILLIQ'] = np.average(abs((P_sector.close-P_sector.open)
        /P_sector.volume)) if i+parameter-1 <= P_temp.shape[0] else np.nan
#非流动性指标计算公式参照文档
#如果规定期间范围内，前期数据不足要求平均的数据期数，那么返回np.nan
    if standardize != False:
        qt = P_temp.ILLIQ.quantile([0.05,0.95])
        if isinstance(qt, pd.Series) and len(qt) ==2:
            P_temp.ILLIQ[P_temp.ILLIQ < qt.iloc[0]]=qt.iloc[0]
            P_temp.ILLIQ[P_temp.ILLIQ > qt.iloc[1]]=qt.iloc[1]
        P_temp.ILLIQ = (P_temp.ILLIQ - P_temp.ILLIQ.mean())/(P_temp.ILLIQ.std())
        return P_temp
    else:
        return P_temp
    
def GET_PROFIT(code,path_or_net):
    pass