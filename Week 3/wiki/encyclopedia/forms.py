from logging import PlaceHolder
from django import forms
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Title", 'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Input Markdown Text Here", 'class': 'form-control'}))