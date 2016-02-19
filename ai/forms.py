
from django import forms

class QuerryForm(forms.Form):
    querry_term = forms.CharField(label='Querry', max_length = 1000)
