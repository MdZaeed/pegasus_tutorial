#!/usr/bin/env python3

import json
import math
from os import utime, write
from dash.html import Center
import numpy
from numpy.core.fromnumeric import sort
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

def normalize(feature_name):
    max_value = feature_name.max()
    min_value = feature_name.min()
    result = (feature_name - min_value) / (max_value - min_value)
    return result


def changeRange(ts):
    b = ts - min(ts)
    # a= numpy.modf(b)
    # return a[1].astype(int)
    return b

# wf_id = "eb2900f6-f072-41ba-8a28-da54010cc916" #1000-gnome
wf_id = "14f1dc74-c508-49de-b17a-61ff68117f30" #SNS-namd

with open("kickstart/" + wf_id) as f:
    workflow_ids = f.read()

f.close()

lst = json.loads(workflow_ids)

df = pd.DataFrame(lst)
# df.set_index('dag_job_id')
# df1  = df.loc[['sassena_ID0000005']]
# fd = df
# fd[fd['dag_job_id'] == 'namd_ID0000002']
# print(fd.nunique())

# df.reset_index()
# df.to_excel("kickSampleFailed.xlsx")

pd.set_option('float_format', '{:f}'.format)

ut_st_rat = df['utime'] / df['stime']
df['ut_st_ratio'] = ut_st_rat
vm_procs_rat = df['vm'] / df['procs']
df['vm_procs_ratio'] = vm_procs_rat
df['pid'] = df['pid'].astype(str)
pid_job = df['pid'] + " : " + df['dag_job_id']
df['pid_job'] = pid_job
df['tsTrans'] = changeRange(df['ts'])
df['vmTrans'] = normalize(df['vm'])
df['bwriteT'] = normalize(df['bwrite'])
df['utimeT'] = normalize(df['utime'])
df['stimeT'] = normalize(df['stime'])
df['iowaitT'] = normalize(df['iowait'])

# yValues = ["threads","vm","bwrite","uTime","stimeT","iowaitT","ut_st_ratio","vm_procs_ratio"]
yValues = ["tsTrans","vm","bwrite","utime","stimeT","iowaitT","ut_st_ratio","vm_procs_ratio"]
# for item in yValues:
#     tempFig = px.scatter(df, 
#         y = item,
#         x = "tsTrans",
#         color = "pid_job")
#     tempFig.show()
app = dash.Dash()
optio = []
for yV in yValues:
    optio.append({'label':yV,'value':yV})
drop = dcc.Dropdown(id="DD",options=optio,value="vm_procs_ratio")
fig = html.Div(id='dd-output-container',style={'text-align':'center'})
figs = [drop,fig]

@app.callback(
    Output('dd-output-container', 'children'),
    Input('DD', 'value')
)
def update_output(value):
    tempFig = px.scatter(df, 
        x= 'tsTrans', y= value,
        color = "pid_job")
    return dcc.Graph(id=value+"fig",figure=tempFig,style={'width': '60vh', 'height': '40vh'})

# for item in yValues:
#     tempFig = px.scatter(df, 
#         x= 'tsTrans', y= item,
#         color = "pid_job")
#     figs.append(dcc.Graph(id=item,figure=tempFig))


def update_output(value):
    return 'You have selected "{}"'.format(value)

app.layout = html.Div(children=figs)

app.run_server(debug=True)  # Turn off reloader if inside Jupyter

# count = 1
# data = ['0']
# for item in yValues:
#     tempFig = px.scatter(df, 
#         y = item,
#         x = "tsTrans",
#         color = "pid")
#     # fig.add_trace(tempFig,count,1)
#     data.append(tempFig)
#     count = count +1 

# fig = go.Figure(data= data, layout=None)
# fig.update_layout(height=6000, width=8000, title_text="Side By Side Subplots")    
# fig.show()

# df_subset = df.loc[:, ['dag_job_id','tsTrans','threads']]
# tsG = df_subset.groupby('tsTrans')['threads'].sum().reset_index()
# # tsG = df_subset.groupby('tsTrans')['threads'].sum()
# # tsG.reset_index()
# # print(tsG.head(100))
# print(tsG)
# fig2 = px.scatter_matrix(tsG)
# fig2.show()



