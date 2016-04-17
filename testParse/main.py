__author__ = 'Xerocry'

from testParse.models import Authors, Scopus, Spin, Wos
import json
from datetime import datetime, timedelta
import datetime
import time


with open('D:/scopus_test.json') as data_file:
    jdata = json.load(data_file)

for title in jdata:
    for key, value in title.items():
        # print(key, " : ", value, "\n")
        print(datetime.date.fromtimestamp(int(title["pubDate"])), "\n")
        # print(title["pubDate"], "\n")

        # tmpDate = datetime(1970, 1, 1) + timedelta(microseconds=int(title["pubDate"])/10)
        # Scopus.objects.create(pubDate = tmpDate, scopusIdentifier=(title["scopusIntid"]), wosUid=title["wosUid"], spinId=title["spinId"], doi=title["doi"], language=title["language"])
        # if key == "authors":
            # for pos, data in value.items():
            #     for pos1 in data:
                    # print(pos, " : ",data, " : ", pos1, "\n")
                    # Authors.objects.create(article = pos1["orcId"], name = pos1["name"], position=pos)
                    # Test.objects.create(parent_name=value["parent_name"], category=value["category"])


context = {"fields": Scopus.objects.all()}