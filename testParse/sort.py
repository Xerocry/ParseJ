import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
from testParse.dprint import dprint
from testParse.parse import getAuthors, parse_pages

__author__ = 'user'
from testParse.models import Article, Authors, IdKeyVal
from django.db.models import Count
from django.db.models import Q


def idSearch(id):
    if id == None:  # If given id even not None(no id in NewArt) -> next filter
        return False
    haveThis = Article.objects.filter(ids__value=id)  # Get queryset
    if not haveThis:  # If it's empty
        return False
    else:
        return haveThis  # Return queryset with this id


def filter1(object, source):
    for title in object:
        if (source == "Wos"):
            tmpDate = datetime.datetime.strptime(title["pub_date"], "%Y-%m-%d").date()
            try:
                page_key = title["page_range"]
            except KeyError:
                page_key = None
            titleEn = title["title_en"]
            pages = parse_pages(page_key)

        elif (source == "Spin"):
            try:
                tmpDate = datetime.datetime.strptime(title["yearpubl"], "%Y").date()
            except KeyError:
                tmpDate = None

            if "pages" in title:
                page_key = "pages"
            elif "pagesnumber" in title:
                page_key = "pagesnumber"

            try:
                if isinstance(title["titles"]["title"], list):
                    titleEn = title["titles"]["title"][0]["text"]
                else:
                    titleEn = title["titles"]["title"]["text"]
            except KeyError:
                titleEn = None

            try:
                pages = parse_pages(title[page_key])
            except KeyError:
                pages = None

        elif (source == "Scopus"):
            try:
                tmpDate = datetime.datetime.fromtimestamp(title["pubDate"] / 1e3)
            except OSError:
                tmpDate = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(title["pubDate"] / 1000))

            try:
                page_key = title["pageRange"]
            except KeyError:
                page_key = None
            titleEn = title["titleEn"]
            pages = parse_pages(page_key)

        try:  # for different source - diff places of doi
            if isinstance(title["codes"]["code"], dict) and title["codes"]["code"]["type"] == "DOI":
                doi = title["codes"]["code"]["text"]
        except KeyError:
            try:
                doi = title["doi"]
            except KeyError:
                doi = None

        firstCircle = idSearch(doi)

        if type(firstCircle) == type(False):
            # firstCircle = Article.objects.filter(ArticleSource="Scopus")
            firstCircle = Article.objects.all()

            secondCircle = dateFilter(firstCircle, tmpDate)
            # dprint(secondCircle) #debug
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            authList = getAuthors(title)
            [thirdCircle, sameIdCount, sameCount] = authorsFilter(secondCircle, authList)

            # dprint(thirdCircle)
            forthCircle = pageFilter(thirdCircle, pages)
            print("~~~~~~~~~~+++++++++++++~~~~~~~~~~~~~~")
            dprint(forthCircle)
            fifthCircle = titleFilter(forthCircle, titleEn)

            print("~~~~~~~~~~+++++++++++++~~~~~~~~~~~~~~")
            dprint(fifthCircle)

        else:
            print("There is doi - ", title["doi"])  # debug
            return False


def dateFilter(queryset, pubDate):
    print("DATE: ", pubDate)  # debug
    startdate = pubDate - datetime.timedelta(1 * 365 / 12)
    enddate = pubDate + datetime.timedelta(1 * 365 / 12)
    newSet = queryset.filter(Q(pubDate__range=[startdate, enddate]) | Q(pubDate__isnull=True))
    return newSet


def authorsFilter(queryset, authors):
    if len(authors) == 1:
        newSet = queryset.filter(authors__name=authors[0])
    else:
        newSet = queryset.annotate(auth_count=Count('authors')).filter(auth_count__exact=len(authors))
        sameCount = dict()
        sameIdCount = dict()
        for art in newSet.values():  # Loop for queryset
            sameIdCount[art["id"]] = 0
            sameCount[art["id"]] = 0
            data = Authors.objects.filter(article=art["id"])  # get authors of cur article from queryset
            for auth in authors:  # loop for given authors
                for d in data.values():  # loop for authors from cur article from queryset
                    if d["name"].split(" ", 1)[0] == auth.name.split(" ", 1)[0]:
                        if not (d["scopusId"] == 1) or not (d["researcherid"] == None) or not (d["spinId"] == None):
                            if d["scopusId"] in auth.getId() or d["resarcherid"] in auth.getId():
                                sameIdCount[art["id"]] += 1
                        else:
                            sameCount[art["id"]] += 1
                            # print("SameId = ", sameIdCount[art["id"]], " / Same = ", sameCount[art["id"]])
    return [newSet, sameCount, sameIdCount]


def pageFilter(queryset, pages):
    print("Page number: ", pages)
    startNum = pages - 1
    endNum = pages + 1
    newSet = queryset.filter(Q(pages__range=[startNum, endNum]) | Q(pages__isnull=True))
    return newSet


def titleFilter(queryset, title):
    print("Article Title: ", title)
    newSet = queryset.filter(title=title)  # Add lowercase and fuzzy search
    # print(title.lower())
    return newSet


# May be deleted
def isbnFilter(queryset, isbn):
    print("ISBN", isbn)
    newSet = queryset.filter(Q(isbn=isbn) | Q(isbn__isnull=True))
    return newSet


"""
if there is doi -> check only for doi
else
    1)see from what source and check id of this source
        if newArt has id in that source
            Check in db for this id
    2)See publication date. Form range +-month. Put all articles from db in that range into new queryset
    3)See authors.
        If NewArt has one author
            form new query with articles by same authors
        else
            Count number of same authors(by name + surname)
            Check for id(only if it exists)
            if >= 1 form new query
    4)Check for page numbers
        If new >> or << then example from query - not the same
        For others form new query
    5)Check for title?!?
    6)Check for isbn?!?
"""