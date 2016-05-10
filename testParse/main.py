import glob
import json
from testParse.dprint import dprint
from testParse.sort import filter1

__author__ = 'Xerocry'


# for file in glob.iglob('D:/publication/**/spin*.json'):
#      with open(file, 'r') as data_file:
#         jdata = json.load(data_file)
#         spin_Parse(jdata)


# for file in glob.iglob('D:/publication/**/scopus*.json'):
#      with open(file, 'r') as data_file:
#         jdata = json.load(data_file)
#         scopus_Parse(jdata)

# for file in glob.iglob('D:/publication/**/wos*.json'):
#      with open(file, 'r') as data_file:
#         jdata = json.load(data_file)
#         wos_Parse(jdata)

for file in glob.iglob('D:/publication/newArticles/*.json'):
     with open(file, 'r') as data_file:
        jdata = json.load(data_file)
        dprint(filter1(jdata))


# q = Article.objects.exclude(doi__isnull=True)
# dprint(q)

# context = {"fields": Article.objects.all()}

