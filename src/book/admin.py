from django.contrib import admin

from .models import Book, Test, SpecifyBook, CommentBook, Category
# Register your models here.

admin.site.register(Book)
# admin.site.register(Test)
admin.site.register(SpecifyBook)
admin.site.register(CommentBook)
admin.site.register(Category)
