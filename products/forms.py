
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset
from crispy_forms.bootstrap import PrependedText
from .cache import Item
from .models import Comment, Rate, Category, MyUser
from .utils import categories_as_choices


class MyLoginForm(AuthenticationForm):

    username = forms.CharField(label=_('username'))
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-7'

        self.helper.add_input(Submit('submit', 'Sign In',
                                     css_class='btn btn-default btn-md col-md-offset-5'))

        self.helper.layout = Layout(
            Field(
                'username', placeholder='Input your login'
            ),
            Field(
                'password', placeholder='Input your password'
            )
        )


class MyRegForm(UserCreationForm):
    form_name = 'reg_form'
    error_messages = {
        'password_mismatch': "Passwords mismatch",
    }
    username = forms.CharField(help_text='Max 30 characters')
    password1 = forms.CharField(min_length=6, label=_('password'), widget=forms.PasswordInput,
                                help_text=_("Min 6 characters"))
    password2 = forms.CharField(min_length=6, label=_('password again'),
                                widget=forms.PasswordInput)
    last_name = forms.CharField(max_length=50, label=_('last name'))
    first_name = forms.CharField(max_length=50, label=_('first name'))
    email = forms.EmailField(label=_('Email'), required=True,)

    def __init__(self, *args, **kwargs):
        super(MyRegForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-7'

        self.helper.add_input(Submit('submit', _('Sign Up'),
                                     css_class='btn btn-default btn-md col-md-offset-5'))

    class Meta:
        model = MyUser
        fields = ('last_name', 'first_name', 'username',
                  'email', 'password1', 'password2',)

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


class ModifyItem(forms.ModelForm):
    price = forms.IntegerField(
        max_value=10000000, min_value=0, label=_('Price'))
    description = forms.CharField(
        widget=forms.Textarea, label=_('Description'))

    quantity = forms.IntegerField( min_value=0, label=_('Quantity'))

    def __init__(self, *args, **kwargs):
        super(ModifyItem, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-7'

        self.helper.add_input(Submit('submit', _('Add/edit item'),
                                     css_class='btn btn-default btn-md col-md-offset-5'))

        self.helper.layout = Layout(
            Fieldset(
                'Add item',
                'name',
                'image_url',
                'categories',
                'description',
                'quantity',
            ),
            PrependedText(
                'price', 'грн.'
            ),

        )

    class Meta:
        model = Item
        fields = ('name', 'price', 'image_url', 'categories', 'description', 'quantity')


class AddCategory(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddCategory, self).__init__(*args, **kwargs)
        self.fields['parent_category'].choices = categories_as_choices()
        self.fields['parent_category'].initial = 'default'

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-7'

        self.helper.add_input(Submit('submit', _('Add/edit category'),
                                     css_class='btn btn-default btn-md col-md-offset-5'))

    class Meta:
        model = Category
        fields = ('name', 'parent_category', )

        help_texts = {
            'parent_category': _('Choose parent category if you want.'),
        }

        labels = {
            'parent_category': _('Parent Category'),
        }
