from django.shortcuts import render

# Create your views here.
from django.views import generic
from testParse.models import Test, SubTest
import json

__author__ = 'Xerocry'

class IndexView(generic.ListView):
    with open('D:/scopus_test.json') as data_file:
        jdata = json.load(data_file)

    for title in jdata['data']:
        # Test.objects.create(id=title['id'], name=title['name'])
        Test.objects.create(parent_name=title['model'], category=title['category'])

    context = {'titles': Test.objects.all()}