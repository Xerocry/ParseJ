__author__ = 'Xerocry'

from testParse.models import Authors, Scopus, Spin, Wos
import json


with open('D:/fuck.json') as data_file:
    jdata = json.load(data_file)

for title in jdata:
    for key, value in title.items():
        if key == "fields":
            print(key, " : ", value, "\n")
            # Test.objects.create(parent_name=value["parent_name"], category=value["category"])

# context = {"fields": Test.objects.all()}