from django.db import models

# Create your models here.
class Scopus(models.Model):
    spinId = models.IntegerField(max_length=200)
    scopusIdentifier = models.IntegerField(max_length=200)
    doi = models.CharField(max_length=200)
    wosUid = models.IntegerField()
    # sourceType = models.CharField(max_length=200) #???
    pubDate = models.DateField()
    language = models.CharField(max_length=200)


class Authors(models.Model):
    article = models.ForeignKey('Article', related_name='authors')
    name = models.CharField(max_length=200, ) #name\initials
    position = models.models.CharField(max_length=200) #student\employee\others


class Wos(models.Model):
    wosId = models.IntegerField(max_length=200)
    pubDate = models.DateField()
    doi = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200)
    language = models.CharField(max_length=200)

class Spin(models.Model):
    doi = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    pubDate = models.DateField()