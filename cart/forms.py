from django import forms
from cart.models import Cart


class AddItemToCart(forms.ModelForm):

    class Meta:
        model = Cart
        fields = ('item', )
