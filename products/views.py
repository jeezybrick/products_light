from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from products import cache
from products.service import  RateService
from .models import Rate, Item, MyUser
from products import forms
from products import models
from products import utils
from haystack.query import SearchQuerySet


# For redirect if not Auth
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/auth/login/')


# For list of items
class ItemListView(View):
    template_name = 'products/products/index.html'

    def get(self, request):
        # Sort by category
        category = request.GET.get('category', False)
        if not category:
            products = SearchQuerySet().models(Item).all().order_by('-id')
        else:
            products = SearchQuerySet().models(Item).filter(
                categories__name=category).order_by('-id')
        # Facet
        facets = SearchQuerySet().models(Item).facet('categories').facet_counts()
        # Pagination
        paginator = Paginator(products, 6)
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'products': products,
                                                    'facets': facets})


# Item detail
class ItemDetailView(View):
    template_name = 'products/products/show.html'

    def get(self, request, **kwargs):

        # get item and current user rate to this item
        item = cache.ProductDetailCache().get(id=kwargs["pk"])
        user_rate = RateService().get_rate(request.user, item.id)

        message = utils.message_of_quantity_items(item)
        item = utils.price_with_percent(item)

        context = {
            'comment_form': forms.AddComment,
            'rating_form': forms.AddRate(instance=user_rate),
            'average_rating': RateService().get_avarage_rate(item.id),
            'item': item,
            'message': message,
        }
        return render(request, self.template_name, context)


# For add new item
class ItemAddView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'products/products/modify.html'
    success_url = '/products_ang/'
    form_class = forms.ModifyItem

    def get_context_data(self, **kwargs):
        context = super(ItemAddView, self).get_context_data(**kwargs)
        context['foo'] = _('Add')
        self.if_user_not_a_shop()
        return context

    def form_valid(self, form):
        first = form.save(commit=False)
        first.user = self.request.user
        first.save()
        messages.success(self.request, _('Item added!'))
        return super(ItemAddView, self).form_valid(form)

    def if_user_not_a_shop(self):
        if not self.request.user.is_shop:
            raise PermissionDenied


# For adding new comments to detail
class AddCommentView(View):
    form_class = forms.AddComment
    template_name = 'products/products/show.html'

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            first = form.save(commit=False)
            first.item = get_object_or_404(models.Item, id=kwargs["pk"])
            first.save()
            messages.success(self.request, _('Your comment add!'))
            return HttpResponseRedirect(reverse('products_show', args=(kwargs["pk"],)))
        return render(request, self.template_name, {'form': form})


# Add rate for specific item
class AddRateView(LoginRequiredMixin, View):
    form_class = forms.AddRate
    template_name = 'products/products/show.html'

    def post(self, request, **kwargs):
        item = get_object_or_404(Item, id=kwargs["pk"])
        try:
            rate = Rate.objects.get(user=request.user.id, item=item.id)
        except ObjectDoesNotExist:
            rate = None
        form = self.form_class(request.POST, instance=rate)
        if form.is_valid():
            first = form.save(commit=False)
            first.item = get_object_or_404(models.Item, id=kwargs["pk"])
            first.user = request.user
            first.save()
            messages.success(self.request, _('Thanks for rate!'))
            return HttpResponseRedirect(reverse('products_show', args=(kwargs["pk"],)))
        return render(request, self.template_name, {'form': form})


# class for edit item
class ItemEditView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'products/products/modify.html'
    success_url = '/products/'
    form_class = forms.ModifyItem

    def get_context_data(self, **kwargs):
        context = super(ItemEditView, self).get_context_data(**kwargs)
        context['foo'] = _('Edit')
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Item edit!'))
        return super(ItemEditView, self).form_valid(form)


# Delete item view
class ItemDeleteView(DeleteView):
    model = Item
    success_url = '/products/'

    def form_valid(self):
        messages.success(self.request, _('Item delete!'))


# List of shops
class ShopListView(View):
    template_name = 'products/shops/index.html'

    def get(self, request):

        shops = SearchQuerySet().models(MyUser).filter(is_shop=True).order_by('-id')
        # Pagination
        paginator = Paginator(shops, 6)
        page = request.GET.get('page')

        try:
            shops = paginator.page(page)
        except PageNotAnInteger:
            shops = paginator.page(1)
        except EmptyPage:
            shops = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'shops': shops})


# Shop detail
class ShopDetailView(View):
    template_name = 'products/shops/show.html'

    def get(self, request, **kwargs):
        shop = cache.ShopDetailCache().get(id=kwargs["pk"])
        context = {
            'shop': shop,
        }
        return render(request, self.template_name, context)


""" View for add/edit action for item """


class ItemActionView(CreateView):
    model = models.Action
    template_name = 'products/actions/modify.html'
    success_url = '/'
    form_class = forms.ModifyAction

    def get_context_data(self, **kwargs):
        context = super(ItemActionView, self).get_context_data(**kwargs)
        context['foo'] = _('Add')
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Action add!'))
        return super(ItemActionView, self).form_valid(form)
