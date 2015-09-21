__author__ = 'user'

from django.conf.urls import include, url
from rest_framework import routers
from .serializers import UserViewSet, ItemViewSet, CategoryViewSet, CommentViewSet, RateViewSet
from django.views.generic import ListView, DetailView, TemplateView
from api import views

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'items', ItemViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'rates', RateViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/items/$', views.ItemList.as_view(), name='item-list'),
    url(r'^api/items/(?P<pk>[0-9]+)/$', views.ItemDetail.as_view(), name='item-detail'),
    url(r"^products_ang/$", TemplateView.as_view(
        template_name='api/products/index.html'
    ), name='products_list_ang'),
    url(r"^products_ang_test/$", TemplateView.as_view(
        template_name='api/products/test.html'
    ), name='products_list_ang_test'),
    url(r"^categories_ang/$", TemplateView.as_view(
        template_name='api/categories/index.html'
    ), name='categories_list_ang'),
    url(r"^products_ang/show/$", TemplateView.as_view(
        template_name='api/products/show.html'
    ), name='products_detail_ang'),
    ]