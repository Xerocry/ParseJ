from django.db import models

# Create your models here.
class Test(models.Model):
    parent_name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)


class SubTest(models.Model):
    test = models.ForeignKey('Test', related_name='subtest')
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    regression_status = models.CharField(max_length=200)