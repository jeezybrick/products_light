
from django.conf.urls import url
from categories import views


urlpatterns = [

    # Categories views
    url(r"^categories/add/$", views.CategoryAddView.as_view(), name='categories_add'),
    url(r"^categories/$", views.CategoryListView.as_view(), name='categories_list'),


]
