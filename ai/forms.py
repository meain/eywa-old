
from django import forms
from .models import Querry

class QuerryForm(forms.ModelForm):
    class Meta:
		model = Querry
		fields = ["querry_term",]
