from shop.models import Product
from django.contrib import admin
from .models import OrderItem, Order, Customer, CartOrder


class ProductInline(admin.StackedInline):
    model = CartOrder.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    list_display = (
     'owner', 'total_products',
     'final_price', 'in_order',
     'for_anonymos_user'
     )

    list_filter = [
    'total_products', 'final_price',
     'in_order', 'for_anonymos_user']

    search_fields = ['email_or_session']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'get_name', 'name', 'anonymos_user'
    )    

    list_filter = ['anonymos_user']

    search_fields = ['email']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ('get_name', 'order', 'qty', 'final_price', 'article')

    search_fields = ['article']


@admin.register(CartOrder)
class CartOrderAdmin(admin.ModelAdmin):

    list_display = (
    'owner', 'full_name', 'address', 
    'delivery', 'total_products', 
    'data_create', 'final_price', 'completed', 'number'
    )

    list_filter = [
        'delivery', 'total_products',
        'data_create', 'final_price', 'completed'
         ]