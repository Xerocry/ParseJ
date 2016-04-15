from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Authors
from .models import Scopus
from .models import Spin
from .models import Wos

admin.site.register(Wos)
admin.site.register(Spin)
admin.site.register(Scopus)
admin.site.register(Authors)