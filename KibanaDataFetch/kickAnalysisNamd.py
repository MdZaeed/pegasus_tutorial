#!/usr/bin/env python3

import json
import math
from os import write
import numpy
from numpy.core.fromnumeric import sort
import pandas as pd
import plotly.express as px

def normalize(feature_name):
    max_value = feature_name.max()
    min_value = feature_name.min()
    result = (feature_name - min_value) / (max_value - min_value)
    return result


def changeRange(ts):
    b = ts - min(ts)
    a= numpy.modf(b)
    return a[1].astype(int)

wf_id = "0d3a50e8-d8f9-4ad1-a3d0-cceba3c9e6e1"

with open("kickstart/" + wf_id) as f:
    workflow_ids = f.read()

f.close()

lst = json.loads(workflow_ids)

df = pd.DataFrame(lst)

pd.set_option('float_format', '{:f}'.format)

df['tsTrans'] = changeRange(df['ts'])
df['pid'] = df['pid'].astype(str)
pid_job = df['pid'] + " : " + df['dag_job_id']
df['pid_job'] = pid_job
df['vmTrans'] = normalize(df['vm'])
df['bwriteT'] = normalize(df['bwrite'])
df['utimeT'] = normalize(df['utime'])
df['stimeT'] = normalize(df['stime'])
df['iowaitT'] = normalize(df['iowait'])

fig = px.scatter_matrix(df, 
    dimensions = ['tsTrans','threads','vmTrans','bwriteT','utimeT','procs','stimeT','iowait'],
    color = "pid_job")
fig.show()

# df_subset = df.loc[:, ['dag_job_id','tsTrans','threads']]
# tsG = df_subset.groupby('tsTrans')['threads'].sum().reset_index()
# # tsG = df_subset.groupby('tsTrans')['threads'].sum()
# # tsG.reset_index()
# # print(tsG.head(100))
# print(tsG)
# fig2 = px.scatter_matrix(tsG)
# fig2.show()

# df.to_excel("kickSampleNamd.xlsx")


