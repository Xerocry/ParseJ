from django.db import models
from datetime import datetime

# Create your models here.


class Scopus(models.Model):
    spinId = models.IntegerField(null=True)
    scopusIdentifier = models.IntegerField(blank=True, null=True)
    doi = models.CharField(max_length=200, null=True)
    wosUid = models.CharField(max_length=200, null=True)
    sourceType = models.CharField(max_length=200, null=True, default=True)
    pubDate = models.DateField(default=datetime.now, blank=True)
    language = models.CharField(max_length=200, null=True)
    wosId = models.IntegerField(null = True, default=True)
    isbn = models.CharField(max_length=200, null=True)




class Authors(models.Model):
    article = models.ForeignKey('Scopus', related_name='Authors')
    name = models.CharField(max_length=200, )
    position = models.CharField(max_length=200)