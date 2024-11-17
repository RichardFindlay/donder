# forms.py
from django import forms

class MountainSearchForm(forms.Form):
    q = forms.CharField(label='', max_length=100)
