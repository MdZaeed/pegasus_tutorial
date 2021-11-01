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

wf_id = "42e89572-5a05-431b-9f53-db62f02fceb5"

with open("kickstart/" + wf_id) as f:
    workflow_ids = f.read()

f.close()

lst = json.loads(workflow_ids)

df = pd.DataFrame(lst)

pd.set_option('float_format', '{:f}'.format)

df['tsTrans'] = changeRange(df['ts'])
df['vmTrans'] = normalize(df['vm'])
df['bwriteT'] = normalize(df['bwrite'])
df['utimeT'] = normalize(df['utime'])
df['stimeT'] = normalize(df['stime'])
df['iowaitT'] = normalize(df['iowait'])

fig = px.scatter_matrix(df, 
    dimensions = ['tsTrans','threads','vmTrans','bwriteT','utimeT','procs','stimeT','iowaitT'],
    color = "dag_job_id")
# fig.show()

# df_subset = df.loc[:, ['dag_job_id','tsTrans','threads']]
# tsG = df_subset.groupby('tsTrans')['threads'].sum().reset_index()
# # tsG = df_subset.groupby('tsTrans')['threads'].sum()
# # tsG.reset_index()
# # print(tsG.head(100))
# print(tsG)
# fig2 = px.scatter_matrix(tsG)
# fig2.show()

df.to_excel("kickSampleNamd.xlsx")


