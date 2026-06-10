from django import forms
from .models import DietProfile

class DietProfileForm(forms.ModelForm):
    class Meta:
        model = DietProfile
        fields = ['age', 'gender', 'height', 'weight', 'goal']