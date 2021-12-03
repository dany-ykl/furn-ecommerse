from django.http.response import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from shop.models import Product, Category
from cart.models import Customer
from accounts.models import CustomUser
from api import serializers as api_s
    


class ProductList(APIView):

    def get(self, request, format=None):
        queryset = Product.objects.all()
        serializer = api_s.ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = api_s.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetail(APIView):

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        product = self.get_object(slug)
        serializer = api_s.ProductSerializer(product)
        return JsonResponse(serializer.data)


class CategoryList(APIView):

    def get(self, request, format=None):
        queryset = Category.objects.all()
        serializer = api_s.CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = api_s.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):

    def get_object(self, id):
        try:
            return Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, id, format=None):
        category = self.get_object(id)
        serializer = api_s.CategorySerializer(category)
        return JsonResponse(serializer.data)

    def delete(self, request, id, format=None):
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class CustomerList(APIView):

    def get(self, request, foramt=None):
        queryset = Customer.objects.all()
        serializer = api_s.CustomerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = api_s.CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):

    def get_object(self, id):
        try:
            return Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        customer = self.get_object(id)
        serializer = api_s.CustomerSerializer(customer)
        return JsonResponse(serializer.data)

    def put(self, request, id, format=None):
        customer = self.get_object(id)
        serializer = api_s.CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, format=None):
        customer = self.get_object(id)
        serializer = api_s.CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        customer = self.get_object(id)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountList(APIView):

    def get(self, request, format=None):
        queryset = CustomUser.objects.all()
        serializer = api_s.AccountSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = api_s.AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):

    def get_object(self, id):
        try:
            return CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        account = self.get_object(id)
        serializer = api_s.AccountSerializer(account)
        return JsonResponse(serializer.data)

    def put(self, request, id, format=None):
        account = self.get_object(id)
        serializer = api_s.AccountSerializerPUT(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        account = self.get_object(id)
        serializer = api_s.AccountSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        account = self.get_object(id)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








