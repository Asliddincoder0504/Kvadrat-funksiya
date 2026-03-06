from django import forms

class QuadraticForm(forms.Form):
    a = forms.FloatField(
        label='a',
        widget=forms.NumberInput(attrs={
            'step': 'any',
            'required': True,
            'placeholder': 'masalan: 1 yoki -2.5'
        })
    )
    b = forms.FloatField(
        label='b',
        widget=forms.NumberInput(attrs={
            'step': 'any',
            'required': True,
            'placeholder': 'masalan: -3 yoki 4'
        })
    )
    c = forms.FloatField(
        label='c',
        widget=forms.NumberInput(attrs={
            'step': 'any',
            'required': True,
            'placeholder': 'masalan: 2 yoki -7'
        })
    )