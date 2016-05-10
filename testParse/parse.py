import datetime
from pprint import pprint
import re
import string
from testParse import dprint
from testParse.models import Article, Authors, IdKeyVal


class Del:
    def __init__(self, keep=string.digits):
        self.comp = dict((ord(c), c) for c in keep)

    def __getitem__(self, k):
        return self.comp.get(k)


def scopus_Parse(jdata):
    for title in jdata:
        try:
            tmpDate = datetime.datetime.fromtimestamp(title["pubDate"] / 1e3)
        except OSError:
            tmpDate = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(title["pubDate"] / 1000))
        newArt = Article.objects.create(ArticleSource="Scopus", pubDate=tmpDate,
                                        language=title["language"],
                                        sourceType=title["sourceType"])
        newArt.save()

        try:
            scopId = title["scopusIntid"]
            if not(scopId is None):
                IdKeyVal.objects.create(article=newArt, key="scopusId", value=scopId)
        except KeyError:
            pass

        try:
            doi = title["doi"]
            if not(doi is None):
                IdKeyVal.objects.create(article=newArt, key="doi", value=doi)
        except KeyError:
            pass

        try:
            spinId = title["spinId"]
            if not(spinId is None):
                IdKeyVal.objects.create(article=newArt, key="spinId", value=spinId)
        except KeyError:
            pass

        try:
            wosId = title["wosUid"]
            if not(wosId is None):
                wosId = wosId.replace('WOS:', '')
                IdKeyVal.objects.create(article=newArt, key="wosUid", value=wosId)
        except KeyError:
            pass

        for pos, data in title["authors"].items():
            for pos1 in data:

                auth = Authors(name=pos1["name"],
                               position=pos, scopusId=pos1["scopusId"])
                if not (Authors.objects.filter(name=pos1["name"], scopusId=pos1["scopusId"]).exists()):
                    auth.save()
                    auth.article.add(newArt)


def wos_Parse(jdata):
    for title in jdata:
        tmpDate = datetime.datetime.strptime(title["pub_date"], "%Y-%m-%d").date()

        try:
            isbn = title["issn"]
        except KeyError:
            isbn = None

        newArt = Article.objects.create(ArticleSource="Wos", isbn=isbn, pubDate=tmpDate)

        try:
            doi = title["doi"]
            IdKeyVal.objects.create(article=newArt, key="doi", value=doi)
        except KeyError:
            pass

        try:
            wosId = title["UID"]
            if not(wosId is None):
                wosId = wosId.replace('WOS:', '')
                IdKeyVal.objects.create(article=newArt, key="wosUid", value=wosId)
        except KeyError:
            pass

        for auth in title["authors"]:
            newAuth = Authors(name=auth["name"])
            if not (Authors.objects.filter(name=auth["name"]).exists()):
                newAuth.save()
                newAuth.article.add(newArt)


def spin_Parse(jdata):
    for title in jdata:
        try:
            tmpDate = datetime.datetime.strptime(title["yearpubl"], "%Y").date()
        except KeyError:
            tmpDate = None

        try:
            if isinstance(title["codes"]["code"], dict) and title["codes"]["code"]["type"] == "DOI":
                doi = title["codes"]["code"]["text"]
                # print(title["codes"]["code"])
            else:
                doi = None
        except KeyError:
            doi = None

        # print(title["codes"]["code"])

        if "pages" in title:
            page_key = "pages"
        elif "pagesnumber" in title:
            page_key = "pagesnumber"

        try:
            pages = parse_pages(title[page_key])
        except KeyError:
            pages = None

        try:
            isbn = title["isbn"]
        except KeyError:
            isbn = None

        if title["language"] == "RU":
            lang = "Russian"
        else:
            lang = "English"

        newArt = Article.objects.create(ArticleSource="Spin", isbn=isbn, language=lang, pubDate=tmpDate, pages=pages)
        for auth1 in title["authors"]["author"]:
            if isinstance(auth1, dict):
                try:
                    newAuth = Authors(name=auth1["lastname"] + " " + auth1["initials"])
                except KeyError:
                    newAuth = Authors(name=auth1["lastname"])
            else:
                try:
                    newAuth = Authors(
                        name=(title["authors"]["author"]["lastname"] + " " + title["authors"]["author"]["initials"]))
                except KeyError:
                    newAuth = Authors(name=(title["authors"]["author"]["lastname"]))

            if not (Authors.objects.filter(name=newAuth.name).exists()):
                newAuth.save()
                newAuth.article.add(newArt)

        if not (doi is None):
            newId = IdKeyVal(article=newArt, key="doi", value=doi)
            newId.save()


def parse_pages(str):
    DD = Del()
    newStr = str.split("-")
    if len(newStr) > 1:
        newStr[0] = newStr[0].translate(DD)
        newStr[1] = newStr[1].translate(DD)
        return int(newStr[1]) - int(newStr[0])
    else:
        return 1