from django.urls import path, include
from api import views
from rest_framework import routers


urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('product/<slug:slug>', views.ProductDetail.as_view(), name='product-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:id>', views.CategoryDetail.as_view(), name='category-list'),
    path('customers/', views.CustomerList.as_view(), name='customer-list'),
    path('customer/<int:id>', views.CustomerDetail.as_view(), name='customer-detail'),
    path('accounts/', views.AccountList.as_view(), name='account-list'),
    path('account/<int:id>', views.AccountDetail.as_view(), name='account-detail'),

]