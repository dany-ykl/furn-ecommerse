from django.shortcuts import render
from django.views import generic
from . import cart_service
from shop.mixins import OrderMixin, get_cart_and_customer


class CartView(OrderMixin, generic.View):
    
    def get(self, request, *args, **kwargs):
        context = {
            'customer': self.customer,
            'order': self.order,
            }
        return render(request, 'cart/cart.html', context)


@get_cart_and_customer
def order_registration(request, *args, **kwargs):
    return cart_service._order_registration(request, cart=kwargs['order'])


@get_cart_and_customer
def add_to_cart_ajax(request, *args, **kwargs):
    return cart_service._add_to_cart_ajax(
                        slug=kwargs['slug'],
                        order=kwargs['order'],
                        customer=kwargs['customer']
                        )    


@get_cart_and_customer
def delete_from_cart_ajax(request, *args, **kwargs):
    return cart_service._delete_from_cart_ajax(
                        article=kwargs['article'],
                        order=kwargs['order'],
                        customer=kwargs['order'].owner
                        )


class ThanksPage(generic.View):

    def get(self, request, *args, **kwargs):
        return render(request, 'cart/thanks.html')
