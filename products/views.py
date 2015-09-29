from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from products import cache
from .models import Rate, Category, Item
from .forms import MyRegForm, AddComment, AddRate, AddItem, MyLoginForm, AddCategory
from haystack.query import SearchQuerySet
# Create your views here.


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/auth/login/')


class LoginView(View):

    form_class = MyLoginForm
    template_name = 'products/auth/login.html'
    success_url = '/'

    def get(self, request):

        form = self.form_class(request)
        context = {
            'form': form,
            'title': 'Sign In',
        }
        return TemplateResponse(request, self.template_name, context)

    def post(self, request):

        form = MyLoginForm(request, data=request.POST)
        context = {
            'form': form,
            'title': 'Sign In',
        }
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(self.success_url)
        return TemplateResponse(request, self.template_name, context)


class ItemListView(View):
    template_name = 'products/products/index.html'

    def get(self, request):
        try:
            request.GET["category"]
        except:
            products = SearchQuerySet().models(Item).order_by('-id')
        else:
            products = SearchQuerySet().models(Item).filter(categories__name=request.GET["category"]).order_by('-id')
        facets = SearchQuerySet().models(Item).facet('categories').facet_counts()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'products': products, 'facets': facets})


class ItemDetailView(View):

    template_name = 'products/products/show.html'

    def get(self, request, *args, **kwargs):
        item = cache.ProductCache().get(id=kwargs["pk"])
        # comments = cache.CommentCache().get(item_id=kwargs["pk"])
        user_rate = None
        for item in item:
            try:
                user_rate = Rate.objects.get(user=request.user.id, item=item.id)
            except:
                user_rate = None
        context = {
            'comment_form': AddComment,
            'rating_form': AddRate(instance=user_rate),
            'average_rating': Rate.objects.filter(item_id=self.kwargs["pk"]).aggregate(Avg('value')),
            'item': item,
        }
        return render(request, self.template_name, context)


class ItemAddView(CreateView):

    model = cache.ProductCache.model
    template_name = 'products/products/modify.html'
    success_url = '/products/'
    form_class = AddItem

    def get_context_data(self, **kwargs):
        context = super(ItemAddView, self).get_context_data(**kwargs)
        context['foo'] = _('Add')
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Item add!'))
        return super(ItemAddView, self).form_valid(form)


class CategoryListView(ListView):

    template_name = 'products/categories/index.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        return cache.CategoryCache().get(parent_category_id__isnull=True)


class CategoryAddView(CreateView):

    model = Category
    template_name = 'products/categories/modify.html'
    success_url = '/categories/'
    form_class = AddCategory

    def get_context_data(self, **kwargs):
        context = super(CategoryAddView, self).get_context_data(**kwargs)
        context['foo'] = _('Add')
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Category add!'))
        return super(CategoryAddView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class RegisterView(View):

    form_class = MyRegForm
    template_name = 'products/auth/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/auth/register/success')
        return render(request, self.template_name, {'form': form})


class AddCommentView(View):

    form_class = AddComment

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            first = form.save(commit=False)
            first.item = get_object_or_404(cache.ProductCache.model, id=kwargs["pk"])
            first.save()
            messages.success(self.request, _('Your comment add!'))
            return HttpResponseRedirect('/products/'+kwargs["pk"]+'/')
        return render(request, 'products/products/show.html', {'form': form})


class AddRateView(LoginRequiredMixin, View):

    form_class = AddRate

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=kwargs["pk"])
        try:
            rate = Rate.objects.get(user=request.user.id, item=item.id)
        except:
            rate = None
        form = self.form_class(request.POST, instance=rate)
        if form.is_valid():
            first = form.save(commit=False)
            first.item = get_object_or_404(cache.ProductCache.model, id=kwargs["pk"])
            first.user = request.user
            first.save()
            messages.success(self.request, _('Thanks for rate!'))
            return HttpResponseRedirect('/products/'+kwargs["pk"]+'/')
        return render(request, 'products/products/show.html', {'form': form})


def get_logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


class ItemEditView(UpdateView):

    model = Item
    template_name = 'products/products/modify.html'
    success_url = '/products/'
    form_class = AddItem

    def get_context_data(self, **kwargs):
        context = super(ItemEditView, self).get_context_data(**kwargs)
        context['foo'] = _('Edit')
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Item edit!'))
        return super(ItemEditView, self).form_valid(form)