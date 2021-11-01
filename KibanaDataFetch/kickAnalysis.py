#!/usr/bin/env python3

import json
from os import write
from numpy.core.fromnumeric import sort
import pandas as pd
import plotly.express as px

def changeRange(ts):
    return ts - min(ts)

wf_id = "eb2900f6-f072-41ba-8a28-da54010cc916"

with open("kickstart/" + wf_id) as f:
    workflow_ids = f.read()

f.close()

lst = json.loads(workflow_ids)

df = pd.DataFrame(lst)

# include =['int']
pd.set_option('float_format', '{:f}'.format)

df['ts'] = changeRange(df['ts'])
# series = df["vm"].describe()
# series2 = df["pid"].describe(include= include)

# first = df.dag_job_id == "individuals_wrapper_ID0000019"
# print(series)
# # print(series2)

# print(df[first].describe())

# dags = df.groupby("dag_job_id")
# sc = lambda x: (x - x.min())
# dags.transform(sc,'ts')

# df['new'] = dags.apply(lambda x: x['ts'] - x['ts'].min())
# print(dags.head())
# print(dags.groups)

# for ts,dag_job_id in dags:
#     print(dag_job_id)
#     print(ts)

fig = px.scatter_matrix(df, 
    dimensions = ['ts','threads'],
    color = "dag_job_id")
fig.show()


