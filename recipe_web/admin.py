from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Recipe, Comment, Favorite

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Favorite) 
