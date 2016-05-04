__author__ = 'user'
import testParse.models

def idSearch(id):
    if testParse.Article.objects.filter(doi__exact=id).exists():
        return True
    else:
        return False

def makeKwargs(newObject):
    if newObject.doi = "s":


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