import datetime
from testParse.dprint import dprint

__author__ = 'user'
from testParse.models import Article, Authors, IdKeyVal


def idSearch(id):
    haveThis = Article.objects.filter(ids__value=id)
    if not haveThis:
        return False
    else:
        return haveThis


def filter1(object):
    for title in object:
        firstCircle = idSearch(title["doi"])
        if type(firstCircle) == type(False):
            print("There is no same doi")
            args = dict()
            if "pub_date" in title:
                args["pubDate"] = title["pub_date"]
            elif "pubDate" in title:
                try:
                    args["pubDate"] = datetime.datetime.fromtimestamp(title["pubDate"] / 1e3)
                except OSError:
                    args["pubDate"] = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(title["pubDate"] / 1000))
            elif "yearpubl" in title:
                args["pubDate"] = datetime.datetime.strptime(title["yearpubl"], "%Y").date()

            
            firstCircle = Article.objects.filter(ArticleSource="Wos")

            secondCircle = filter2(firstCircle, title["pub_date"])
            dprint(secondCircle)
        else:
            print("There is doi - ", title["doi"])
            return False
            # dprint(trying)
            # return True


def filter2(queryset, pubDate):
    for article in queryset.values():
        print("DATE: ", datetime.datetime.strptime(pubDate, "%Y-%m-%d").date())
        startdate = article["pubDate"] - datetime.timedelta(1*365/12)
        enddate = startdate + datetime.timedelta(1*365/12)
        newSet = queryset.filter(pubDate__range=[startdate, enddate])
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