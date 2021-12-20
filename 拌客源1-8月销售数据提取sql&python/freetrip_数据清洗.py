"""
对 freetrip_源文件未清洗.csv 该非结构化数据进行数据清洗
制作人: 严世宇
"""

import pandas as pd
import numpy as np
import matplotlib as plt

dataframe = pd.read_csv('freetrip_源文件未清洗.csv', index_col=0)

"""去除空格"""
col = dataframe.columns.values
# 循环
# new = []
# for item in col:
#     new.append(item.strip())
dataframe.columns = [x.strip() for x in col]

"""重复值的查看"""
# print(
# dataframe.duplicated()  # 返回布尔型数据，告诉重复值的位置
# dataframe.duplicated().sum()
# dataframe[dataframe.duplicated()]  # 查看重复的记录
# )

"""删除重复值"""
dataframe.drop_duplicates(inplace=True)  # inplace=True表示直接在源数据上进行操作
# 修改源数据集，需要index重置
dataframe.index = range(dataframe.shape[0])  # RangeIndex(start=0, stop=5000, step=1)
# 检查index
# print(dataframe.index)

"""异常值的处理"""
# 显示数值型数据
# print(dataframe.describe().T)
# 可以看到最大值异常，通关判断是否超过三倍标准差 : (x-mean)/std >3
sta = (dataframe['价格'] - dataframe['价格'].mean()) / dataframe['价格'].std()
# 查看数据中符合条件的异常值
# print(dataframe[abs(sta) > 3])

# 找节省的异常值:节省最多等于价格，而不应该高于价格
# 同时删去节省和价格的异常值
del_index = pd.concat([dataframe[dataframe.节省 > dataframe.价格], dataframe[sta.abs() > 3]]).index
# 删除指定index
dataframe.drop(del_index, inplace=True)
dataframe.index = range(dataframe.shape[0])


"""缺失值的处理"""
# 查看缺失值，并按照类型filter
# print(dataframe.isnull().sum())
# 根据已知路线名修改正确出发地和目的地
# 填上正确出发地
dataframe.loc[dataframe.出发地.isnull(), '出发地'] = [str(x)[:2] for x in dataframe[dataframe.出发地.isnull()].路线名]
# 目的地
dataframe.loc[dataframe.目的地.isnull(), '目的地'] = [str(x)[3:5] for x in dataframe[dataframe.目的地.isnull()].路线名]

# 缺失值
# 查看价格缺失的项
# print(dataframe[dataframe.价格.isnull()])
# 处理价格缺失值: 按平均值处理
dataframe.价格.fillna(round(dataframe.价格.mean(), 0), inplace=True)
# 处理节省缺失值: 按该项平均值处理
dataframe.节省.fillna(round(dataframe.节省.mean(), 0), inplace=True)

"""增加数据列"""
# 提取酒店评分
dataframe['酒店评分'] = dataframe.酒店.str.extract('(\d\.\d)分/5分', expand=False)
# 提取酒店等级
dataframe['酒店等级'] = dataframe.酒店.str.extract(' (.+) ', expand=False)
# 填充空的酒店等级
# dataframe.loc[dataframe.酒店等级.isnull(), '酒店等级'] = '无'
dataframe.酒店等级.fillna('无', inplace=True)
# 提供天数信息
dataframe['天数'] = dataframe.路线名.str.extract('(\d)天\d晚',expand=False)

"""写入新csv"""
# dataframe.to_csv('freetrip_清洗完毕.csv',encoding='utf-8-sig')
