from django import forms
from .models import BookData


class BookDataForm(forms.ModelForm):
    class Meta:
        model = BookData
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book_title'].widget.attrs.update({'class': 'input-group-text table-add-input'})
        self.fields['book_author'].widget.attrs.update({'class': 'input-group-text table-author-input'})
        self.fields['book_publish_date'].widget.attrs.update({'class': 'input-group-text'})
        self.fields['book_length'].widget.attrs.update({'class': 'input-group-text'})
        self.fields['book_qt'].widget.attrs.update({'class': 'input-group-text qt-add-input'})
        self.fields['book_ISBN'].widget.attrs.update({'class': 'input-group-text'})
        self.fields['book_description'].widget.attrs.update({'class': 'input-group-text description-add-input'})
        self.fields['book_description'].widget.attrs.update({'rows': 5, 'cols': 5})

