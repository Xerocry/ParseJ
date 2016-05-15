import datetime
from testParse.dprint import dprint
from testParse.parse import getAuthors

__author__ = 'user'
from testParse.models import Article, Authors, IdKeyVal


def idSearch(id):
    if id == None: #If given id even not None(no id in NewArt) -> next filter
        return False
    haveThis = Article.objects.filter(ids__value=id) #Get queryset
    if not haveThis: #If it's empty
        return False
    else:
        return haveThis #Return queryset with this id


def filter1(object):
    for title in object:
        try: #for different source - diff places of doi
            if isinstance(title["codes"]["code"], dict) and title["codes"]["code"]["type"] == "DOI":
                doi = title["codes"]["code"]["text"]
        except KeyError:
            try:
                doi = title["doi"]
            except KeyError:
                doi = None

        firstCircle = idSearch(doi)

        if type(firstCircle) == type(False):
            print("There is no same doi")
            args = dict()
            if "pub_date" in title:
                pubDate = title["pub_date"]
                # pubDate = dateFilter(firstCircle, title["pub_date"])
            elif "pubDate" in title:
                try:
                    pubDate = datetime.datetime.fromtimestamp(title["pubDate"] / 1e3)
                    # secondCircle = dateFilter(firstCircle, title["pub_date"])
                except OSError:
                    pubDate = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(title["pubDate"] / 1000))
            elif "yearpubl" in title:
                pubDate = datetime.datetime.strptime(title["yearpubl"], "%Y").date()

            firstCircle = Article.objects.filter(ArticleSource="Wos")

            secondCircle = dateFilter(firstCircle, pubDate)
            dprint(secondCircle) #debug
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            authList = getAuthors(title)

            thirdCircle = authorsFilter(secondCircle, authList)
            dprint(thirdCircle)
        else:
            print("There is doi - ", title["doi"]) #debug
            return False


def dateFilter(queryset, pubDate):
    print("DATE: ", datetime.datetime.strptime(pubDate, "%Y-%m-%d").date()) #debug
    startdate = datetime.datetime.strptime(pubDate, "%Y-%m-%d").date() - datetime.timedelta(1*365/12)
    enddate = datetime.datetime.strptime(pubDate, "%Y-%m-%d").date() + datetime.timedelta(1*365/12)
    newSet = queryset.filter(pubDate__range=[startdate, enddate])
    return newSet

def authorsFilter(queryset, authors):
    if len(authors) == 1:
        newSet = queryset.filter(authors__name=authors[0])#Q3
    else:
        sameCount = dict()
        for art in queryset.values():
            for auth in authors:
                if art.object.get(authors__name__exists=auth): #Q2
                    # if :

                    # else:
                    sameCount[art.id] += 1

    return newSet

def pageFilter(queryset, pages):
    print("Page number: ", pages)
    startNum = pages - 1
    endNum = pages+1
    newSet = queryset.filter(pages__range=[startNum, endNum])
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