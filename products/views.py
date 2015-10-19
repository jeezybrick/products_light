from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from products import cache
from products.service import RateService
from .models import Rate, Item
from products import forms
from products import models
from products import utils
from products.validators import if_user_not_a_shop
from my_auth.models import MyUser
from my_auth.cache import ShopDetailCache
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
            products_list = SearchQuerySet().models(Item).all().order_by('-id')
        else:
            products_list = SearchQuerySet().models(Item).filter(
                categories__name=category).order_by('-id')
        # Facet
        facets = SearchQuerySet().models(Item).facet('categories').facet_counts()
        # Pagination
        paginator = Paginator(products_list, 6)
        page = request.GET.get('page')

        try:
            products_list = paginator.page(page)
        except PageNotAnInteger:
            products_list = paginator.page(1)
        except EmptyPage:
            products_list = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'products_list': products_list,
                                                    'facets': facets, })


# Item detail
class ItemDetailView(View):
    template_name = 'products/products/show.html'

    def get(self, request, **kwargs):

        # get item and current user rate to this item
        item = cache.ProductDetailCache().get(id=kwargs["pk"])
        user_rate = RateService().get_rate(request.user, item.id)

        # quantity-count message
        message_of_quantity_count = utils.message_of_quantity_items(item)
        item = utils.price_with_percent(item)

        context = {
            'comment_form': forms.AddComment,
            'rating_form': forms.AddRate(instance=user_rate),
            'average_rating': models.Rate.objects.average(item_id=item.id),
            'item': item,
            'message': message_of_quantity_count,
        }
        return render(request, self.template_name, context)


# For add new item
class ItemAddView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'products/products/modify.html'
    form_class = forms.ModifyItem
    success_msg = _('Item added!')

    def get_context_data(self, **kwargs):
        context = super(ItemAddView, self).get_context_data(**kwargs)
        context['foo'] = _('Add')
        if_user_not_a_shop(self)  # Check if auth user is shop
        return context

    def form_valid(self, form):
        first = form.save(commit=False)
        first.user = self.request.user
        first.save()
        messages.success(self.request, self.success_msg)
        return super(ItemAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse("products_list_ang")


# class for edit item
class ItemEditView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'products/products/modify.html'
    form_class = forms.ModifyItem
    success_msg = _('Item edited!')

    def get_context_data(self, **kwargs):
        context = super(ItemEditView, self).get_context_data(**kwargs)
        context['foo'] = _('Edit')
        if_user_not_a_shop(self)  # Check if auth user is shop
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super(ItemEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse("products_list")


# Delete item view
class ItemDeleteView(DeleteView):
    model = Item
    success_msg = _('Item delete!')

    def form_valid(self):
        messages.success(self.request, self.success_msg)

    def get_success_url(self):
        return reverse("products_list")


# For adding new comments to detail
class AddCommentView(View):
    form_class = forms.AddComment
    template_name = 'products/products/show.html'
    success_msg = _('Your comment added!')

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            first = form.save(commit=False)
            first.item = get_object_or_404(models.Item, id=kwargs["pk"])
            first.save()
            messages.success(self.request, self.success_msg)
            return HttpResponseRedirect(reverse('products_show', args=(kwargs["pk"],)))
        return render(request, self.template_name, {'form': form})


# Add rate for specific item
class AddRateView(LoginRequiredMixin, View):
    form_class = forms.AddRate
    template_name = 'products/products/show.html'
    success_msg = _('Thanks for your rating!')

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
            messages.success(self.request, self.success_msg)
            return HttpResponseRedirect(reverse('products_show', args=(kwargs["pk"],)))
        return render(request, self.template_name, {'form': form})


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
        shop = ShopDetailCache().get(id=kwargs["pk"])
        context = {
            'shop': shop,
        }
        return render(request, self.template_name, context)


""" View for add/edit action for item """


class ItemActionView(CreateView):
    model = models.Action
    template_name = 'products/actions/modify.html'
    form_class = forms.ModifyAction
    success_msg = _('Action add!')

    def get_context_data(self, **kwargs):
        context = super(ItemActionView, self).get_context_data(**kwargs)
        context['foo'] = _('Add')
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super(ItemActionView, self).form_valid(form)

    def get_success_url(self):
        return reverse("products_list_ang")
