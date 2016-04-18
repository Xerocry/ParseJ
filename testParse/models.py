from django.db import models
from datetime import datetime
from testParse import managers

# Create your models here.

# class AuthManager(models.Manager):


class Article(models.Model):
    spinId = models.IntegerField(null=True)
    scopusIdentifier = models.IntegerField(blank=True, null=True)
    doi = models.CharField(max_length=200, null=True)
    wosUid = models.CharField(max_length=200, null=True)
    sourceType = models.CharField(max_length=200, null=True)
    pubDate = models.DateField(default=datetime.now, blank=True, null=True)
    language = models.CharField(max_length=200, null=True)
    isbn = models.CharField(max_length=200, null=True)
    # Meta and String



class Authors(models.Model):
    article = models.ManyToManyField(Article, related_name='authors')
    scopusId = models.BigIntegerField(null = True, default=True)
    name = models.CharField(max_length=200, null = True)
    position = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "%s - %s" % (self.article, self.name)