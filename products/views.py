from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .cache import Item, Category
from .models import Rate
from .forms import MyRegForm, AddComment, AddRate, AddItem
from haystack.query import SearchQuerySet
# Create your views here.


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/auth/login/')


class ItemListView(View):
    template_name = 'products/products/index.html'

    def get(self, request, *args, **kwargs):
        products = SearchQuerySet().models(Item).all()
        # products = Item.objects.all()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'products': products})


class ItemDetailView(DetailView):

    model = Item
    context_object_name = 'item'
    template_name = 'products/products/show.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = AddComment
        context['rating_form'] = AddRate
        context['average_rating'] = Rate.objects.filter(item_id=self.kwargs["pk"]).aggregate(Avg('value'))
        return context


class ItemAddView(CreateView):

    model = Item
    template_name = 'products/products/add.html'
    success_url = '/products/'
    form_class = AddItem

    def get_context_data(self, **kwargs):
        context = super(ItemAddView, self).get_context_data(**kwargs)
        context['foo'] = 'Добавить'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Товар добавлен!')
        return super(ItemAddView, self).form_valid(form)


class CategoryListView(ListView):

    template_name = 'products/categories/index.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        return Category.objects.filter(parent_category_id__isnull=True)


class CategoryAddView(CreateView):

    model = Category
    fields = ('name', 'parent_category')
    template_name = 'products/categories/modify.html'
    success_url = '/categories/'

    def get_context_data(self, **kwargs):
        context = super(CategoryAddView, self).get_context_data(**kwargs)
        context['foo'] = 'Добавить'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Категория добавлена!')
        return super(CategoryAddView, self).form_valid(form)


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

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            first = form.save(commit=False)
            first.item = get_object_or_404(Item, id=kwargs["pk"])
            first.save()
            messages.success(self.request, 'Ваш комментарий добавлен!')
            return HttpResponseRedirect('/products/'+kwargs["pk"]+'/')
        return render(request, 'products/products/show.html', {'form': form})


class AddRateView(LoginRequiredMixin, View):

    form_class = AddRate

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            first = form.save(commit=False)
            first.item = get_object_or_404(Item, id=kwargs["pk"])
            first.user = request.user
            first.save()
            messages.success(self.request, 'Вы поставили оценку!')
            return HttpResponseRedirect('/products/'+kwargs["pk"]+'/')
        return render(request, 'products/products/show.html', {'form': form})