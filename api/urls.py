__author__ = 'user'

from django.conf.urls import include, url
from rest_framework import routers
from .serializers import UserViewSet, ItemViewSet, CategoryViewSet
from django.views.generic import ListView, DetailView, TemplateView
from .views import ItemList

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r"^products_ang/$", TemplateView.as_view(
        template_name='api/products/index.html'
    ), name='products_list_ang'),
    url(r"^categories_ang/$", TemplateView.as_view(
        template_name='api/categories/index.html'
    ), name='categories_list_ang'),
    ]