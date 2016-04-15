from django.db import models

# Create your models here.


class Scopus(models.Model):
    spinId = models.IntegerField()
    scopusIdentifier = models.IntegerField()
    doi = models.CharField(max_length=200)
    wosUid = models.IntegerField()
    # sourceType = models.CharField(max_length=200) #???
    pubDate = models.DateField()
    language = models.CharField(max_length=200)


class Authors(models.Model):
    article = models.ForeignKey('Scopus', related_name='Authors')
    name = models.CharField(max_length=200, )
    position = models.CharField(max_length=200)


class Wos(models.Model):
    wosId = models.IntegerField()
    pubDate = models.DateField()
    doi = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200)
    language = models.CharField(max_length=200)


class Spin(models.Model):
    doi = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    pubDate = models.DateField()