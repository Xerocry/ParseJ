__author__ = 'Xerocry'

from testParse.models import Authors, Scopus, Spin, Wos
import json


with open('D:/scopus_test.json') as data_file:
    jdata = json.load(data_file)

for title in jdata:
    for key, value in title.items():
            # print(key, " : ", value, "\n")
            if key == "authors":
                for pos, data in value.items():
                    for pos1 in data:
                        # print(pos, " : ",data, "\n")
                        Authors.objects.create(article = pos1["orcId"], name = pos1["name"], position=pos)
                    # Test.objects.create(parent_name=value["parent_name"], category=value["category"])
            # Scopus.objects.create(spinId=value["spinId"], doi=["doi"], wosId=["wosUid"], language=["language"])

context = {"fields": Scopus.objects.all()}