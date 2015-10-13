from django import forms
from django.utils.translation import ugettext_lazy as _
from categories.models import Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from categories.utils import categories_as_choices


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
