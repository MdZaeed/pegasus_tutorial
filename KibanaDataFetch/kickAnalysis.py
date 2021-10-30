#!/usr/bin/env python3

import json
from os import write
import pandas as pd

wf_id = "eb2900f6-f072-41ba-8a28-da54010cc916"

with open("kickstart/" + wf_id) as f:
    workflow_ids = f.read()

f.close()

lst = json.loads(workflow_ids)

df = pd.DataFrame(lst)

print(df)

