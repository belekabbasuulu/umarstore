from django import forms
from django.forms import NumberInput


class CartAddProductForm(forms.Form):

    quantity = forms.IntegerField(
        min_value=1,
        widget=NumberInput(attrs={
            'class': 'form-control text-center px-3',
            'value': 1
        }))

    CHOICES = (
        (35, 35),
        (36, 36),
        (37, 37),
        (38, 38),
        (39, 39),
        (40, 40),
        (41, 41),
        (42, 42),
        (43, 43),
    )
    size = forms.IntegerField(
        widget=forms.Select(
            choices=CHOICES,
            attrs={'style': "border: none; margin-left: 1.5rem;"}
        ),

    )
