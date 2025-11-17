from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=255)
    author = forms.CharField(max_length=255)
    published_date = forms.DateField(required=False)
