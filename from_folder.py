#!/usr/bin/python
import json
import pprint
import elasticsearch
import os

path = "/mapr/demo.mapr.com/user/mapr/data/"

#method called to ingest data, takes json string as input
#parses out id,username,tweet and submits as well as prints to output
def submit_data(data):
        #create json object based on string passed
        j = json.loads(data)
        print "*" * 20
	
        es = {}
        es["id"] = str(j["id"]).replace("'","").replace("\"", "")
        es["username"] = j["user"]["screen_name"]
        es["tweet"] = j["text"]
        es_j = json.dumps(es)

        #submit to elasticsearch
        es_api = elasticsearch.Elasticsearch()
        es_api.index(
                index="folderdata",
                doc_type="tweets",
                id=es["id"],
                body=es
                )

        #print output to console
        pprint.pprint(es)
        print "*" * 20
        return True


ofolder = os.listdir(path)

#iterate through each file and submit to the index
for filename in ofolder:
    contents = open(path + filename, "r").read()
    submit_data(contents)
