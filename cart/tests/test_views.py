from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import AnonymousUser
from django.core import mail

from cart import cart_service
from cart import views
from accounts.models import CustomUser
from cart.models import Customer, Order, CartOrder
from shop.models import Category, Product


service = cart_service

class CartViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create(
            email='test@mail.com',
            first_name='test',
            password='test!rtek[1111'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            name='test',
            email='test@mail.com'
        )
        self.category = Category.objects.create(name='Sofa')
        self.product_a = Product.objects.create(
            category=self.category,
            name='Sofa V',
            description='Description for the Sofa V',
            image=SimpleUploadedFile(name='sofa_3.jpg', content=b'', content_type='image/jpeg'),
            price=5000.00,
            stock=10,
            slug='sofa-v'
        )
        self.product_b = Product.objects.create(
            category=self.category,
            name='Sofa B',
            description='Description for the Sofa B',
            image=SimpleUploadedFile(name='sofa_3.jpg', content=b'', content_type='image/jpeg'),
            price=5000.00,
            stock=10,
            slug='sofa-b'
        )
        self.order = Order.objects.create(owner=self.customer)
        self.factory = RequestFactory()

    def test_cart_view_get(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('cart/cart.html')
        self.assertIsInstance(response.context['customer'], Customer)
        self.assertIsInstance(response.context['order'], Order)

    def test_viewadd_to_cart_ajax_for_user(self):
        #test add to cart
        request = self.factory.get('')
        request.user = self.user
        response = views.add_to_cart_ajax(
            request,
            slug=self.product_a.slug,
            order=self.order,
            customer=self.customer
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

        #add second product
        response = views.add_to_cart_ajax(
            request,
            slug=self.product_b.slug,
            order=self.order,
            customer=self.customer
        )

        order = Order.objects.get(owner=self.customer)
        self.assertEqual(order.final_price, 10000)
        self.assertEqual(order.total_products, 2)

    def test_view_add_to_cart_ajax_for_anonym(self):
        request = self.factory.get('')
        request.user = AnonymousUser()
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        customer = Customer.objects.create(
            anonymos_user=True,
            session_id=request.session.session_key
        )
        order = Order.objects.create(
            owner=customer,
            for_anonymos_user=True
        )
        response = views.add_to_cart_ajax(
            request,
            slug=self.product_a.slug,
            order=order,
            customer=customer
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        self.assertEqual(order.products.count(), 1)

        response = views.add_to_cart_ajax(
            request,
            slug=self.product_b.slug,
            order=order,
            customer=customer
        )
        order = Order.objects.get(owner=customer)
        self.assertEqual(order.total_products, 2)
        self.assertEqual(order.final_price, 10000)

    def test_view_delete_from_cart_ajax_for_user(self):
        #test add to cart
        request = self.factory.get('')
        request.user = self.user
        response = views.add_to_cart_ajax(
            request,
            slug=self.product_a.slug,
            order=self.order,
            customer=self.customer
        )
        #add second product
        response = views.add_to_cart_ajax(
            request,
            slug=self.product_b.slug,
            order=self.order,
            customer=self.customer
        )
        #delete
        response_delete = views.delete_from_cart_ajax(
            request,
            article=self.order.products.first().article,
            order=self.order,
            customer=self.customer
        )
        order = Order.objects.get(owner=self.customer)
        self.assertEqual(response_delete.status_code, 200)
        self.assertEqual(order.total_products, 1)
        self.assertEqual(order.final_price, 5000)

    def test_view_delete_from_cart_ajax_for_anonym(self):
        request = self.factory.get('')
        request.user = AnonymousUser()
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        customer = Customer.objects.create(
            anonymos_user=True,
            session_id=request.session.session_key
        )

        order = Order.objects.create(
            owner=customer,
            for_anonymos_user=True
        )
        views.add_to_cart_ajax(
            request,
            slug=self.product_a.slug,
            order=order,
            customer=customer
        )
        views.add_to_cart_ajax(
            request,
            slug=self.product_b.slug,
            order=order,
            customer=customer
        )
        response_delete = views.delete_from_cart_ajax(
            request,
            article=order.products.first().article,
            order=order,
            customer=customer
        )
        order = Order.objects.get(owner=customer)
        self.assertEqual(response_delete.status_code, 200)
        self.assertEqual(order.total_products, 1)
        self.assertEqual(order.final_price, 5000)

    def test_view_order_registration_for_user(self):
        request = self.factory.get('')
        request.user = self.user
        views.add_to_cart_ajax(
            request,
            slug=self.product_a.slug,
            order=self.order,
            customer=self.customer
        )
        data = {
            'email': self.user.email,
            'number': 123412312,
            'full_name': 'Test Testovich',
            'address': 'Test address',
            'delivery': ('free')
        }
        request = self.factory.post('', data=data, content_type="application/x-www-form-urlencoded")
        request.user = self.user
        request.POST = data
        response = views.order_registration(request, cart=self.order)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('cart/thanks.html')
        self.assertEqual(CartOrder.objects.count(), 1)
        self.assertEqual(CartOrder.objects.get(owner=self.user.email).owner, self.user.email)
        self.assertEqual(self.order.products.count(), 0)

    def test_view_order_registration_for_anonym(self):
        data = {
            'email': 'test_anonym@mail.com',
            'number': 123412312,
            'full_name': 'Test Testovich',
            'address': 'Test address',
            'delivery': ('free')
        }
        request = self.factory.post('', data=data, content_type="application/x-www-form-urlencoded")
        request.user = AnonymousUser()
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        customer = Customer.objects.create(
            anonymos_user=True,
            session_id=request.session.session_key
        )
        order = Order.objects.create(
            owner=customer,
            for_anonymos_user=True)

        views.add_to_cart_ajax(
            request,
            slug=self.product_a.slug,
            order=order,
            customer=customer
        )
        request.POST = data
        response = views.order_registration(request, cart=order)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('cart/thanks.html')
        self.assertEqual(CartOrder.objects.get(owner=data['email']).owner, data['email'])
        self.assertEqual(order.products.count(), 0)

    def test_send_email_order_to_shop(self):
        service.send_email_order_to_shop(self.order)
        self.assertEqual(len(mail.outbox), 1)