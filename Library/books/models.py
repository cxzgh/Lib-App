import datetime
from django.db import models


# Create your models here.

class BookData(models.Model):
    def __str__(self):
        return self.book_title

    book_title = models.CharField(max_length=200, unique=False)
    book_author = models.CharField(max_length=200)
    book_publish_date = models.CharField(max_length=200, default=0)
    book_length = models.CharField(max_length=200, default=0)
    book_qt = models.IntegerField(default=0)
    book_ISBN = models.CharField(default=0, max_length=50)
    book_description = models.TextField(max_length=4000, default='No Description')

class Order(models.Model):
    def __str__(self):
        return self.book.book_title

    STATUS = (
        ('active', 'active'),
        ('returned', 'returned'),
    )

    user_id = models.IntegerField(default=0)
    book = models.ForeignKey(BookData, null=True, on_delete=models.SET_NULL)
    borrow_date = models.DateTimeField(auto_now=True, null=True)
    borrow_due = models.DateTimeField(null=True, default=datetime.datetime.now() + datetime.timedelta(days=10))
    status = models.CharField(max_length=10, default='active', choices=STATUS)


class Log(models.Model):
    def __str__(self):
        return self.order

    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    user_id = models.IntegerField(default=0)
    book_id = models.IntegerField(default=0)
    borrow_date = models.CharField(max_length=200)
    borrow_due = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True, null=True)

