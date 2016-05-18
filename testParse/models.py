from django.db import models
from datetime import datetime

# Create your models here.

# class AuthManager(models.Manager):


class Article(models.Model):
    ArticleSource = models.CharField(max_length=200, null=True)  # scopus - wos - spin
    # spinId = models.IntegerField(null=True)
    # scopusIdentifier = models.IntegerField(blank=True, null=True)
    # doi = models.CharField(max_length=200, null=True)
    # wosUid = models.CharField(max_length=200, null=True)
    sourceType = models.CharField(max_length=200, null=True)
    pubDate = models.DateField(default=datetime.now, blank=True, null=True)
    language = models.CharField(max_length=200, null=True)
    isbn = models.CharField(max_length=200, null=True)
    pages = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=500, null=True)
    # Meta and String


class IdKeyVal(models.Model):
    article = models.ForeignKey(Article, related_name='ids', db_index=True)
    key = models.CharField(max_length=240, db_index=True)
    value = models.CharField(max_length=240, db_index=True)


class Authors(models.Model):
    article = models.ManyToManyField(Article, related_name='authors')
    scopusId = models.BigIntegerField(null=True, default=True)
    spinId = models.CharField(max_length=200, null=True)
    researcherid = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    position = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "%s - %s" % (self.article, self.name)