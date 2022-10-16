from . import views
from django.urls import path

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('add/', views.add_book, name='add_book'),
    path('add_confirmation/', views.add_confirm, name='confirm'),
    path('librarian/', views.librarian, name='librarian_page'),
    path('delete/<int:id>/', views.delete_book, name='delete'),
    path('edit/<int:id>/', views.edit_book, name='edit'),
    path('borrow/<int:id>', views.borrow_book, name='borrow'),
    path('out_of_order', views.out_of_order, name='out_of_order'),
    path('details/<int:id>', views.details, name='details'),
]