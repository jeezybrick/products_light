from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from cart.service import CartService
from cart import forms


# For redirect if not Auth
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/auth/login/')


# List of items in cart for
class CartView(LoginRequiredMixin, View):
    template_name = 'cart/index.html'
    form_class = forms.AddItemToCart

    def get(self, request):
        cart = CartService().get_cart(request.user)
        context = {
            'cart': cart,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            first = form.save(commit=False)
            first.user = request.user
            first.save()
            messages.success(self.request, _('Item add to cart!'))
            return HttpResponseRedirect(reverse('products_list'))
        return render(request, self.template_name, {'form': form})
