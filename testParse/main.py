import glob
import os

__author__ = 'Xerocry'

from testParse.models import Authors, Article
import json
from datetime import datetime, timedelta
import datetime
import time

def scopus_Parse(jdata):
    for title in jdata:
        try:
            tmpDate = datetime.datetime.fromtimestamp(title["pubDate"]/1e3)
        except OSError:
            tmpDate = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(title["pubDate"]/1000))
        newArt = Article.objects.create(pubDate=tmpDate,
                                        scopusIdentifier=(title["scopusIntid"]),
                                        wosUid=title["wosUid"], spinId=title["spinId"],
                                        doi=title["doi"], language=title["language"],
                                        sourceType = title["sourceType"])
        newArt.save()
        for pos, data in title["authors"].items():
            for pos1 in data:

                auth = Authors(name=pos1["name"],
                                       position=pos, scopusId=pos1["scopusId"])
                if not(Authors.objects.filter(name=pos1["name"], scopusId=pos1["scopusId"]).exists()):
                    auth.save()
                    auth.article.add(newArt)

def wos_Parse(jdata):
    for title in jdata:
        # try:
        tmpDate = datetime.datetime.strptime(title["pub_date"], "%Y-%m-%d")
        # except OSError:
        #     tmpDate = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(title["pubDate"]/1000))
        try:
            doi = title["doi"]
        except KeyError:
            doi = None
        try:
            isbn=title["issn"]
        except KeyError:
            isbn = None
        newArt = Article.objects.create(isbn=isbn, wosUid=title["UID"],
                                        doi=doi)
        # newArt.Authors_set.all()
        for auth in title["authors"]:
            newAuth = Authors(name = auth["name"])
            if not(Authors.objects.filter(name=auth["name"]).exists()):
                    newAuth.save()
                    newAuth.article.add(newArt)

def spin_Parse(jdata):
    for title in jdata:
        try:
            tmpDate = datetime.datetime.strptime(title["yearpubl"], "%Y")
        except KeyError:
            tmpDate = None




        # try:
        #     doi = title["codes"]["code"]["text"]
        # except KeyError:
        #     doi = None


        try:
            isbn=title["isbn"]
        except KeyError:
            isbn = None


        if title["language"] == "RU":
            lang = "Russian"
        else:
            lang = "English"
        # newArt = Article.objects.create(isbn=isbn, language=lang,
        #                                 doi=doi)
        # newArt.Authors_set.all()
        # for auth in title["authors"]:
            # newAuth = Authors(name = auth["name"])
            # if not(Authors.objects.filter(name=auth["name"]).exists()):
                    # newAuth.save()
                    # newAuth.article.add(newArt)

for file in glob.iglob('D:/test/**/spin*.json'):
     with open(file, 'r') as data_file:
        jdata = json.load(data_file)
        spin_Parse(jdata)

# for file in glob.iglob('D:/test/**/spin*.json'):
#      with open(file, 'r') as data_file:
#         jdata = json.load(data_file)
#         spin_Parse(jdata)
#
# for file in glob.iglob('D:/test/**/wos*.json'):
#      with open(file, 'r') as data_file:
#         jdata = json.load(data_file)
#         wos_Parse(jdata)
context = {"fields": Article.objects.all()}