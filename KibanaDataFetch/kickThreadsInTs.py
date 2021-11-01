#!/usr/bin/env python3

import json
import math
from os import write
import numpy
from numpy.core.fromnumeric import sort
import pandas as pd
import plotly.express as px

def changeRange(ts):
    b = ts - min(ts)
    a= numpy.modf(b)
    return a[1].astype(int)

wf_id = "eb2900f6-f072-41ba-8a28-da54010cc916"

with open("kickstart/" + wf_id) as f:
    workflow_ids = f.read()

f.close()

lst = json.loads(workflow_ids)

df = pd.DataFrame(lst)

pd.set_option('float_format', '{:f}'.format)

df['tsTrans'] = changeRange(df['ts'])

fig = px.scatter_matrix(df, 
    dimensions = ['tsTrans','threads'],
    color = "dag_job_id")
# fig.show()

df_subset = df.loc[:, ['dag_job_id','tsTrans','threads']]
tsG = df_subset.groupby('tsTrans')['threads'].sum().reset_index()
# tsG = df_subset.groupby('tsTrans')['threads'].sum()
# tsG.reset_index()
# print(tsG.head(100))
print(tsG)
fig2 = px.scatter_matrix(tsG)
fig2.show()


