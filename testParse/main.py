import glob
import json
from testParse.dprint import dprint
from testParse.models import Article
from testParse.sort import filterJdata, testFilter
from testParse.parse import spin_Parse, scopus_Parse, wos_Parse

__author__ = 'Xerocry'


# for file in glob.iglob('D:/publication/**/spin*.json'):
#      with open(file, 'r') as data_file:
#         jdata = json.load(data_file)
#         spin_Parse(jdata)
#
#
# for file in glob.iglob('D:/publication/**/scopus*.json'):
#      with open(file, 'r') as data_file:
#         jdata = json.load(data_file)
#         scopus_Parse(jdata)
#
# for file in glob.iglob('D:/publication/**/wos*.json'):
#      with open(file, 'r') as data_file:
#         jdata = json.load(data_file)
#         wos_Parse(jdata)

# for file in glob.iglob('D:/publication/newArticles/*.json'):
#      with open(file, 'r') as data_file:
#         jdata = json.load(data_file)
#         filter1(jdata, "Wos")
#         # dprint(filter1(jdata)) #debug

set = Article.objects.all()
# dprint(set)
f1 = open('./testfile.txt', 'w+')

# for art in set:
for i in range(100, 200):
    query = testFilter(set[i], set[i].ArticleSource)
    if(len(query) >= 1):
        for a in query:
            if not(a.id == set[i].id):
                # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", file=f1)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                # print("Title: ", art.title, " id: ", art.id, "\n")
                print("Title: ", set[i].title.encode("utf-8"), " id: ", set[i].id, "\n", file=f1)
                print("Title: ", set[i].title.encode("utf-8"), " id: ", set[i].id, "\n")
                # print("The same: ", a.title, " id: ", a.id, "\n")
                print("The same: ", a.title.encode("utf-8"), " id: ", a.id, "\n", file=f1)
                print("The same: ", a.title.encode("utf-8"), " id: ", a.id, "\n")
f1.close()

