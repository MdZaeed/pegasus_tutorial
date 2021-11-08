#!/usr/bin/env python3

import json
from os import write
from elasticsearch import Elasticsearch

es = Elasticsearch("https://data.panorama.isi.edu")

es_ids = set()
statistics = {}

workflow_id = "eb2b1ada-b5ab-4b40-9f98-7a3196e6351e"
dag_job_id = "individuals_wrapper_ID0000006"

query = 'wf_uuid: "'+ workflow_id + '"'
print(query)
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
print(json.dumps(data[0], indent=2))

dataF = open("stampede/" + workflow_id,'x')
dataF.write(json.dumps(data, indent = 2 ))