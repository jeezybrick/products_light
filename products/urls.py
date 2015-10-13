
from django.conf.urls import include, url
from django.views.generic import TemplateView
from products import views


urlpatterns = [
    # Home view
    url(r"^$", TemplateView.as_view(
        template_name='products/home.html'
    ), name='home'),

    # Auth views
    url(r'^auth/login/$', views.LoginView.as_view(),
        name='login'),
    url(r'^auth/logout/$', views.get_logout, name='logout'),
    url(r"^auth/register/$", views.RegisterView.as_view(), name='register'),
    url(r"^auth/register/success/$", TemplateView.as_view(
        template_name='products/auth/register_success.html'
    ), name='register_success'),

    # Django views
    url(r"^shops/$", views.ShopListView.as_view(), name='shop_list'),
    url(r"^shops/(?P<pk>\w+)/$", views.ShopDetailView.as_view(), name='shop_detail'),

    url(r"^products/$", views.ItemListView.as_view(), name='products_list'),
    url(r"^products/add/$", views.ItemAddView.as_view(), name='products_add'),
    url(r"^products/(?P<pk>\w+)/$",
        views.ItemDetailView.as_view(), name='products_show'),
    url(r"^products/(?P<pk>\w+)/edit/$",
        views.ItemEditView.as_view(), name='products_edit'),
    url(r"^products/(?P<pk>\w+)/delete/$",
        views.ItemDeleteView.as_view(), name='products_delete'),
    url(r"^products/(?P<pk>\w+)/action/$",
        views.ItemActionView.as_view(), name='products_action'),

    url(r"^products/(?P<pk>\w+)/comments/add/$",
        views.AddCommentView.as_view(), name='comment_add'),
    url(r"^products/(?P<pk>\w+)/rates/add/$",
        views.AddRateView.as_view(), name='rate_add'),


    # Angular views
    url(r"^products_ang/$", TemplateView.as_view(
        template_name='api/products/index.html'
    ), name='products_list_ang'),
    url(r"^products_ang/show/$", TemplateView.as_view(
        template_name='api/products/show.html'
    ), name='products_detail_ang'),
    url(r"^products_ang/edit/$", TemplateView.as_view(
        template_name='api/products/modify.html'
    ), name='products_edit_ang'),
    url(r"^products_ang/action/add/$", TemplateView.as_view(
        template_name='api/action/action_form.html'
    ), name='products_action_add_ang'),
    url(r"^categories_ang/$", TemplateView.as_view(
        template_name='api/categories/index.html'
    ), name='categories_list_ang'),


    # Haystack search
    url(r'^search/', include('haystack.urls')),


]
