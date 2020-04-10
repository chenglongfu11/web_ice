from django import forms

class Addfloor_form(forms.Form):
    nfloor = forms.IntegerField(label='Number of floors', required=True)
    cheight = forms.FloatField(label = 'Ceiling heigt is', required=True)
