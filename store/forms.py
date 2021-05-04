from django import forms
from .models import Store, OpenDay


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            'name',
            'description',
            'cnpj'
        ]


class OpenDayForm(forms.ModelForm):
    class Meta:
        model = OpenDay
        fields = [
            'day_of_week'
        ]
