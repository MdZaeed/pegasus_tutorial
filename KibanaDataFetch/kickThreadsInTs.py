#!/usr/bin/env python3

import json
import math
from os import write
import numpy
from numpy.core.fromnumeric import sort
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def changeRange(ts,sts):
    return ts - min(sts)
    # a= numpy.modf(b)
    # return a[1].astype(int)

wf_id = "42e89572-5a05-431b-9f53-db62f02fceb5"
with open("kickstart/" + wf_id) as f:
    workflow_ids = f.read()
f.close()
lst = json.loads(workflow_ids)
df = pd.DataFrame(lst)

with open("stampede/" + wf_id) as f:
    workflow_ids = f.read()
f.close()
lst = json.loads(workflow_ids)
sdf = pd.DataFrame(lst)

pd.set_option('float_format', '{:f}'.format)

df['tsTrans'] = changeRange(df['ts'],sdf['ts'])
df['pid'] = df['pid'].astype(str)
pid_job = df['pid'] + " : " + df['dag_job_id']
df['pid_job'] = pid_job

# fig = px.scatter_matrix(df, 
#     dimensions = ['tsTrans','threads','procs'],
#     color = "pid_job")
# fig.show()

df_subset = df.loc[:, ['dag_job_id','tsTrans','threads']]
tsG = df_subset.groupby('tsTrans')['threads'].sum().reset_index()
# tsG = df_subset.groupby('tsTrans')['threads'].sum()
# tsG.reset_index()
# print(tsG.head(100))

# print(tsG)
fig2 = px.scatter_matrix(tsG)
# fig2.show()

# print(min(df['ts']))
# print(min(sdf['ts']))
# sdf[sdf['event'] == 'stampede.task.monitoring']
select_mon = sdf.loc[sdf['event'] == 'stampede.task.monitoring']
select_mon = select_mon[['event','job__id','start_time','end_time']].reset_index()
# print(select_mon)

df.sort_values(by=['ts'])

ts_range = min(sdf['ts'])
range = 35
tss = []
no_of_threadss = []
while (ts_range < max(sdf['ts'])):
    no_of_threads = 0
    for index, item in sdf.iterrows():
        if (item['start_time'] < ts_range) & (item['end_time'] > ts_range):
            # print(item['job__id'] + " running on " + str(ts_range-min(sdf['ts'])))
            job_id = item['job__id']
            select_mont = df.loc[(df['dag_job_id'] == job_id) & (df['ts'] > ts_range) & (df['ts'] < ts_range+range)].reset_index()
            select_mont_g = select_mont.groupby('pid').tail(1)
            # print(select_mont_g)
            for ind, it in select_mont_g.iterrows():
                no_of_threads+= it['threads'] 
    ts_range+=range
    # print(str(ts_range) + ": " + str(no_of_threads))
    tss.append(ts_range-min(sdf['ts']))
    no_of_threadss.append(no_of_threads)

# df_T = df.groupby(['dag_job_id','pid'])
# print(df_T.last()['ts'])

fig =px.line(x=tss, y=no_of_threadss)
fig.show()
