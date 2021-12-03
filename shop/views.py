from django.shortcuts import render
from .mixins import OrderMixin
from django.views import generic
from .models import Product
from .shop_service import get_products_list


class HomeView(generic.View):
    
    def get(self, request, *args, **kwargs):
        if not request.session.exists(request.session.session_key):
            request.session.create()

        context = get_products_list(request)   

        return render(request, 'shop/base.html', context)


class ProductListView(generic.ListView):
    model = Product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductDetailView(generic.DetailView):
    model = Product

    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
