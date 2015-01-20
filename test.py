import pprint
import json
import elasticsearch

index_doc = {}
index_doc["id"] = "123456"
index_doc["name"] = "Russell Wilson"
index_doc["position"] = "QB"
index_doc["team"] = "Seattle Seahawks"

#submit to elasticsearch
es_api = elasticsearch.Elasticsearch()
es_api.index(
    index="nfl",
    doc_type="players",
    id=index_doc["id"],
    body=index_doc
    )

#print output to console
pprint.pprint(index_doc)


