
from django.conf.urls import include, url
from django.views.generic import TemplateView
from products import views


urlpatterns = [

    # Auth views
    url(r'^auth/login/$', views.LoginView.as_view(),
        name='login'),
    url(r'^auth/logout/$', views.get_logout, name='logout'),
    url(r"^auth/register/$", views.RegisterView.as_view(), name='register'),
    url(r"^auth/register/success/$", TemplateView.as_view(
        template_name='products/auth/register_success.html'
    ), name='register_success'),



]
