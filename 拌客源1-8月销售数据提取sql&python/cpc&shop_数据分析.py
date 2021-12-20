"""
对cpc.csv,shop.csv 使用sql与python进行数据分析和制图
制作人: 严世宇
"""

import pandas as pd
import pymysql

pd.set_option('display.max_rows', 9999)
pd.set_option('display.max_columns', 9999)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

cpc = pd.read_csv('cpc.csv', sep=',', encoding='gbk')

# - 1【select】筛选门店名称并且去重
# select distinct(平台门店名称)
# from ddm.cpc
# 返回去重平台名称，series格式
# print(pd.Series(pd.unique(cpc.平台门店名称)))

# - 2【select】筛选出平台门店名称，以及计算下单率
# select 平台门店名称，(门店下单量/门店访问量) as 下单率
# from ddm.cpc
# cpc['符号'] = '%'
# cpc['下单率'] = (round(cpc.门店下单量 / cpc.门店访问量, 1) * 100).map(str).str.cat(cpc['符号'])
# # [['x1','x2']]：select
# # cpc：from
# print(cpc[['平台门店名称', '下单率']])

# 样例演示
# - 1【运算符】and：查找gmvroi>7 且 gmvroi<8 的门店ID跟名字
# select  门店ID,平台门店名称
# from    ddm.cpc
# where   gmvroi <8.0
# and     gmvroi >7.0

# - 2【运算符】between and：查找门店gmvroi介于[7,8]的门店ID跟名字
# select 	门店ID,平台门店名称
# from 	ddm.cpc
# where 	gmvroi between 7.0 and 8.0

# print(cpc.query('gmvroi>7.0&gmvroi<8.0')[['门店ID','平台门店名称']])
# print(cpc[cpc.gmvroi.between(7,8)][['门店ID','平台门店名称']])
# query：where
# &：and

# - 3【运算符】in：查找门店gmvroi等于[7,8]的门店ID跟名字
# select 	门店ID,平台门店名称
# from 	ddm.cpc
# where 	gmvroi in(7.0,8.0)
# select 放置先后顺序没关系
# print(cpc[['门店ID', '平台门店名称']][cpc.gmvroi.isin([7, 8])])
# print(cpc[cpc.gmvroi.isin([7, 8])][['门店ID', '平台门店名称']])
# - 4【运算符】null：查找门店实收为空的门店ID跟名字
# select 	门店ID,平台门店名称
# from 	ddm.cpc
# where 	门店实收 is null

# print(cpc[cpc.门店实收.isnull()][['门店ID', '平台门店名称']])
# cpc[['门店ID','平台门店名称']]：select 门店ID,平台门店名称
# []内cpc：from
# 门店实收.isnull()：where 	门店实收 is null

# - 5【模糊查询】like：查找名称带有宝山的门店
# select  distinct(平台门店名称)
# from    ddm.cpc
# where 平台门店名称 like '%宝山%'
# print(pd.Series(cpc.平台门店名称[cpc.平台门店名称.str.contains('宝山')].unique()))
# cpc['平台门店名称']：select 平台门店名称
# []内cpc：from
# 平台门店名称.str.contains('宝山')：平台门店名称 like '%宝山%'
# unique()：distinct
# pd.Series：将结果转换为Series类型

# - 1【聚合函数】avg：查找各个门店的平均实收
# select  	平台门店名称,avg(门店实收) as 平均实收
# from    	ddm.cpc
# group by 	平台门店名称

# print(cpc.groupby('平台门店名称').agg(平均实收=('门店实收', 'mean')))
# cpc：from
# groupby('平台门店名称')：group by 平台门店名称
# agg(平均实收 = ('门店实收','mean'))：avg(门店实收) as 平均实收
# 最终结果会显示所有提到的字段

# - 2【分组筛选】having：查找实收>10k的门店名称 与 实收，按实收降序
# select  	平台门店名称,sum(门店实收)
# from    	ddm.cpc
# group by 	平台门店名称
# having      sum(门店实收)>10000
# order by    sum(门店实收) desc

# print(cpc.groupby('平台门店名称').agg(总合=('门店实收', 'sum')).query('总合>10000').sort_values(by='总合', ascending=False))
# cpc:from
# groupby('平台门店名称'):group by 平台门店名称
# agg(总合 = ('门店实收','sum')):sum(门店实收)
# query('总合>10000'):having sum(门店实收)>10000
# sort_values(by = '总合',ascending=False):order by sum(门店实收) desc

# - 1【排序】order by：查看每个“武宁路”门店的实收，按实收降序
# select 		平台门店名称,sum(门店实收)
# from		ddm.cpc
# where 		平台门店名称 like '%武宁路%'
# group by 	平台门店名称
# order by 	sum(门店实收) desc

# x = cpc[cpc.平台门店名称.str.contains('武宁路')]
# print(x.groupby(cpc.平台门店名称).agg(实收=('门店实收', 'sum')).sort_values(by='实收', ascending=False))
# 代码较长，采用两段的形式讲解
# cpc.平台门店名称.str.contains('武宁路'):where 平台门店名称 like '%武宁路%'
# groupby(cpc.平台门店名称):group by 平台门店名称
# sort_values(by='实收',ascending = False):order by sum(门店实收) desc
# agg(实收 = ('门店实收','sum')):sum(门店实收)


# - 习题1【LIMIT】limit x,y：跳过前5行，显示5条数据
# select 	*
# from 	ddm.cpc
# limit 	5,5
# print(cpc[5:10])

# 习题2【LIMIT】查找前5行的门店名称
# select	平台门店名称
# from 	ddm.cpc
# limit	5
# print(cpc.loc[:4,'平台门店名称'])

# - 习题2【LIMIT】查找门店平均实收>1K的门店名称与平均实收，显示前10条数据，结构按照平均实收降序
# select 		平台门店名称,avg(门店实收) as 平均实收
# from		ddm.cpc
# group by 	平台门店名称
# having      平均实收 > 1000
# order by 	平均实收 desc
# limit       5

# groupby的项会出现在最后表单中
# print(cpc.groupby('平台门店名称').agg(平均实收=('门店实收', 'mean')).query('平均实收>1000').sort_values(by='平均实收', ascending=False).head(5))
# cpc:from ddm.cpc
# groupby('平台门店名称'):group by 平台门店名称
# order by 平均实收 desc:query('平均实收>1000')
# sort_values(by = '平均实收',ascending=False):order by 	平均实收 desc
# head(5):limit 5
# agg(平均实收 = ('门店实收','mean')):avg(门店实收) as 平均实收

# 子查询
# - 1：查找实收（cpc.csv）>1K的门店名称
# select  distinct 平台门店名称
# from    ddm.cpc
# where   门店ID
# in
#     (
#     select  门店ID
#     from    ddm.cpc
#     where   门店实收>1000
#     )

# a = cpc.query('门店实收>1000').门店ID  # 子查询条件a:门店实收>1k的门店ID
# b = cpc['平台门店名称'][cpc['门店ID'].isin(a)].unique()  # 将条件放入isin()当中
# print(pd.Series(b))


# shop = pd.read_csv('./shop.csv', encoding='gbk')
# # - 1【内连接】：查看门店名称（shop）的实收（cpc）（连接字段：门店ID）
# # select 		s.门店名称
# # 			,sum(c.门店实收)
# # from 		ddm.cpc c
# # join 		ddm.shop s
# # on 			c.门店ID = s.门店ID
# # group by 	s.门店名称
# M = pd.merge(cpc, shop, left_on='门店ID', right_on='门店ID', how='inner')
# M.groupby(['门店名称']).agg(门店实收=('门店实收', 'sum'))
# # 代码较长，分为两段
# # pd.merge:join
# # cpc,shop:from cpc join shop
# # left_on:左表cpc连接字段
# # right_on:右表shop连接字段
# # how = 'inner':(inner) join
# # groupby(['门店名称']):group by s.门店名称

# # - 2 继续题1，采用2个连接字段：门店ID与日期
# # select 		s.门店名称
# # 			,sum(c.门店实收)
# # from 		ddm.cpc c
# # join 		ddm.shop s
# # on 			c.门店ID = s.门店ID
# # and			c.日期 = s.日期
# # group by 	s.门店名称
#
# M = pd.merge(cpc,shop,left_on = ['门店ID','日期'],right_on = ['门店ID','日期'],how = 'inner')
# M.groupby(['门店名称']).agg(门店实收 = ('门店实收','sum'))


# # - 1：每一天/不同门店的/门店实收排名，采用日期、门店实收正序输出
# # select  日期
# #         ,平台门店名称
# #         ,门店实收
# #         ,rank() over (partition by 日期 order by 门店实收 desc) as rankk
# # from    ddm.cpc
# # order by 日期,门店实收 desc
#
# cpc['rank'] = cpc.groupby('日期')['门店实收'].rank(method='min', ascending=False)
# # 这里相当于rank() over (partition by 日期 order by 门店实收 desc) as rankk
#
# print(cpc.sort_values(by=['日期', '门店实收'], ascending=[True, False])[['日期', '平台门店名称', '门店实收', 'rank']])
# # sort_values(by = ['日期','门店实收'],ascending=[True,False]):order by 日期,门店实收 desc
# # [['日期','平台门店名称','门店实收','rank']]:select  日期,平台门店名称,门店实收,rankk
# cpc['rank'] = cpc.groupby(['日期','平台i'])['门店实收'].rank(method = 'min

# 数据透视表
# pivot table 数据透视表 - 1：各个门店在不同平台的商家实收 table = pd.pivot_table(cpc, values = ['门店实收','cpc总费用'], index = ['平台门店名称'],
# columns = ['平台i'], aggfunc = np.sum).fillna(0) print(table)

