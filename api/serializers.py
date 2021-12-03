from django.db.models import fields
from rest_framework import serializers
from shop.models import Product, Category
from cart import models
from accounts.models import CustomUser


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('category', 'name', 'image', 'price', 'stock', 'available', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    count = serializers.IntegerField(required=False)
    products = serializers.ListField(
        child=serializers.CharField(), 
        source='get_products',
        required=False,
        )
    
    class Meta:
        model = Category
        fields = ('name', 'count', 'products')


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            password=validated_data['password']
        )
        return user


class AccountSerializerPUT(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'is_active', 'is_staff', 'is_superuser')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.save()
        return instance