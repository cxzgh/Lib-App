from django import forms
from .models import BookData


class BookDataForm(forms.ModelForm):
    class Meta:
        model = BookData
        fields = ['book_title', 'book_author', 'book_qt', 'book_publish_date', 'book_ISBN']
