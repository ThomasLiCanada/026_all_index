# websites/forms.py

from django import forms
from .models import *


class InputIndexForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=IndexCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    new_category = forms.CharField(
        max_length=1028,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Select Category above; or Input New Category below:',
    )

    class Meta:
        model = Index
        fields = ['key_words', 'address', 'website_image', 'category']

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')

        if not category and not new_category:
            raise forms.ValidationError('Please select an existing category or input a new one.')

        return cleaned_data


class ToDoTaskForm(forms.ModelForm):
    class Meta:
        model = ToDoTask
        fields = '__all__'
