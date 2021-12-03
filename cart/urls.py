from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),

    path('add-to-cart/<str:slug>/',
    views.add_to_cart_ajax,
    name='add_to_cart_ajax'),

    path('delete-from-cart/<str:article>/',
     views.delete_from_cart_ajax,
     name='delete_from_cart_ajax'),

    path('order-registration',
    views.order_registration,
    name='order_registration'),

    path('thanks',
    views.ThanksPage.as_view(),
    name='thanks')
]