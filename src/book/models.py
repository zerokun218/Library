from django.db import models
from django.utils import timezone
from datetime import date,timedelta

from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    class Meta:
        unique_together = ('name',)
        ordering = ['name']
    def __str__(self):
        return str(self.name)

class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ManyToManyField(Category)
    url = models.URLField(blank=True, null=True)
    image   = models.ImageField(upload_to='image/', blank=True, null=True)
    description = models.TextField()
    publish_time = models.DateTimeField(default = timezone.now, null=True)
    update_time = models.DateTimeField(auto_now=True)

    amount = models.IntegerField(default=5)
    class Meta:
        ordering = ['-update_time', 'name','author']
        unique_together = ('name','author')


    def __str__(self):
        return self.name

class Test(models.Model):
    name = models.CharField(max_length=255, blank = True, null = True)
    created_time = models.DateTimeField(auto_now_add = True)
    update_time = models.DateTimeField(auto_now=True)
    date_create = models.DateField(default = date.today)


class SpecifyBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_time = models.DateField(default=date.today)
    charge_time = models.DateField(default=date.today)
    is_charge = models.BooleanField(default = False)
    state = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{0}-{1}'.format(self.user.username, self.book.name)


class CommentBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-comment_time']
        unique_together = ('user','book','comment_time')

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.user.username, self.book.name, self.id)
