from django import forms
from .models import StoryModel

class StoryForm(forms.ModelForm):
    class Meta:
        model = StoryModel
        fields = ('image', )