__author__ = 'user'

from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^api/items/$', views.ItemList.as_view(), name='item-list'),
    url(r'^api/items/(?P<pk>[0-9]+)/$',
        views.ItemDetail.as_view(), name='item-detail'),
    url(r'^api/rates/$', views.RateList.as_view(), name='rate-list'),
    url(r'^api/comments/$', views.CommentList.as_view(), name='comment-list'),
    url(r'^api/categories/$', views.CategoryList.as_view(), name='category-list'),
    url(r'^api/shops/$', views.ShopList.as_view(), name='shop-list'),
    url(r'^api/shops/(?P<pk>[0-9]+)/$',
        views.ShopDetail.as_view(), name='shop-detail'),
    url(r'^api/cart/$', views.ShopList.as_view(), name='shop-list'),


]
