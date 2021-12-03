from django.contrib.auth.models import AnonymousUser
from django.http import response
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.views.generic import View

from accounts.models import CustomUser
from cart.models import Customer, Order
from shop import mixins 


class ShopMixinsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create(
            email='test@mail.com',
            first_name='test',
            password='test!rtek[1111')

        
    @mixins.get_cart_and_customer    
    def method_for_mixins(self, request, *args, **kwargs):
        return request, args, kwargs
    

    def test_method_get_cart_and_customer_for_user(self):
        request = self.factory.get('/')
        request.user = self.user

        response = self.method_for_mixins(request)
        self.assertIsInstance(response[2]['order'], Order)
        self.assertIsInstance(response[2]['customer'], Customer)


    def test_method_get_cart_and_customer_for_anonym_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()

        #create session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.create()

        response = self.method_for_mixins(request)
        self.assertIsInstance(response[2]['order'], Order)
        self.assertIsInstance(response[2]['customer'], Customer)

    
    class TestMix(mixins.OrderMixin, View):

        def get(self, requset, *args, **kwargs):
            context = {'customer': self.customer,
                        'order': self.order
                        }
            return context

    def test_class_mixins_get_cart_castomer(self):
        request = self.factory.get('/')
        request.user = self.user
        response = self.TestMix.as_view()(request)
        self.assertIsInstance(response['order'], Order)
        self.assertIsInstance(response['customer'], Customer)





