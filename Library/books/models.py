from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class BookData(models.Model):
    def __str__(self):
        return self.book_title

    book_title = models.CharField(max_length=200, unique=False)
    # book_subject = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    book_publish_date = models.CharField(max_length=200, default=0)
    # book_length = models.CharField(max_length=200)
    book_qt = models.IntegerField(default=0)
    book_ISBN = models.CharField(default=0, max_length=50)


class Order(models.Model):
    def __str__(self):
        return self.book

    user_id = models.IntegerField(default=0)
    book = models.ForeignKey(BookData, null=True, on_delete=models.SET_NULL)
    borrow_date = models.DateTimeField(auto_now=True, null=True)
