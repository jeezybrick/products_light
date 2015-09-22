__author__ = 'user'
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .cache import Item
from .models import Comment, Rate


class MyLoginForm(AuthenticationForm):

    username = forms.CharField(label=_('username'), max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter username'}))
    password = forms.CharField(label=_("password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter password'}))


class MyRegForm(UserCreationForm):
    form_name = 'reg_form'
    error_messages = {
        'password_mismatch': "Passwords mismatch",
    }
    username = forms.CharField(help_text='Max 30 characters',
                               validators=[
                                   validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
                                   ])
    password1 = forms.CharField(min_length=6, label=_('password'), widget=forms.PasswordInput,
                                help_text=_("Min 6 characters"))
    password2 = forms.CharField(min_length=6, label=_('password again'),
                                widget=forms.PasswordInput)
    last_name = forms.CharField(max_length=50, label=_('last name'))
    first_name = forms.CharField(max_length=50, label=_('first name'))
    email = forms.EmailField(label=_('Email'), required=True,)

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(MyRegForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class AddComment(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, label=_('comment'))

    class Meta:
        model = Comment
        fields = ('username', 'message', )


class AddRate(forms.ModelForm):
    value = forms.IntegerField(max_value=10, min_value=1, label=_('rate item'))

    class Meta:
        model = Rate
        fields = ('value', )


class AddItem(forms.ModelForm):
    price = forms.IntegerField(max_value=10000000, min_value=0, label=_('price'))
    description = forms.CharField(widget=forms.Textarea, label=_('description'))

    class Meta:
        model = Item
        fields = ('name', 'price', 'image_url', 'categories', 'description', )