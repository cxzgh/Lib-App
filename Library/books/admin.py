from django.contrib import admin
from .models import BookData, Order
from django.contrib.auth.models import User


# Register your models here.
class OrderData(admin.ModelAdmin):
    list_display = ('book', 'book_id', 'user_id', 'status')


admin.site.register(BookData)
admin.site.register(Order, OrderData)
