from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Authors
from .models import Article


admin.site.register(Article)
admin.site.register(Authors)