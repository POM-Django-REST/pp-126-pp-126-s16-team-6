from django import forms
from .models import Book


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'count', 'author', 'publication_year', 'issue_date', 'description']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'})
        }


class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'count', 'author', 'publication_year', 'issue_date', 'description']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'})
        }