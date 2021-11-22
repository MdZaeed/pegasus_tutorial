#!/usr/bin/env python3

import json
import math
from os import utime, write
import numpy
from numpy.core.fromnumeric import mean, sort
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from os.path import exists
import sys

def deviation(feature_name):
    result = (feature_name - feature_name.mean())
    return result


pd.set_option('float_format', '{:f}'.format)

with open("uids") as f:
    workflow_ids = f.read().splitlines()

# 29a158f5-3d8d-4b3e-b76a-c0aea646b3ac longest
# e8c30de5-6bb2-4b38-a000-2b719e688e38 shortest

kick_stats = []
for workflow_id in workflow_ids:
    row = []
    with open("kickstart/" + workflow_id) as f:
        temp_data = f.read()
        f.close()
    lst = json.loads(temp_data)
    kick_df = pd.DataFrame(lst)

    if kick_df.empty != True:
        if kick_df.loc[0,'wf_label'].__contains__('1000'):
            # print(kick_df.iloc[1,9])
            row.append(workflow_id)
            row.append(kick_df.loc[0,'wf_label'])
            row.append(int(max(kick_df['ts']-min(kick_df['ts']))))
            # kick_stats.append(row)
            # print(row)
        # print(row)

    with open("stampede/" + workflow_id) as f:
        temp_data = f.read()
        f.close()
    lst = json.loads(temp_data)
    kick_df = pd.DataFrame(lst)
    if kick_df.empty != True:
        if kick_df.loc[0,'dax__label'].__contains__('1000'):
            # print(kick_df.iloc[1,9])
            row.append(int(max(kick_df['ts']-min(kick_df['ts']))))
            kick_stats.append(row)

coloumns = ['wf_uid','wf_label','makespan','stampmakespan']
kick_stats_df = pd.DataFrame(kick_stats,columns=coloumns)
print(kick_stats_df)
kick_stats_df['tsDev'] = deviation(kick_stats_df['makespan'])
kick_stats_df.to_excel("kickStats1000.xlsx")