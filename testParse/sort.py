import datetime
from itertools import chain
import json
from django.core import serializers
from testParse.parse import getAuthors, parse_pages

__author__ = 'user'
from testParse.models import Article, Authors, IdKeyVal
from django.db.models import Count, Min, Max
from django.db.models import Q
from fuzzywuzzy import fuzz


def idSearch(id):
    if id == None:  # If given id even not None(no id in NewArt) -> next filter
        return False
    haveThis = Article.objects.filter(ids__value=id)  # Get queryset
    if not haveThis:  # If it's empty
        return False
    else:
        return haveThis  # Return queryset with this id


def testFilter(obj, qSet):
    tmpDate = obj.pubDate
    titleEn = obj.title
    authList = list()
    for d in Authors.objects.filter(article=obj.id):
        authList.append(d)

    pages = obj.pages

    secondCircle = dateFilter(qSet, tmpDate)

    thirdCircle = authorsFilter(secondCircle, authList)

    forthCircle = pageFilter(thirdCircle, pages)

    fifthCircle = titleFilter(forthCircle, titleEn)

    return fifthCircle


def findDuplicates():
    dateList = list()
    pageList = list()
    authList = list()
    titleList = list()

    allArt = Article.objects.all()

    curDate = allArt.aggregate(Min("pubDate"))["pubDate__min"]
    endDate = allArt.aggregate(Max("pubDate"))["pubDate__max"]

    dateList.append(allArt.filter(pubDate=None))

    dateList.append(allArt.filter(pubDate__range=[curDate, curDate + datetime.timedelta(3 * 365 / 12)]))
    while curDate <= endDate:
        curDate = curDate + datetime.timedelta(3 * 365 / 12)
        newRange = allArt.filter(
            pubDate__range=[curDate, curDate + datetime.timedelta(2 * 365 / 12)])
        dateList.append(newRange)

    dateList = [x for x in dateList if x]

    curPgNum = 1
    interval = 3
    for qSet in dateList:
        endPgNum = qSet.aggregate(Max("pages"))["pages__max"]
        pageList.append(qSet.filter(pages=None))
        pageList.append(qSet.filter(pages__range=[curPgNum, curPgNum + 2]))
        while curPgNum <= endPgNum:
            if curPgNum >= 100:
                interval = 40000
            curPgNum += interval
            newPageRange = qSet.filter(pages__range=[curPgNum, curPgNum + interval])
            pageList.append(newPageRange)
        interval = 3
        curPgNum = 1

    pageList = [x for x in pageList if x]

    curAuthNum = 1
    interval = 3

    for qSet in pageList:
        endAuthNum = qSet.annotate(auth_count=Count('authors')).aggregate(Max("auth_count"))["auth_count__max"]
        newAuthRange = qSet.annotate(auth_count=Count('authors')).filter(auth_count=0)
        authList.append(newAuthRange)

        authList.append(
            qSet.annotate(auth_count=Count('authors')).filter(auth_count__range=[curAuthNum, curAuthNum + interval]))
        while curAuthNum <= endAuthNum:
            curAuthNum += interval
            if curAuthNum >= 50:
                interval = 400
            newAuthRange = qSet.annotate(auth_count=Count('authors')).filter(
                auth_count__range=[curAuthNum, curAuthNum + interval])
            authList.append(newAuthRange)
        interval = 3
        curAuthNum = 1

    for qSet in authList:
        if qSet.count() == 1 or qSet.count() == 0:
            continue
        titleList.append(qSet)

    stats = dict()
    stats["WosScopus"] = 0
    stats["WosSpin"] = 0
    stats["SpinScopus"] = 0
    stats["Triple"] = 0
    stats["Spin"] = 0
    stats["Scopus"] = 0
    stats["Wos"] = 0

    with open("file.json", "w") as out:
        json_serializer = serializers.get_serializer('json')()
        for qSet in titleList:
            for art in qSet:
                sameSet = testFilter(art, art.ArticleSource,
                                     qSet)  # LIST!!!! of same articles. Contains original + copies
                idList = list()
                for x in sameSet:
                    idList.append(x.id)

                try:
                    stats[gainStats(sameSet)] += 1
                except KeyError:
                    pass

                if len(sameSet) > 1:
                    json.dump("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n", out, ensure_ascii=False)
                    json_serializer.serialize(sameSet, stream=out)
                qSet = qSet.exclude(id__in=idList)
        json.dump(stats, out, ensure_ascii=False)


def gainStats(sameQuery):
    if len(sameQuery) == 2:
        if sameQuery[0].ArticleSource == sameQuery[1].ArticleSource:
            return sameQuery[0].ArticleSource
        elif sameQuery[0].ArticleSource == "Wos" and sameQuery[1].ArticleSource == "Spin" or \
                                sameQuery[1].ArticleSource == "Wos" and sameQuery[0].ArticleSource == "Spin":
            return "WosSpin"
        elif sameQuery[0].ArticleSource == "Scopus" and sameQuery[1].ArticleSource == "Spin" or \
                                sameQuery[1].ArticleSource == "Scopus" and sameQuery[0].ArticleSource == "Spin":
            return "SpinScopuus"
        else:
            return "WosScopus"
    elif len(sameQuery) == 3:
        if sameQuery[0].ArticleSource != sameQuery[1].ArticleSource != sameQuery[2].ArticleSource:
            return "Triple"


def filterJdata(object, source):
    for title in object:
        if source == "Wos":
            tmpDate = datetime.datetime.strptime(title["pub_date"], "%Y-%m-%d").date()
            try:
                page_key = title["page_range"]
            except KeyError:
                page_key = None
            titleEn = title["title_en"]
            pages = parse_pages(page_key)

        elif source == "Spin":
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

        elif source == "Scopus":
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

        if isinstance(firstCircle, False):
            firstCircle = Article.objects.filter(ArticleSource=source)

            secondCircle = dateFilter(firstCircle, tmpDate)
            authList = getAuthors(title)
            [thirdCircle, sameCount] = authorsFilter(secondCircle, authList)

            forthCircle = pageFilter(thirdCircle, pages)
            fifthCircle = titleFilter(forthCircle, titleEn)

            return fifthCircle

        else:
            print("There is doi - ", title["doi"])  # debug
            return False


def dateFilter(queryset, pubDate):
    if pubDate is None:
        return queryset
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
        for art in newSet.values():  # Loop for queryset
            sameCount[art["id"]] = 0
            data = Authors.objects.filter(article=art["id"])  # get authors of cur article from queryset
            for auth in authors:  # loop for given authors
                for d in data.values():  # loop for authors from cur article from queryset
                    if d["name"] is not None and auth.name is not None:
                        if d["name"].split(" ", 1)[0] == auth.name.split(" ", 1)[0]:
                            sameCount[art["id"]] += 1
    return newSet


def pageFilter(queryset, pages):
    if pages is None:
        return queryset
    startNum = pages - 1
    endNum = pages + 1
    newSet = queryset.filter(Q(pages__range=[startNum, endNum]) | Q(pages__isnull=True))
    return newSet


def titleFilter(queryset, title):
    my_obj_list = list()
    for data in queryset:
        if fuzz.ratio(title.lower(), data.title.lower()) >= 70:
            my_obj_list.append(data)
    none_qs = Article.objects.none()
    newSet = list(chain(none_qs, my_obj_list))
    return newSet


def isbnFilter(queryset, isbn):
    newSet = queryset.filter(Q(isbn=isbn) | Q(isbn__isnull=True))
    return newSet