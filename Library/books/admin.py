from django.contrib import admin
from .models import BookData, Order

# Register your models here.
admin.site.register(BookData)
admin.site.register(Order)
