from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(Saved)
admin.site.register(Liked) 
admin.site.register(Comment)