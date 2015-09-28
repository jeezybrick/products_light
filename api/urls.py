__author__ = 'user'

from django.conf.urls import include, url
from rest_framework import routers
from django.views.generic import TemplateView
from api import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
#router.register(r'categories', views.CategoryViewSet)
# router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/items/$', views.ItemList.as_view(), name='item-list'),
    url(r'^api/items/(?P<pk>[0-9]+)/$', views.ItemDetail.as_view(), name='item-detail'),
    url(r'^api/rates/$', views.RateList.as_view(), name='rate-list'),
    url(r'^api/comments/$', views.CommentList.as_view(), name='comment-list'),
    url(r'^api/categories/$', views.CategoryList.as_view(), name='category-list'),

    ]