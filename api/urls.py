
from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^api/items/$', views.ItemList.as_view(), name='item_list'),
    url(r'^api/items/(?P<pk>[0-9]+)/$',
        views.ItemDetail.as_view(), name='item_detail'),

    url(r'^api/rates/$', views.RateList.as_view(), name='rate_list'),

    url(r'^api/comments/$', views.CommentList.as_view(), name='comment_list'),

    url(r'^api/categories/$', views.CategoryList.as_view(), name='category_list'),

    url(r'^api/shops/$', views.ShopList.as_view(), name='shop_list'),
    url(r'^api/shops/(?P<pk>[0-9]+)/$',
        views.ShopDetail.as_view(), name='shop_detail'),

    url(r'^api/cart/$', views.CartList.as_view(), name='cart_list'),
    url(r'^api/cart/(?P<pk>[0-9]+)/$',
        views.CartDetail.as_view(), name='cart_detail'),

    url(r'^api/action/$', views.ActionList.as_view(), name='action_list'),


]
