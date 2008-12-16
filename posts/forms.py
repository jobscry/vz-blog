from django import forms
from django.forms import ModelForm
from models import Post

class SearchForm(forms.Form):
	search_string = forms.CharField(max_length=100, label='Look for')
