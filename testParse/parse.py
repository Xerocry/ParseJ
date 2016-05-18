import datetime
from pprint import pprint
import re
import string
from testParse import dprint
from testParse.models import Article, Authors, IdKeyVal


class Author:
    pos = "This shape has not been described yet"
    id = list()
    name = "Nobody has claimed to make this shape yet"

    # def __init__(self, name, pos, id):
    # self.name = name
    #     self.pos = pos
    #     self.id = id

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def getPos(self):
        return self.pos

    def setPos(self, text):
        self.pos = text

    def setId(self, id):
        self.id.append(id)

    def setName(self, text):
        self.name = text


class Del:
    def __init__(self, keep=string.digits):
        self.comp = dict((ord(c), c) for c in keep)

    def __getitem__(self, k):
        return self.comp.get(k)


def getAuthors(title):
    authList = list()
    try:
        for pos, data in title["authors"].items():  # Scopus
            for pos1 in data:
                newAuth = Author()
                newAuth.setName(pos1["name"])
                newAuth.setId(pos1["scopusId"])
                newAuth.setId(pos1["researcherId"])
                newAuth.setId(pos1["spinAuthorId"])
                newAuth.setPos(pos)
                authList.append(newAuth)
    except AttributeError:
        try:  # Wos
            for auth in title["authors"]:
                newAuth = Author()
                newAuth.setName(auth["name"])
                try:
                    newAuth.setId(auth["researcher_id"])
                except KeyError:
                    pass
                authList.append(newAuth)
        except KeyError:  # Spin
            for auth1 in title["authors"]["author"]:
                if isinstance(auth1, dict):
                    newAuth = Author()
                    try:
                        newAuth.setName(auth1["lastname"] + " " + auth1["initials"])
                    except KeyError:
                        newAuth.setName(auth1["lastname"])
                    authList.append(newAuth)
                else:
                    newAuth = Author()
                    try:
                        newAuth.setName(
                            title["authors"]["author"]["lastname"] + " " + title["authors"]["author"]["initials"])
                    except KeyError:
                        newAuth.setName(title["authors"]["author"]["lastname"])
                    authList.append(newAuth)
    return authList


def scopus_Parse(jdata):
    for title in jdata:
        try:
            tmpDate = datetime.datetime.fromtimestamp(title["pubDate"] / 1e3)
        except OSError:
            tmpDate = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(title["pubDate"] / 1000))
        try:
            pages = title["pageRange"]
        except KeyError:
            pages = None

        newArt = Article.objects.create(ArticleSource="Scopus", pubDate=tmpDate,
                                        language=title["language"],
                                        sourceType=title["sourceType"], pages=parse_pages(pages),
                                        title=title["titleEn"])
        newArt.save()

        try:
            scopId = title["scopusIntid"]
            if not (scopId is None):
                IdKeyVal.objects.create(article=newArt, key="scopusId", value=scopId)
        except KeyError:
            pass

        try:
            doi = title["doi"]
            if not (doi is None):
                IdKeyVal.objects.create(article=newArt, key="doi", value=doi)
        except KeyError:
            pass

        try:
            spinId = title["spinId"]
            if not (spinId is None):
                IdKeyVal.objects.create(article=newArt, key="spinId", value=spinId)
        except KeyError:
            pass

        try:
            wosId = title["wosUid"]
            if not (wosId is None):
                wosId = wosId.replace('WOS:', '')
                IdKeyVal.objects.create(article=newArt, key="wosUid", value=wosId)
        except KeyError:
            pass

        for pos, data in title["authors"].items():
            for pos1 in data:
                # try:
                #     id = pos1["researcherId"]
                # except KeyError:
                #     id = None

                auth = Authors(name=pos1["name"],
                               position=pos, scopusId=pos1["scopusId"], spinId=pos1["spinAuthorId"], researcherid=pos1["researcherId"])

                if not (Authors.objects.filter(name=pos1["name"], scopusId=pos1["scopusId"],
                                               spinId=pos1["spinAuthorId"], researcherid=pos1["researcherId"]).exists()):
                    auth.save()
                    auth.article.add(newArt)


def wos_Parse(jdata):
    for title in jdata:
        tmpDate = datetime.datetime.strptime(title["pub_date"], "%Y-%m-%d").date()

        try:
            lang = title["static_data"]["fullrecord_metadata"]["languages"]["language"]["text"]
        except:
            lang = None

        try:
            isbn = title["issn"]
        except KeyError:
            isbn = None

        try:
            pages = title["page_range"]
        except KeyError:
            pages = None

        newArt = Article.objects.create(ArticleSource="Wos", isbn=isbn, pubDate=tmpDate, pages=parse_pages(pages),
                                        language=lang, title=title["title_en"])

        try:
            doi = title["doi"]
            IdKeyVal.objects.create(article=newArt, key="doi", value=doi)
        except KeyError:
            pass

        try:
            wosId = title["UID"]
            if not (wosId is None):
                wosId = wosId.replace('WOS:', '')
                IdKeyVal.objects.create(article=newArt, key="wosUid", value=wosId)
        except KeyError:
            pass

        for auth in title["authors"]:
            try:
                id = auth["researcher_id"]
            except KeyError:
                id = None
            newAuth = Authors(name=auth["name"], researcherid=id)
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
            else:
                doi = None
        except KeyError:
            doi = None

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

        try:
            if isinstance(title["titles"]["title"], list):
                # print(title["titles"]["title"])
                titleEn = title["titles"]["title"][0]["text"]
            else:
                titleEn = title["titles"]["title"]["text"]
        except KeyError:
            titleEn = None


        newArt = Article.objects.create(ArticleSource="Spin", isbn=isbn, language=lang, pubDate=tmpDate, pages=pages,
                                        title=titleEn)
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
    if str is None:
        return
    DD = Del()
    newStr = str.split("-")
    if len(newStr) > 1:
        try:
            newStr[0] = newStr[0].translate(DD)
            newStr[1] = newStr[1].translate(DD)
            return int(newStr[1]) - int(newStr[0])
        except ValueError:
            return roman_to_arabic(newStr[1]) - roman_to_arabic(newStr[0])
    else:
        return 1

rule_add = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000,
}

rule_div = {
    ('I', 'V'): 3,
    ('I', 'X'): 8,
    ('X', 'L'): 30,
    ('X', 'C'): 80,
    ('C', 'D'): 300,
    ('C', 'M'): 800,
}


def roman_to_arabic(roman_number):
    number = 0
    prev_literal = None
    for literal in roman_number:
        if prev_literal and rule_add[prev_literal] < rule_add[literal]:
            number += rule_div[(prev_literal, literal)]
        else:
            number += rule_add[literal]
        prev_literal = literal
    return number