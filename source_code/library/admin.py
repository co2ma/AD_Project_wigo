from django.contrib import admin
from .models import Book, BorrowHistory

# Register your models here.
admin.site.register(Book)
admin.site.register(BorrowHistory)
