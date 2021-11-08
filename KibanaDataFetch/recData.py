#!/usr/bin/env python3

import json
from os import write
from elasticsearch import Elasticsearch

es = Elasticsearch("https://data.panorama.isi.edu")

es_ids = set()
statistics = {}

workflow_id = ""

with open("uids") as f:
    workflow_ids = f.read().splitlines()

for workflow_id in workflow_ids:
    # Change xwf__id to wf_uuid for kickstart and transfer data
    query = 'wf_uuid: "'+ workflow_id + '"'
    print(query)
    # Change to panorama_stampede and panorama_transfer for corresponding data, remove sort='ts' for panorama_transfer
    res = es.search(index="panorama_kickstart", q=query, scroll="30m", sort='ts', size=100)
    num_results = res['hits']['total']
    print("Total Results: %d" % num_results)

    data = []
    if num_results > 0:
        total_lines = 0
        while total_lines != num_results:
            if res['_scroll_id'] not in es_ids:
                es_ids.add(res['_scroll_id'])
            for doc in res['hits']['hits']:
                data.append(doc['_source'])
                total_lines += 1
            res = es.scroll(scroll='30m', scroll_id=res['_scroll_id']) 
            
    print("Total data: %d" % len(data))
    print("Contents of 1st record:")
    # print(json.dumps(data[0], indent=2))
    dataF = open("kickstart/" + workflow_id,'x')
    dataF.write(json.dumps(data, indent = 2 ))