from django import forms

class StockDataForm(forms.Form):
    file = forms.FileField()
