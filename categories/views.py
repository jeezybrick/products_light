from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from categories import cache
from categories.models import Category
from categories.forms import AddCategory
from products.views import LoginRequiredMixin


# Category list
class CategoryListView(ListView):
    template_name = 'categories/index.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        return cache.CategoryCache().get(parent_category_id__isnull=True)


# For add new category
class CategoryAddView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'categories/modify.html'
    form_class = AddCategory
    success_msg = _('Category added!')

    def get_context_data(self, **kwargs):
        context = super(CategoryAddView, self).get_context_data(**kwargs)
        context['foo'] = _('Add')
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super(CategoryAddView, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("categories_list_ang")
