from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile 
from django.test import TestCase

from cart.models import Customer, Order, CartOrder, OrderItem
from accounts.models import CustomUser
from shop.models import Product, Category
from cart import cart_service

service = cart_service

class CartModelsTestCase(TestCase):

    def setUp(self):
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
        self.anonymos = AnonymousUser()
        self.customer_anonymos = Customer.objects.create(
            anonymos_user=True,
            session_id='21321321321ewfkfwk[ew'
        )
        self.category = Category.objects.create(name='Sofa')
        self.product_one = Product.objects.create(
            category=self.category,
            name='Sofa V',
            description='Description for the Sofa V',
            image=SimpleUploadedFile(name='sofa_3.jpg', content=b'', content_type='image/jpeg'),
            price=5000.00,
            stock=10,
            slug='sofa-v'
        )
        self.product_two = Product.objects.create(
            category=self.category,
            name='Sofa B',
            description='Description for the Sofa B',
            image=SimpleUploadedFile(name='sofa_3.jpg', content=b'', content_type='image/jpeg'),
            price=5000.00,
            stock=10,
            slug='sofa-b'
        )
        self.order = Order.objects.create(owner=self.customer)
        self.order_anonym = Order.objects.create(
            owner=self.customer_anonymos,
            for_anonymos_user=True)

    def test_models_customer_method_get_name(self):
        name = self.customer.get_name()
        self.assertEqual(name, 'test@mail.com')

    def test_models_customer_method_get_name_anonym(self):
        name = self.customer_anonymos.get_name()
        session_id='21321321321ewfkfwk[ew'
        self.assertEqual(self.customer_anonymos.session_id, session_id)
        self.assertEqual(name, session_id)
        
    def create_order_item_user_or_anonym(self, anonym=False):
        if anonym:
            customer = self.customer
            order = self.order
        else:
            customer = self.customer_anonymos
            order = self.order_anonym

        order_product_one = OrderItem.objects.create(
            user=customer,
            order=order,
            content_object=self.product_one,
            final_price=self.product_one.price
        )

        order_product_two = OrderItem.objects.create(
            user=customer,
            order=order,
            content_object=self.product_two,
            final_price=self.product_one.price
        )

        return [order_product_one, order_product_two]

    def test_models_order_user(self):
        order_products = self.create_order_item_user_or_anonym()
        self.order.products.add(*order_products)
        service.recalculate_cart(self.order)
        self.order.save()
        self.assertEqual(str(self.order.owner), self.customer.email)
        self.assertEqual(self.order.email_or_session, self.customer.email)
        self.assertEqual(self.order.final_price, 10000)
        self.assertEqual(self.order.total_products, 2)
    
    def test_models_order_anonym(self):
        order_products = self.create_order_item_user_or_anonym(anonym=True)
        self.order_anonym.products.add(*order_products)
        service.recalculate_cart(self.order_anonym)
        self.order.save()
        self.assertEqual(str(self.order_anonym.owner), self.customer_anonymos.session_id)
        self.assertEqual(self.order_anonym.email_or_session, self.customer_anonymos.session_id)
        self.assertEqual(self.order_anonym.final_price, 10000)
        self.assertEqual(self.order_anonym.total_products, 2)

    def test_models_order_item(self):
        product_a, _ = [*self.create_order_item_user_or_anonym()]

        self.assertIsInstance(product_a.user, Customer)
        self.assertIsInstance(product_a.order, Order)
        self.assertIsInstance(product_a.content_object, Product)
        self.assertEqual(product_a.qty, 1)
        self.assertEqual(product_a.final_price, 5000.00)

        product_a.qty += 1
        product_a.save()

        self.assertEqual(product_a.qty, 2)
        self.assertEqual(product_a.final_price, 10000.00)

    def test_models_cart_order(self):
        products = self.create_order_item_user_or_anonym()
        self.order.products.add(*products)
        service.recalculate_cart(self.order)
        
        cart_order = CartOrder.objects.create(
            owner=str(self.customer),
            total_products=self.order.total_products,
            full_name='Test Testo',
            address='Test country',
            delivery=('free', 'Pickup'),
            number=79965623441,
            final_price=self.order.final_price
        )

        cart_order.products.add(*self.order.products.all())

        self.assertEqual(cart_order.owner, str(self.customer))
        self.assertEqual(cart_order.total_products, 2)
        self.assertEqual(cart_order.full_name, 'Test Testo')
        self.assertEqual(cart_order.address, 'Test country')
        self.assertEqual(cart_order.delivery, ('free', 'Pickup'))
        self.assertEqual(cart_order.number, 79965623441)
        self.assertEqual(cart_order.final_price, self.order.final_price)