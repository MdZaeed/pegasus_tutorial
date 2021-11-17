#!/usr/bin/env python3

import json
import math
from os import utime, write
import numpy
from numpy.core.fromnumeric import sort
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from os.path import exists
import sys

def normalize(feature_name):
    max_value = feature_name.max()
    min_value = feature_name.min()
    result = (feature_name - min_value) / (max_value - min_value)
    return result

def toMegabytes(feature_name):
    return feature_name / 1048576

def changeRange(ts):
    b = ts - min(ts)
    # a= numpy.modf(b)
    # return a[1].astype(int)
    return b

with open("toReadForB") as f:
    workflow_ids = f.read().splitlines()

pd.set_option('float_format', '{:f}'.format)

kick_dfs = []
stamp_dfs = []
transfer_dfs = []
# wf_id = "eb2900f6-f072-41ba-8a28-da54010cc916" #1000-gnome
# wf_id = "42e89572-5a05-431b-9f53-db62f02fceb5" #SNS-namd
for workflow_id in workflow_ids:
    with open("kickstart/" + workflow_id) as f:
        temp_data = f.read()
        f.close()
    lst = json.loads(temp_data)
    kick_df = pd.DataFrame(lst)
    if kick_df.empty != True:
        kick_dfs.append(kick_df)

    if exists("stampede/" + workflow_id):
        with open("stampede/" + workflow_id) as f:
            temp_data = f.read()
        f.close()
    lst = json.loads(temp_data)
    stamp_df = pd.DataFrame(lst)
    if stamp_df.empty != True:
            stamp_dfs.append(stamp_df)
    else:
        stamp_dfs.append(pd.DataFrame())


    with open("transfer/" + workflow_id) as f:
        temp_data = f.read()
    f.close()
    lst = json.loads(temp_data)
    transfer_df = pd.DataFrame(lst)
    if transfer_df.empty != True:
        transfer_dfs.append(transfer_df)

    # Showing threads counts in workflows
    # select_mon = stamp_df.loc[stamp_df['event'] == 'stampede.task.monitoring']
    # select_mon = select_mon[['event','job__id','start_time','end_time']].reset_index()

    kick_df.sort_values(by=['ts'])

    ts_range = min(stamp_df['ts'])
    range = 35
    tss = []
    bwritten = []
    bread = []
    bsum = []
    while (ts_range < max(stamp_df['ts'])):
        byteWritten = 0
        bytesRead = 0
        select_mont = kick_df.loc[(kick_df['ts'] < ts_range+range)].reset_index()
        if select_mont.empty != True : 
            select_mont_g = select_mont.groupby('pid').tail(1)
            for ind, it in select_mont_g.iterrows():
                byteWritten+= it['bwrite'] 
                bytesRead += it['bread']
        ts_range+=range
        tss.append(ts_range-min(stamp_df['ts']))
        bwritten.append(byteWritten)
        bread.append(bytesRead)
    bwritten = pd.Series(bwritten)
    bwritten = bwritten.diff().fillna(bwritten)
    bwritten = toMegabytes(bwritten)
    bread = pd.Series(bread)
    bread = bread.diff().fillna(bread)
    bread = toMegabytes(bread)
    fig =px.bar(x=tss, y=[bread,bwrite],
        title="Single Bytes analysis by " + workflow_id,barmode="group")
    fig.show()


# if(len(sys.argv)==2): kick_dfs[int(sys.argv[1])].to_excel("KickSmapleNew.xlsx")
# if(len(sys.argv)==2): stamp_dfs[int(sys.argv[1])].to_excel("StampSample.xlsx")
# if(len(sys.argv)==2): transfer_dfs[int(sys.argv[1])].to_excel("TransferSample.xlsx")



# df = kick_dfs[0]

# ut_st_rat = df['utime'] / df['stime']
# df['ut_st_ratio'] = ut_st_rat
# vm_procs_rat = df['vm'] / df['procs']
# df['vm_procs_ratio'] = vm_procs_rat
# df['pid'] = df['pid'].astype(str)
# pid_job = df['pid'] + " : " + df['dag_job_id']
# df['pid_job'] = pid_job
# df['tsTrans'] = changeRange(df['ts'])
# df['vmTrans'] = normalize(df['vm'])
# df['bwriteT'] = normalize(df['bwrite'])
# df['utimeT'] = normalize(df['utime'])
# df['stimeT'] = normalize(df['stime'])
# df['iowaitT'] = normalize(df['iowait'])

# yValues = ["tsTrans","threads","vm","bwrite","utime","stimeT","iowaitT","ut_st_ratio","vm_procs_ratio"]

# tempFig = px.scatter_matrix(df, 
#     dimensions = yValues,
#     color = "pid_job")
# tempFig.show()




