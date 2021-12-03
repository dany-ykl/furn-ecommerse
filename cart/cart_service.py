from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db import models
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect

from shop.models import Product
from .forms import CartOrderForm
from .models import OrderItem, CartOrder, Order, Customer


def recalculate_cart(order: Order):
    order.total_products = order.products.count()
    order_data = order.products.aggregate(models.Sum('final_price'))
    if order_data['final_price__sum']:
        order.final_price = order_data['final_price__sum']
    else:
        order.final_price = 0
    order.save()

def _order_registration(request, cart: Order) -> (HttpResponseRedirect or HttpResponse):
    if request.method == 'POST':
        
        form = CartOrderForm(request.POST)

        if request.POST.get('email'):
            owner = request.POST['email']
        else:
            owner = cart.email_or_session  
        if form.is_valid():
            order = CartOrder.objects.create(
                owner=owner,
                full_name=request.POST['full_name'],
                address=request.POST['address'],
                delivery=request.POST['delivery'],
                final_price=cart.final_price,
                total_products=cart.total_products,
                number=request.POST['number']
                )

            for product in cart.products.all():
                product.content_object.stock -=1
                product.content_object.save()
            
            order.save()

            order.products.add(*cart.products.all())

            if request.POST['email']:
                send_email_order_to_client(order)
            send_email_order_to_shop(order)
            cart.products.all().delete()

            return HttpResponseRedirect(reverse_lazy('cart:thanks'))

    else:
        form = CartOrderForm()
    return render(request, 'cart/create_order.html', {'form': form})


def _delete_from_cart_ajax(article:str, order:Order, customer:Customer) -> JsonResponse:
    order_product = OrderItem.objects.filter(
        user=customer,
        order=order, 
        article=article).first()
    
    order.products.remove(order_product)
    order_product.delete()
    recalculate_cart(order)
    order.save()
    return JsonResponse({'success':True})


def _add_to_cart_ajax(slug:str, order:Order, customer:Customer) -> JsonResponse:
    product = Product.objects.get(slug=slug)
    order_product = OrderItem.objects.create(
        user=customer,
        order=order,
        content_object=product,
        final_price=product.price)
    order.products.add(order_product)
    recalculate_cart(order)
    order.save()
    return JsonResponse({'success':True})


def send_email_order_to_client(order: CartOrder) -> None:
    subject, from_email, to = 'Hello, your order!', 'shopfurn24@gmail.com', order.owner
    html_message = render_to_string(
                    'cart/order_email.html', 
                    {'order': order})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        

def send_email_order_to_shop(order: CartOrder) -> None:
    """Sends email to the order processing service """

    subject, from_email, to = f'Hello {order.owner}, your order!', 'shopfurn24@gmail.com', 'shopfurnservice@gmail.com'
    html_message = render_to_string(
                    'cart/order_email.html', 
                    {'order': order})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


