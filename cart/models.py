import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from accounts.models import CustomUser


class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    anonymos_user = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100, default='', null=True, blank=True)

    def __str__(self):
        if self.user:
            return str(self.user)
        else:
            return str(self.session_id)

    def get_name(self):
        """for admin page"""
        if self.user:
            return str(self.user)
        else:
            return str(self.session_id)


class OrderItem(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='related_orders')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)
    article = models.UUIDField(default=uuid.uuid4)


    def __str__(self):
        return f'Product: {self.object_id}|{self.content_object.name}'

    def get_name(self):
        """for admin page"""
        return  self.content_object.name

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Order(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    email_or_session = models.CharField(max_length=100)
    products = models.ManyToManyField(OrderItem, blank=True, related_name='related_order')
    total_products = models.PositiveIntegerField(default=0, blank=True)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anonymos_user = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.email_or_session = str(self.owner)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.owner)


class CartOrder(models.Model):

    DELIVERY_CHOICE = [
        ('free', 'Pickup'),
        ('info', 'Delivery by mail'),
        ('info', 'Delivery by courier')
    ]

    owner = models.CharField(max_length=100, default='anonym')
    products = models.ManyToManyField(OrderItem, blank=True, related_name='related_products')
    total_products = models.PositiveIntegerField(default=0)
    article = models.UUIDField(default=uuid.uuid4)
    full_name = models.CharField(max_length=400)
    address = models.CharField(max_length=500)
    delivery = models.CharField(max_length=50, choices=DELIVERY_CHOICE)
    number = models.CharField(max_length=20, null=True)
    completed = models.BooleanField(default=False)
    data_create = models.DateTimeField(auto_now_add=True)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2)