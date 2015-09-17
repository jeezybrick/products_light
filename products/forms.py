__author__ = 'user'
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from .cache import Item
from .models import Comment, Rate


class MyLoginForm(AuthenticationForm):

    username = forms.CharField(label='Логин', max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Введите ваш логин'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Введите ваш пароль'}))


class MyRegForm(UserCreationForm):
    form_name = 'reg_form'
    error_messages = {
        'password_mismatch': "Пароли не совпадают!",
    }
    username = forms.CharField(help_text='Максимум 30 символов',
                               validators=[
                                   validators.RegexValidator(r'^[\w.@+-]+$',
                                                             'Введите правильный логин. '
                                                             'Логин может состоять из букв,цифр'
                                                             'и  @/./+/-/_ символов.',
                                                             'invalid'),
                                   ],
                               error_messages={'required': 'Это поле обязательное к запонению',
                                               'unique': 'Пользователь с таким логином уже существует'}
                               )
    password1 = forms.CharField(min_length=6, label='Пароль', widget=forms.PasswordInput,
                                help_text="Минимум 6 символов",)
    password2 = forms.CharField(min_length=6, label='Введите пароль еще раз',
                                help_text="Введите повторно пароль для проверки",
                                widget=forms.PasswordInput)
    last_name = forms.CharField(max_length=50, label='Фамилия',
                                error_messages={'required': 'Это поле обязательное к запонению'})
    first_name = forms.CharField(max_length=50, label='Имя',
                                 error_messages={'required': 'Это поле обязательное к запонению'})
    email = forms.EmailField(label='Email', required=True,
                             error_messages={'unique': 'Пользователь с таким email уже существует'})

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
    message = forms.CharField(widget=forms.Textarea, label='Ваш комментарий')

    class Meta:
        model = Comment
        fields = ('username', 'message', )


class AddRate(forms.ModelForm):
    value = forms.IntegerField(max_value=10, min_value=1, label='Ваша оценка товару')

    class Meta:
        model = Rate
        fields = ('value', )


class AddItem(forms.ModelForm):
    price = forms.IntegerField(max_value=10000000, min_value=0, label='Цена')
    description = forms.CharField(widget=forms.Textarea, label='Описание товара')

    class Meta:
        model = Item
        fields = ('name', 'price', 'image_url', 'categories', 'description', )