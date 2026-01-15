from django.contrib import admin
from .models import book, review

admin.site.register(book)
admin.site.register(review)
