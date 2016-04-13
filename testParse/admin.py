from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Test
from .models import SubTest

admin.site.register(Test)
admin.site.register(SubTest)