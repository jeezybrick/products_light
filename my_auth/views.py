from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from products import forms


# For login
class LoginView(View):
    form_class = forms.MyLoginForm
    template_name = 'my_auth/login.html'
    title = _('Sign In')

    def get(self, request):
        form = self.form_class(request)
        context = {
            'form': form,
            'title': self.title,
        }
        return TemplateResponse(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        context = {
            'form': form,
            'title': self.title,
        }
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        return TemplateResponse(request, self.template_name, context)

    def get_success_url(self):
        return reverse("home")


# Registration view
class RegisterView(View):
    form_class = forms.MyRegForm
    template_name = 'my_auth/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('register_success'))
        return render(request, self.template_name, {'form': form})


# logout function
def get_logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("home"))
