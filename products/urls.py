__author__ = 'user'


from django.conf.urls import include, url
from django.views.generic import ListView, DetailView, TemplateView
from .forms import MyLoginForm
from .models import Item, Category
from products import views


urlpatterns = [
    url(r"^$", TemplateView.as_view(
        template_name='products/home.html'
    ), name='home'),
    url(r'^auth/login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'products/auth/login.html',
            'authentication_form': MyLoginForm,
            'extra_context':
            {
                'title': 'Вход пользователя',
            }
        },
        name='login'),
    url(r'^auth/logout/$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),
    url(r"^auth/register/$", views.RegisterView.as_view(), name='register'),
    url(r"^auth/register/success/$", TemplateView.as_view(
        template_name='products/auth/register_success.html'
    ), name='register_success'),
    url(r"^products/$", views.ItemListView.as_view(), name='products_list'),
    url(r"^products/add/$", views.ItemAddView.as_view(), name='products_add'),
    url(r"^products/(?P<pk>\w+)/$", views.ItemDetailView.as_view(), name='products_show'),
    url(r"^products/(?P<pk>\w+)/comments/add/$", views.AddCommentView.as_view(), name='comment_add'),
    url(r"^products/(?P<pk>\w+)/rates/add/$", views.AddRateView.as_view(), name='rate_add'),
    url(r"^categories/add/$", views.CategoryAddView.as_view(), name='categories_add'),
    url(r"^categories/$", views.CategoryListView.as_view(), name='categories_list'),
    url(r'^search/', include('haystack.urls')),


    ]

